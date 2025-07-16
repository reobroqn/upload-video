from sqlalchemy import Column, ForeignKey, Integer, Table

from app.core.database import Base

video_category_association = Table(
    "video_category_association",
    Base.metadata,
    Column("video_id", Integer, ForeignKey("videos.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
)
