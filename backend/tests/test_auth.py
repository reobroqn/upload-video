from typing import Any

from fastapi import status
from fastapi.testclient import TestClient

# Constants
TOKEN_TYPE = "bearer"  # Expected token type in responses


def test_register_user(client: TestClient) -> None:
    """
    Test user registration with valid data.

    Args:
        client: Test client for making HTTP requests

    """
    # Arrange
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "full_name": "New User",
        "password": "TestPassword123!",  # Using a strong password
    }

    # Act
    response = client.post("/api/v1/auth/register", json=user_data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    # Verify response data
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert data["full_name"] == user_data["full_name"]
    assert "hashed_password" not in data  # Password should never be returned
    assert "id" in data  # Should have an ID assigned by the database


def test_register_duplicate_email(
    client: TestClient, test_user: dict[str, Any]
) -> None:
    """
    Test registration with duplicate email.

    Args:
        client: Test client for making HTTP requests
        test_user: Fixture providing a pre-existing test user

    """
    # Arrange - Use same email as test_user but different username
    user_data = {
        "email": test_user["email"],  # Duplicate email
        "username": "differentuser",
        "full_name": "Different User",
        "password": "TestPassword123!",
    }

    # Act
    response = client.post("/api/v1/auth/register", json=user_data)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response.json()["detail"]


def test_login_success(client: TestClient, test_user: dict[str, Any]) -> None:
    """
    Test successful login with correct credentials.

    Args:
        client: Test client for making HTTP requests
        test_user: Fixture providing test user credentials

    """
    # Arrange
    login_data = {"username": test_user["username"], "password": test_user["password"]}
    headers = {"content-type": "application/x-www-form-urlencoded"}

    # Act
    response = client.post(
        "/api/v1/auth/login",
        data=login_data,
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == TOKEN_TYPE
    assert len(data["access_token"]) > 0  # Token should not be empty


def test_login_invalid_credentials(
    client: TestClient, test_user: dict[str, Any]
) -> None:
    """
    Test login with invalid credentials.

    Args:
        client: Test client for making HTTP requests
        test_user: Fixture providing test user credentials

    """
    # Arrange - Use incorrect password
    login_data = {"username": test_user["username"], "password": "WrongPassword123!"}
    headers = {"content-type": "application/x-www-form-urlencoded"}

    # Act
    response = client.post(
        "/api/v1/auth/login",
        data=login_data,
        headers=headers,
    )

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response_data = response.json()
    assert "detail" in response_data
    assert "Incorrect username or password" in response_data["detail"]


def test_protected_route(client: TestClient, test_user: dict[str, Any]) -> None:
    """
    Test accessing a protected route with a valid token.

    Args:
        client: Test client for making HTTP requests
        test_user: Fixture providing test user credentials

    """
    # Arrange - Login to get token
    login_data = {"username": test_user["username"], "password": test_user["password"]}
    headers = {"content-type": "application/x-www-form-urlencoded"}

    # Act - Get access token
    login_response = client.post(
        "/api/v1/auth/login",
        data=login_data,
        headers=headers,
    )
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]

    # Act - Access protected route
    response = client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]
    assert "hashed_password" not in data  # Sensitive data should be excluded


def test_protected_route_unauthorized(client: TestClient) -> None:
    """
    Test accessing a protected route without a token.

    Args:
        client: Test client for making HTTP requests

    """
    # Act - Access protected route without authentication
    response = client.get("/api/v1/users/me")

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response_data = response.json()
    assert "detail" in response_data
    assert "Not authenticated" in response_data["detail"]


def test_protected_route_invalid_token(client: TestClient) -> None:
    """
    Test accessing a protected route with an invalid token.

    Args:
        client: Test client for making HTTP requests

    """
    # Arrange - Use an invalid token
    invalid_token = "this-is-not-a-valid-jwt"

    # Act - Access protected route with the invalid token
    response = client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {invalid_token}"}
    )

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response_data = response.json()
    assert "detail" in response_data
    assert "Could not validate credentials" in response_data["detail"]
