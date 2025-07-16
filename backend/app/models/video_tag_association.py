from sqlalchemy import Column, ForeignKey, Integer, Table

from app.core.database import Base

video_tag_association = Table(
    "video_tag_association",
    Base.metadata,
    Column("video_id", Integer, ForeignKey("videos.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)
