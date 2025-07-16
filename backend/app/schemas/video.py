from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.category import CategoryInDB
from app.schemas.tag import TagInDB


class VideoBase(BaseModel):
    """
    Base schema for video data.
    """

    title: str = Field(..., description="Title of the video")
    description: str | None = Field(None, description="Description of the video")


class VideoCreate(VideoBase):
    """
    Schema for creating a new video.
    """

    file_name: str = Field(..., description="Original file name of the video")
    file_size: float = Field(..., description="Size of the video file in bytes")
    mime_type: str = Field(..., description="MIME type of the video file")


class VideoInDB(VideoBase):
    """
    Schema for video data as stored in the database.
    """

    id: int = Field(..., description="Primary key")
    file_key: str = Field(..., description="S3 object key for the video file")
    created_at: datetime = Field(
        ..., description="Timestamp when the video record was created"
    )
    updated_at: datetime | None = Field(
        None, description="Timestamp when the video record was last updated"
    )
    status: str = Field(..., description="Status of the video processing")
    hls_url: str | None = Field(None, description="URL to the HLS master playlist")
    tags: list[TagInDB] = []
    categories: list[CategoryInDB] = []

    class Config:
        from_attributes = True


class PresignedPost(BaseModel):
    """
    Schema for the presigned POST URL response.
    """

    url: str = Field(..., description="The URL to which the file should be uploaded")
    fields: dict[str, str] = Field(
        ..., description="A dictionary of form fields to include in the POST request"
    )
    video_id: int = Field(
        ..., description="The ID of the video record created in the database"
    )


class VideoUploadComplete(BaseModel):
    """
    Schema for confirming video upload completion.
    """

    video_id: int = Field(..., description="The ID of the video that has been uploaded")
    status: str = Field("completed", description="Status of the upload")
