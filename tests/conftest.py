import pytest
from sqlalchemy import create_engine
from unittest.mock import patch

from services.database import Base


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

@pytest.fixture(scope="session", autouse=True)
def mock_database_engine():
    with patch("services.database.get_db_engine") as mock_get_db_engine:
        mock_get_db_engine.return_value = engine
        yield


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
