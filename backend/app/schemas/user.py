from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Base schema for user data.

    Attributes:
        email: User's email address
        username: User's username (3-50 characters)
        full_name: User's full name (optional)

    """

    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="User's username (3-50 characters)",
    )
    full_name: str | None = Field(None, description="User's full name (optional)")


class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Inherits all fields from UserBase and adds password field.

    Attributes:
        password: User's password (minimum 8 characters)

    """

    password: str = Field(
        ..., min_length=8, description="User's password (minimum 8 characters)"
    )


class UserUpdate(BaseModel):
    """
    Schema for updating an existing user's information.

    All fields are optional, allowing partial updates.

    Attributes:
        email: New email address (optional)
        username: New username (3-50 characters, optional)
        full_name: New full name (optional)
        password: New password (minimum 8 characters, optional)

    """

    email: EmailStr | None = Field(None, description="New email address (optional)")
    username: str | None = Field(
        None,
        min_length=3,
        max_length=50,
        description="New username (3-50 characters, optional)",
    )
    full_name: str | None = Field(None, description="New full name (optional)")
    avatar_url: str | None = Field(None, description="URL to user's avatar image (optional)")
    password: str | None = Field(
        None, min_length=8, description="New password (minimum 8 characters, optional)"
    )


class UserInDB(UserBase):
    """
    Schema for user data as stored in the database.

    Inherits from UserBase and adds database-specific fields.

    Attributes:
        id: Primary key
        is_active: Whether the user account is active
        is_superuser: Whether the user has superuser privileges
        created_at: Timestamp when the user was created
        updated_at: Timestamp when the user was last updated (optional)

    """

    id: int = Field(..., description="Primary key")
    is_active: bool = Field(..., description="Whether the user account is active")
    is_superuser: bool = Field(
        ..., description="Whether the user has superuser privileges"
    )
    created_at: datetime = Field(..., description="Timestamp when the user was created")
    updated_at: datetime | None = Field(
        None, description="Timestamp when the user was last updated (optional)"
    )

    class Config:
        """Pydantic config for UserInDB."""

        from_attributes = True


class Token(BaseModel):
    """
    Schema for JWT token response.

    Attributes:
        access_token: The JWT access token
        token_type: The token type (default: "bearer")

    """

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type (default: bearer)")


class TokenData(BaseModel):
    """
    Schema for token payload data.

    Attributes:
        username: Username extracted from the token (optional)

    """

    username: str | None = Field(
        None, description="Username extracted from the token (optional)"
    )
