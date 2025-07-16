from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Category(Base):
    """
    SQLAlchemy model representing a category for videos.
    """

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"
