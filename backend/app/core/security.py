"""
Security utilities for authentication and authorization.

This module provides functions for password hashing, JWT token creation and validation,
and other security-related operations used throughout the application.
"""

from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.

    Args:
        plain_password: The plain text password to verify
        hashed_password: The hashed password to verify against

    Returns:
        bool: True if the password matches the hash, False otherwise

    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a secure hash from a password.

    Args:
        password: The plain text password to hash

    Returns:
        str: The hashed password

    """
    return pwd_context.hash(password)


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """
    Create a JWT access token.

    Args:
        data: The data to encode in the token (usually contains user identity)
        expires_delta: Optional timedelta for token expiration. Defaults to 15 minutes.

    Returns:
        str: The encoded JWT token

    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict[str, Any] | None:
    """
    Decode and verify a JWT token.

    This function verifies the token's signature and expiration time.
    If the token is invalid or expired, it returns None.

    Args:
        token: The JWT token to decode and verify

    Returns:
        Optional[Dict[str, Any]]: The decoded token payload if valid,
        None if the token is invalid or expired

    Example:
        ```python
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        payload = decode_token(token)
        if payload:
            username = payload.get("sub")
        ```

    """
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
