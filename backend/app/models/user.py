from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    """
    SQLAlchemy model representing a user in the system.

    Attributes:
        id: Primary key, auto-incrementing integer
        email: User's email address (unique, indexed)
        username: User's username (unique, indexed)
        hashed_password: Hashed password using bcrypt
        full_name: User's full name (optional)
        is_active: Whether the user account is active
        is_superuser: Whether the user has superuser privileges
        created_at: Timestamp when the user was created
        updated_at: Timestamp when the user was last updated

    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, doc="Primary key identifier")
    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
        doc="User's email address (must be unique)",
    )
    username = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
        doc="User's username (must be unique)",
    )
    hashed_password = Column(String, nullable=False, doc="Hashed password using bcrypt")
    full_name = Column(String, nullable=True, doc="User's full name (optional)")
    is_active = Column(Boolean, default=True, doc="Whether the user account is active")
    is_superuser = Column(
        Boolean, default=False, doc="Whether the user has superuser privileges"
    )
    avatar_url = Column(String, nullable=True, doc="URL to user's avatar image")
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        doc="Timestamp when the user was created",
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
        doc="Timestamp when the user was last updated",
    )
    videos = relationship("Video", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """
        Return a string representation of the User instance.

        Returns:
            str: A string containing the user's ID, username, and email

        """
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

    def to_dict(self) -> dict:
        """
        Convert the User instance to a dictionary.

        Returns:
            dict: A dictionary containing user attributes

        """
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "avatar_url": self.avatar_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
