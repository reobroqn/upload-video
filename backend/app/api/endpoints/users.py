from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps.deps import get_current_active_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserInDB, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserInDB)
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
) -> UserInDB:
    """
    Get the current authenticated user's profile.

    This endpoint returns the profile information of the currently authenticated
    user. The user must provide a valid JWT token in the Authorization header.

    Args:
        current_user: The currently authenticated user (from JWT token)

    Returns:
        UserInDB: The user's profile information

    """
    return current_user


@router.patch("/me", response_model=UserInDB)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> UserInDB:
    """
    Update the current authenticated user's profile.

    This endpoint allows the currently authenticated user to update their
    profile information, including full name and avatar URL.

    Args:
        user_update: User update data including full_name and avatar_url
        current_user: The currently authenticated user (from JWT token)
        db: Database session dependency

    Returns:
        UserInDB: The updated user object

    Raises:
        HTTPException: 400 if username or email is already taken by another user

    """
    if user_update.username and user_update.username != current_user.username:
        existing_user = db.query(User).filter(User.username == user_update.username).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

    if user_update.email and user_update.email != current_user.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    for field, value in user_update.model_dump(exclude_unset=True).items():
        if field == "password":
            # Password hashing should be handled separately if needed,
            # or a dedicated endpoint for password change.
            # For now, we are not allowing password update via this endpoint.
            continue
        setattr(current_user, field, value)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return current_user
