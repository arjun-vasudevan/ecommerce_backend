import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


def get_database_url():
    load_dotenv(os.path.join(os.path.dirname(__file__), "user_service", ".env"))
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


def get_db_engine(database_url, *args, **kwargs):
    return create_engine(database_url, *args, **kwargs)


engine = None
SessionLocal = None


def setup_database():
    global engine, SessionLocal
    if engine is None:
        database_url = get_database_url()
        engine = get_db_engine(database_url, pool_size=10, max_overflow=20)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    if SessionLocal is None:
        setup_database()

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
