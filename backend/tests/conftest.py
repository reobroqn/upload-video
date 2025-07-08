from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import Base, get_db
from app.main import app

# Test database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"

# Create a test database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,  # Set to True for SQL query logging
)

# Create a test session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database() -> Generator[None, None, None]:
    """
    Set up the test database with all tables before tests and clean up afterward.

    This fixture runs once per test session and ensures a clean database state.
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # This yield allows tests to run
    yield

    # Clean up after all tests complete
    Base.metadata.drop_all(bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    """
    Override the database dependency for testing.

    Yields:
        Session: A database session for testing

    Note:
        This function is used to override the get_db dependency in the FastAPI app.

    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the database dependency in the FastAPI app
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """
    Create a test client for making HTTP requests to the FastAPI application.

    Yields:
        TestClient: A test client instance

    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_user(client: TestClient) -> dict[str, str]:
    """
    Create and return a test user for authentication tests.

    Args:
        client: Test client for making HTTP requests

    Returns:
        Dict containing test user's email, username, full_name, and password.

    """
    user_data = {
        "email": "testuser@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "testpassword123",  # Using a stronger password for testing
    }

    # Create a test user by making a request to the registration endpoint
    response = client.post("/api/v1/auth/register", json=user_data)

    # Ensure the user was created successfully
    assert response.status_code == 200, "Failed to create test user"

    return user_data
