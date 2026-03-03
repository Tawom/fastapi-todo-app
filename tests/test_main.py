from fastapi.testclient import TestClient

def test_root_endpoint(client):
    """Test the root endpoint returns welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Welcome" in response.json()["message"]

def test_ping_endpoint(client):
    """Test the ping endpoint returns pong"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}