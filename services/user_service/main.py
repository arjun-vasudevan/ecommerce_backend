from contextlib import asynccontextmanager
from fastapi import FastAPI
from services.database import Base, setup_database
from services.user_service.controllers import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_database()
    from services.database import engine

    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "Welcome"}
