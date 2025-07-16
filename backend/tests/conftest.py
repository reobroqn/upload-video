from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import Base, get_db
from app.main import app
from app.models.user import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db() -> Generator[Session, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


@pytest.fixture(scope="session")
def client(db: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def test_user_data() -> dict[str, str]:
    return {
        "email": "testuser@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "testpassword123",
    }


@pytest.fixture(scope="session")
def test_user(
    client: TestClient, db: Session, test_user_data: dict[str, str]
) -> tuple[User, str]:
    user = db.query(User).filter(User.email == test_user_data["email"]).first()
    if user is None:
        response = client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 201, (
            f"Failed to create test user: {response.text}"
        )
        db.commit()  # Explicitly commit the user to the database
        user = db.query(User).filter(User.email == test_user_data["email"]).first()
        assert user is not None
    return user, test_user_data["password"]


@pytest.fixture
def user_token_headers(
    client: TestClient, test_user: tuple[User, str]
) -> dict[str, str]:
    user, password = test_user
    login_data = {
        "username": user.username,
        "password": password,
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200, f"Failed to log in test user: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
