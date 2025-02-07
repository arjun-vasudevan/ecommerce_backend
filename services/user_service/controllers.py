from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from typing import Annotated

from services.auth_utils import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from services.database import get_session
from services.user_service.models import User
from services.user_service.schemas import UserCreate, UserBase, Role


ACCESS_TOKEN_EXPIRE_MINUTES = 30
user_router = APIRouter(prefix="/api/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SessionDep = Annotated[Session, Depends(get_session)]


def get_user(db, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: SessionDep) -> UserBase:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(db, username)

    if user is None:
        raise credentials_exception
    elif not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    return UserBase(
        username=user.username, name=user.name, role=user.role, is_active=user.is_active
    )


async def get_current_admin(current_user: Annotated[UserBase, Depends(get_current_user)]) -> UserBase:
    if current_user.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user


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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

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
        data={"sub": db_user.username, "role": db_user.role, "id": db_user.id},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/profile", response_model=UserBase)
async def profile(current_user: Annotated[UserBase, Depends(get_current_user)]):
    return current_user
