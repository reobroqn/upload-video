from sqlalchemy import Column, DateTime, Enum, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.schemas.video_status import VideoStatus
from sqlalchemy.sql import func

from app.core.database import Base


class Video(Base):
    """
    SQLAlchemy model representing a video in the system.

    Attributes:
        id: Primary key, auto-incrementing integer
        title: Title of the video
        description: Description of the video
        file_key: S3 object key for the video file
        file_size: Size of the video file in bytes
        mime_type: MIME type of the video file
        created_at: Timestamp when the video record was created
        updated_at: Timestamp when the video record was last updated

    """

    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True, doc="Primary key identifier")
    title = Column(String, nullable=False, doc="Title of the video")
    description = Column(String, nullable=True, doc="Description of the video")
    file_key = Column(
        String, unique=True, nullable=False, doc="S3 object key for the video file"
    )
    file_size = Column(Float, nullable=False, doc="Size of the video file in bytes")
    mime_type = Column(String, nullable=False, doc="MIME type of the video file")
    status = Column(
        Enum(VideoStatus),
        default=VideoStatus.PENDING,
        nullable=False,
        doc="Status of the video processing",
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        doc="Timestamp when the video record was created",
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
        doc="Timestamp when the video record was last updated",
    )
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, doc="The ID of the user who owns the video")
    owner = relationship("User", back_populates="videos")

    def __repr__(self) -> str:
        """
        Return a string representation of the Video instance.
        """
        return (
            f"<Video(id={self.id}, title='{self.title}', file_key='{self.file_key}')>"
        )
