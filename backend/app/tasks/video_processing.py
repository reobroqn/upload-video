import os
import shutil
import subprocess
import tempfile

from minio import Minio

from app.core.celery_app import celery_app
from app.core.config import settings
from app.core.database import get_db
from app.models.video import Video
from app.schemas.video_status import VideoStatus


@celery_app.task(acks_late=True)
def transcode_video(video_id: int):
    """
    Celery task to transcode a video into HLS format with multiple renditions.
    """
    original_file_path = None
    output_dir = None
    with get_db() as db:
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            print(f"Video with ID {video_id} not found.")
            return

        video.status = VideoStatus.PROCESSING
        db.add(video)
        db.commit()
        db.refresh(video)

        minio_client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False,  # Use True for HTTPS
        )

        try:
            # 1. Download the original video from MinIO
            temp_dir_for_original = tempfile.mkdtemp()
            original_file_name = video.file_key.split("/")[-1]
            original_file_path = os.path.join(temp_dir_for_original, original_file_name)

            try:
                minio_client.fget_object(
                    settings.MINIO_BUCKET_NAME, video.file_key, original_file_path
                )
                print(f"Downloaded {video.file_key} to {original_file_path}")
            except Exception as e:
                print(f"Error downloading video {video.file_key}: {e}")
                video.status = VideoStatus.FAILED
                db.add(video)
                db.commit()
                return

            # 2. Transcode to HLS with multiple renditions
            output_dir = tempfile.mkdtemp(prefix=f"{video.id}_hls_")

            # Define renditions (example: 360p, 720p)
            renditions = [
                {"height": 360, "bitrate": "800k", "audio_bitrate": "96k"},
                {"height": 720, "bitrate": "2500k", "audio_bitrate": "128k"},
            ]

            ffmpeg_command = [
                "ffmpeg",
                "-i",
                original_file_path,
                "-preset",
                "fast",
                "-g",
                "48",
                "-keyint_min",
                "48",
                "-sc_threshold",
                "0",
                "-c:v",
                "libx64",
                "-c:a",
                "aac",
                "-b:a",
                "96k",
                "-ar",
                "48000",
                "-f",
                "hls",
                "-hls_time",
                "10",
                "-hls_playlist_type",
                "vod",
                "-hls_segment_filename",
                f"{output_dir}/%v_%03d.ts",
                "-master_pl_name",
                "master.m3u8",
            ]

            for i, rendition in enumerate(renditions):
                ffmpeg_command.extend(
                    [
                        "-vf",
                        f"scale=-2:{rendition['height']}",
                        "-b:v",
                        rendition["bitrate"],
                        f"{output_dir}/stream_{rendition['height']}p.m3u8",
                    ]
                )

            try:
                # S603: The `ffmpeg_command` is constructed from a list of trusted inputs
                # and securely generated temporary file paths, mitigating the risk of
                # untrusted input execution. `shell=False` is implicitly used when passing
                # a list, preventing shell injection.
                subprocess.run(ffmpeg_command, check=True, capture_output=True)
                print(f"Transcoding complete for video ID {video_id}")
            except subprocess.CalledProcessError as e:
                print(f"FFmpeg error: {e.stderr.decode()}")
                video.status = VideoStatus.FAILED
                db.add(video)
                db.commit()
                return

            # 3. Upload HLS files to MinIO
            hls_prefix = f"hls/{video.id}/"
            try:
                for root, _, files in os.walk(output_dir):
                    for file in files:
                        local_path = os.path.join(root, file)
                        minio_path = os.path.join(
                            hls_prefix, os.path.relpath(local_path, output_dir)
                        )
                        minio_client.fput_object(
                            settings.MINIO_BUCKET_NAME, minio_path, local_path
                        )
                        print(f"Uploaded {local_path} to {minio_path}")
                # Update video with HLS manifest URL
                video.hls_url = f"http://{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET_NAME}/{hls_prefix}master.m3u8"
                video.status = VideoStatus.PROCESSED
                db.add(video)
                db.commit()
                print(f"Video ID {video_id} processed and HLS URL updated.")
            except Exception as e:
                print(f"Error uploading HLS files to MinIO: {e}")
                video.status = VideoStatus.FAILED
                db.add(video)
                db.commit()
        finally:
            # Clean up temporary files and directories
            if original_file_path and os.path.exists(
                os.path.dirname(original_file_path)
            ):
                shutil.rmtree(os.path.dirname(original_file_path))
            if output_dir and os.path.exists(output_dir):
                shutil.rmtree(output_dir)
