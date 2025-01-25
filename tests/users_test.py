import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from services.database import Base, get_session
from services.main import app
from services.user_service.models import User

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Use test database
def override_get_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)


@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_register_user(setup_database):
    response = client.post(
        "/api/users/register",
        json={"username": "testuser0", "password": "testpassword", "name": "Test User 0"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Verify the user is in the database
    db = TestingSessionLocal()
    user = db.query(User).filter(User.username == "testuser0").first()
    assert user is not None
    assert user.username == "testuser0"
    assert user.name == "Test User 0"


def test_registered_user_duplicate(setup_database):
    response = client.post(
        "/api/users/register",
        json={"username": "testuser1", "password": "testpassword", "name": "Test User 1"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Try to register the same user again
    response = client.post(
        "/api/users/register",
        json={"username": "testuser1", "password": "testpassword"}
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Username already registered"

    # Ensure only one user is in the database
    db = TestingSessionLocal()
    users = db.query(User).all()
    assert len(users) == 1


def test_get_profile(setup_database):
    response = client.post(
        "/api/users/register",
        json={"username": "testuser2", "password": "testpassword", "name": "Test User 2"}
    )

    assert response.status_code == 200
    data = response.json()
    access_token = data["access_token"]

    # Get the profile
    response = client.get(
        "/api/users/profile",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser2"
    assert data["name"] == "Test User 2"