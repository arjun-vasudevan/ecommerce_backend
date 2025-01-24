from fastapi import FastAPI

from services.user_service.main import user_router

app = FastAPI()

app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "Welcome"}
