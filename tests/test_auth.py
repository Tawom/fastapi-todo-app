import pytest
from fastapi import status

def test_register_user(client):
    """Test user registration"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass123",
        "role": "user"
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data
    assert "password" not in data  # Password should never be returned

def test_register_duplicate_email(client):
    """Test registration with existing email fails"""
    # First registration
    user_data = {
        "email": "duplicate@example.com",
        "username": "user1",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass123",
        "role": "user"
    }
    client.post("/auth/register", json=user_data)

    # Second registration with same email
    user_data["username"] = "user2"  # Different username
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response.json()["detail"]

def test_login_success(client):
    """Test successful login returns token"""
    # First create a user
    user_data = {
        "email": "login@example.com",
        "username": "loginuser",
        "first_name": "Login",
        "last_name": "Test",
        "password": "testpass123",
        "role": "user"
    }
    client.post("/auth/register", json=user_data)

    # Then login
    response = client.post(
        "/auth/login",
        data={"username": "loginuser", "password": "testpass123"}
    )
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data

def test_login_wrong_password(client):
    """Test login with wrong password fails"""
    # Create user
    user_data = {
        "email": "wrongpass@example.com",
        "username": "wrongpass",
        "first_name": "Wrong",
        "last_name": "Pass",
        "password": "correctpass",
        "role": "user"
    }
    client.post("/auth/register", json=user_data)

    # Try wrong password
    response = client.post(
        "/auth/login",
        data={"username": "wrongpass", "password": "wrongpass"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_user(client):
    """Test getting current user with valid token"""
    # Register and login
    user_data = {
        "email": "current@example.com",
        "username": "currentuser",
        "first_name": "Current",
        "last_name": "User",
        "password": "testpass123",
        "role": "user"
    }
    client.post("/auth/register", json=user_data)

    login_resp = client.post(
        "/auth/login",
        data={"username": "currentuser", "password": "testpass123"}
    )
    token = login_resp.json()["access_token"]

    # Get current user
    response = client.get(
        "/auth/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "currentuser"