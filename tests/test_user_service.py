from fastapi.testclient import TestClient

from services.user_service.main import app
from services.user_service.models import User


client = TestClient(app)


def test_register_user(db):
    response = client.post(
        "/api/users/register",
        json={
            "username": "testuser0",
            "password": "testpassword",
            "name": "Test User 0",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Verify the user is in the database
    user = db.query(User).filter(User.username == "testuser0").first()
    assert user is not None
    assert user.username == "testuser0"
    assert user.name == "Test User 0"


def test_registered_user_duplicate(db):
    response = client.post(
        "/api/users/register",
        json={
            "username": "testuser1",
            "password": "testpassword",
            "name": "Test User 1",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Try to register the same user again
    response = client.post(
        "/api/users/register",
        json={"username": "testuser1", "password": "testpassword"},
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Username already registered"

    # Ensure only one user is in the database
    users = db.query(User).all()
    assert len(users) == 1


def test_get_profile():
    response = client.post(
        "/api/users/register",
        json={
            "username": "testuser2",
            "password": "testpassword",
            "name": "Test User 2",
        },
    )

    assert response.status_code == 200
    data = response.json()
    access_token = data["access_token"]

    # Get the profile
    response = client.get(
        "/api/users/profile", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser2"
    assert data["name"] == "Test User 2"
    assert data["role"] == "user"
