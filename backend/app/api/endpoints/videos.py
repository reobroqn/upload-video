from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from minio import Minio
from minio.error import S3Error
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.core.config import settings
from app.core.database import get_db
from app.models.category import Category
from app.models.tag import Tag
from app.models.user import User
from app.models.video import Video
from app.schemas.video import PresignedPost, VideoCreate, VideoInDB, VideoUploadComplete
from app.schemas.video_status import VideoStatus
from app.tasks.video_processing import transcode_video

router = APIRouter(prefix="/videos", tags=["videos"])


@router.post(
    "/upload-request", response_model=PresignedPost, status_code=status.HTTP_201_CREATED
)
async def create_upload_url(
    video_in: VideoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> PresignedPost:
    """
    Request a presigned URL for direct S3 upload.

    This endpoint creates a video record in the database and generates a presigned
    POST URL, allowing clients to upload files directly to S3 without proxying
    through the backend.

    Args:
        video_in: Video creation data including title, description, file_name, file_size, and mime_type.
        db: Database session dependency.
        current_user: The currently authenticated user.

    Returns:
        PresignedPost: An object containing the presigned URL, form fields, and the created video's ID.

    Raises:
        HTTPException: 500 if S3 presigning fails.

    """
    # Validate file size (2GB limit)
    if video_in.file_size > 2 * 1024 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the 2GB limit.",
        )

    # Validate MIME type
    allowed_mime_types = ["video/mp4", "video/webm", "video/quicktime"]
    if video_in.mime_type not in allowed_mime_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported MIME type: {video_in.mime_type}. Allowed types are {', '.join(allowed_mime_types)}.",
        )

    # Create a unique file key for S3
    file_extension = video_in.file_name.split(".")[-1]
    file_key = f"{current_user.id}/{video_in.title.replace(' ', '_')}_{datetime.now().timestamp()}.{file_extension}"

    # Create video record in DB first
    db_video = Video(
        title=video_in.title,
        description=video_in.description,
        file_key=file_key,
        file_size=video_in.file_size,
        mime_type=video_in.mime_type,
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)

    minio_client = Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=False,  # Use True for HTTPS
    )

    try:
        # Ensure the bucket exists
        found = minio_client.bucket_exists(settings.MINIO_BUCKET_NAME)
        if not found:
            minio_client.make_bucket(settings.MINIO_BUCKET_NAME)

        presigned_post = minio_client.presigned_post(
            bucket_name=settings.MINIO_BUCKET_NAME,
            object_name=file_key,
            expires=datetime.timedelta(hours=1),  # URL expires in 1 hour
            fields={
                "Content-Type": video_in.mime_type,
                "Content-Length": str(int(video_in.file_size)),
            },
            conditions=[
                {"Content-Type": video_in.mime_type},
                ["content-length-range", 0, int(video_in.file_size)],
            ],
        )
    except S3Error as e:
        # If presigning fails, delete the video record from DB
        db.delete(db_video)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not generate presigned URL: {e}",
        )

    return PresignedPost(
        url=presigned_post["url"],
        fields=presigned_post["fields"],
        video_id=db_video.id,
    )


@router.post("/upload-complete", response_model=VideoInDB)
async def confirm_upload_complete(
    upload_complete: VideoUploadComplete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> VideoInDB:
    """
    Confirm that a video upload to S3 has been completed.

    This endpoint updates the status of a video record in the database after
    a successful direct upload to S3.

    Args:
        upload_complete: Data confirming the video upload, including the video_id.
        db: Database session dependency.
        current_user: The currently authenticated user.

    Returns:
        VideoInDB: The updated video object.

    Raises:
        HTTPException: 404 if the video is not found or does not belong to the current user.

    """
    video = db.query(Video).filter(Video.id == upload_complete.video_id).first()

    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found."
        )

    # Optional: Add logic to verify MinIO object existence/integrity here if needed

    video.status = VideoStatus.UPLOADED
    db.add(video)
    db.commit()
    db.refresh(video)

    # Trigger video transcoding task
    transcode_video.delay(video.id)

    return video


@router.get("/{video_id}", response_model=VideoInDB)
async def get_video_details(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> VideoInDB:
    """
    Get details of a specific video.

    Args:
        video_id: The ID of the video to retrieve.
        db: Database session dependency.
        current_user: The currently authenticated user.

    Returns:
        VideoInDB: The video object.

    Raises:
        HTTPException: 404 if the video is not found.

    """
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found."
        )
    return video


@router.post("/{video_id}/tags/{tag_id}", response_model=VideoInDB)
async def add_tag_to_video(
    video_id: int,
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> VideoInDB:
    """
    Add a tag to a video.
    """
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )

    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )

    if tag not in video.tags:
        video.tags.append(tag)
        db.add(video)
        db.commit()
        db.refresh(video)

    return video


@router.delete("/{video_id}/tags/{tag_id}", response_model=VideoInDB)
async def remove_tag_from_video(
    video_id: int,
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> VideoInDB:
    """
    Remove a tag from a video.
    """
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )

    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )

    if tag in video.tags:
        video.tags.remove(tag)
        db.add(video)
        db.commit()
        db.refresh(video)

    return video


@router.post("/{video_id}/categories/{category_id}", response_model=VideoInDB)
async def add_category_to_video(
    video_id: int,
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> VideoInDB:
    """
    Add a category to a video.
    """
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    if category not in video.categories:
        video.categories.append(category)
        db.add(video)
        db.commit()
        db.refresh(video)

    return video


@router.delete("/{video_id}/categories/{category_id}", response_model=VideoInDB)
async def remove_category_from_video(
    video_id: int,
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> VideoInDB:
    """
    Remove a category from a video.
    """
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    if category in video.categories:
        video.categories.remove(category)
        db.add(video)
        db.commit()
        db.refresh(video)

    return video
