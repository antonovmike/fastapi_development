from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Welcome"}


def test_create_posts():
    test_data = {
        "title": "demo",
        "content": "demo"
    }
    
    response = client.post("/posts", json=test_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert "title" in response.json()
    assert "content" in response.json()
