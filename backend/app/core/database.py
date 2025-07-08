"""
Database configuration and session management.

This module provides database connection setup, session management, and
initialization utilities for the application's SQLAlchemy ORM.
"""

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from .config import settings

# Create database engine using the database URL from settings
SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting a database session.

    Yields:
        Session: A SQLAlchemy database session

    Example:
        ```python
        with get_db() as db:
            # Use the database session
            users = db.query(User).all()
        ```

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize the database with all defined models.

    This function performs the following actions:
    1. Imports all SQLAlchemy models to ensure they are registered with the Base metadata
    2. Creates all database tables that don't already exist

    Note:
        This function should be called during application startup, typically in the
        application factory or startup event handler.

    Example:
        ```python
        # In main.py or app/__init__.py
        from .core.database import init_db

        def create_app():
            app = FastAPI()
            init_db()
            return app
        ```

    """
    # Import all models here to ensure they are registered with SQLAlchemy
    from app.models.user import User  # noqa: F401

    # Create all tables
    Base.metadata.create_all(bind=engine)
