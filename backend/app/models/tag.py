from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Tag(Base):
    """
    SQLAlchemy model representing a tag for videos.
    """

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, name='{self.name}')>"
