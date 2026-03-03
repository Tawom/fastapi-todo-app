import pytest
from fastapi import status

@pytest.fixture
def auth_client(client):
    """Create a client with authenticated user"""
    # Register user
    user_data = {
        "email": "todo@example.com",
        "username": "todouser",
        "first_name": "Todo",
        "last_name": "Tester",
        "password": "testpass123",
        "role": "user"
    }
    client.post("/auth/register", json=user_data)

    # Login
    login_resp = client.post(
        "/auth/login",
        data={"username": "todouser", "password": "testpass123"}
    )
    token = login_resp.json()["access_token"]

    # Add auth header to all requests
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

def test_create_todo(auth_client):
    """Test creating a todo"""
    todo_data = {
        "title": "Learn pytest",
        "description": "Write tests for FastAPI",
        "completed": False
    }

    response = auth_client.post("/todos/", json=todo_data)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data["title"] == todo_data["title"]
    assert data["description"] == todo_data["description"]
    assert data["completed"] == todo_data["completed"]
    assert "id" in data
    assert "owner_id" in data
    assert "created_at" in data

def test_get_todos(auth_client):
    """Test listing todos"""
    # Create a todo first
    todo_data = {"title": "Test todo", "description": "Test", "completed": False}
    auth_client.post("/todos/", json=todo_data)

    # Get all todos
    response = auth_client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK

    todos = response.json()
    assert isinstance(todos, list)
    assert len(todos) >= 1
    assert todos[0]["title"] == todo_data["title"]

def test_get_single_todo(auth_client):
    """Test getting a specific todo"""
    # Create a todo
    todo_data = {"title": "Single todo", "description": "Get me", "completed": False}
    create_resp = auth_client.post("/todos/", json=todo_data)
    todo_id = create_resp.json()["id"]

    # Get the todo
    response = auth_client.get(f"/todos/{todo_id}")
    assert response.status_code == status.HTTP_200_OK

    todo = response.json()
    assert todo["id"] == todo_id
    assert todo["title"] == todo_data["title"]

def test_update_todo(auth_client):
    """Test updating a todo"""
    # Create a todo
    todo_data = {"title": "Update me", "description": "Original", "completed": False}
    create_resp = auth_client.post("/todos/", json=todo_data)
    todo_id = create_resp.json()["id"]

    # Update the todo
    update_data = {"title": "Updated", "completed": True}
    response = auth_client.put(f"/todos/{todo_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK

    updated = response.json()
    assert updated["title"] == "Updated"
    assert updated["completed"] is True
    assert updated["description"] == "Original"  # Unchanged field

def test_delete_todo(auth_client):
    """Test deleting a todo"""
    # Create a todo
    todo_data = {"title": "Delete me", "description": "Gone soon", "completed": False}
    create_resp = auth_client.post("/todos/", json=todo_data)
    todo_id = create_resp.json()["id"]

    # Delete it
    delete_resp = auth_client.delete(f"/todos/{todo_id}")
    assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

    # Verify it's gone
    get_resp = auth_client.get(f"/todos/{todo_id}")
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND