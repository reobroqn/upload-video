from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserInDB

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)) -> UserInDB:
    """
    Register a new user account.

    This endpoint allows users to create a new account by providing their email,
    username, and password. The password will be hashed before storage.

    Args:
        user: User registration data including email, username, and password
        db: Database session dependency

    Returns:
        UserInDB: The newly created user object

    Raises:
        HTTPException: 400 if email or username is already registered

    """
    # Check if user with email already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Check if username is taken
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_active=True,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict[str, str]:
    """
    Authenticate a user and return an access token.

    This endpoint validates the user's credentials and returns a JWT access token
    that can be used for subsequent authenticated requests.

    Args:
        form_data: OAuth2 form data containing username and password
        db: Database session dependency

    Returns:
        dict: A dictionary containing the access token and token type

    Raises:
        HTTPException:
            - 401 if username or password is incorrect
            - 400 if the user account is inactive

    """
    # Find user by username
    user = db.query(User).filter(User.username == form_data.username).first()

    # Check if user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
