import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Dict, Generator

Base = declarative_base()

engines: Dict[str, Engine] = {}
session_makers: Dict[str, sessionmaker] = {}


def _get_database_url(service_name: str) -> str:
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DB = os.getenv(f"{service_name.upper()}_POSTGRES_DB")
    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


def get_db_engine(service_name: str, *args, **kwargs) -> Engine:
    if service_name in engines:
        return engines[service_name]

    database_url = _get_database_url(service_name)
    engines[service_name] = create_engine(database_url, *args, **kwargs)

    return engines[service_name]


def setup_database(service_name: str) -> None:
    engine = get_db_engine(service_name, pool_size=10, max_overflow=20)

    session_makers[service_name] = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    Base.metadata.create_all(bind=engine)


def get_session(service_name: str) -> Generator[sessionmaker, None, None]:
    if service_name not in session_makers:
        setup_database(service_name)

    db = session_makers[service_name]()

    try:
        yield db
    finally:
        db.close()


def get_user_session() -> Generator[sessionmaker, None, None]:
    yield from get_session("user_service")


def get_cart_session() -> Generator[sessionmaker, None, None]:
    yield from get_session("cart_service")
