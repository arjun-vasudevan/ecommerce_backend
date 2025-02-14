from contextlib import asynccontextmanager
from fastapi import FastAPI
from services.database import setup_database
from services.user_service.controllers import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_database("user_service")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "Welcome"}
