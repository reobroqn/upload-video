"""
Dependency injection utilities for FastAPI endpoints.

This module provides dependency functions for handling authentication and authorization
in the FastAPI application, including JWT token validation and user role verification.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.schemas.user import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Retrieve the current authenticated user from the JWT token.

    Args:
        db: Database session dependency
        token: JWT token from the Authorization header

    Returns:
        User: The authenticated user

    Raises:
        HTTPException: 401 if the token is invalid or the user doesn't exist

    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        if not payload:
            raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Verify that the current user is active.

    This function checks if the current user is active and raises an HTTPException if
    the user is inactive.

    Args:
        current_user: The authenticated user from get_current_user

    Returns:
        User: The active user

    Raises:
        HTTPException: 400 if the user is inactive

    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Verify that the current user is an active superuser.

    Args:
        current_user: The authenticated user from get_current_user

    Returns:
        User: The superuser

    Raises:
        HTTPException: 403 if the user is not a superuser

    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
