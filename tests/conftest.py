from pytest import fixture
from sqlalchemy import create_engine
from unittest.mock import patch

from services.database import Base, get_session


# Test database
test_engine = create_engine(
    "sqlite:///test.db", connect_args={"check_same_thread": False}
)


@fixture()
def db():
    session = next(get_session())
    yield session
    session.close()


@fixture(scope="session", autouse=True)
def mock_postgres_engine():
    with patch("services.database.get_db_engine") as mock_get_db_engine:
        mock_get_db_engine.return_value = test_engine

        yield


@fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
