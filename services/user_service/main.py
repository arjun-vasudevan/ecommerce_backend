from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from services.user_service.models import UserCreate, UserBase, Role
from services.user_service.schemas import User
from services.user_service.utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_user,
    hash_password,
    SessionDep,
)

user_router = APIRouter(prefix="/api/users", tags=["users"])


# Receives username and password and returns an access token
@user_router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: SessionDep) -> dict:
    user = authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


# Receives username, password, and an option name and registers a new user
@user_router.post("/register")
async def register(new_user: UserCreate, db: SessionDep):
    user = get_user(db, new_user.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = User(
        username=new_user.username,
        name=new_user.name,
        hashed_password=hash_password(new_user.password),
        role=Role.user,
        is_active=True,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.username, "role": Role.user},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/profile", response_model=UserBase)
async def profile(current_user: Annotated[UserBase, Depends(get_current_user)]):
    return current_user
