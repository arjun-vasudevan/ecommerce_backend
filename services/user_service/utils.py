from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from typing import Annotated

import jwt
import os

from services.user_service.models import UserBase, Role
from services.user_service.schemas import User
from services.database import get_session

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SessionDep = Annotated[Session, Depends(get_session)]


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str):
    return pwd_context.hash(password)


def get_user(db, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
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
        raise HTTPException(status_code=400, detail="Inactive user")

    return UserBase(
        username=user.username, name=user.name, role=user.role, is_active=user.is_active
    )


async def get_current_admin(current_user: Annotated[UserBase, Depends(get_current_user)]) -> UserBase:
    if current_user.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user
