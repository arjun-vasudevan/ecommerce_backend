from enum import Enum
from pydantic import BaseModel


class Role(str, Enum):
    admin = "admin"
    user = "user"


class UserBase(BaseModel):
    username: str
    name: str | None = None
    role: Role
    is_active: bool = True


class UserCreate(BaseModel):
    username: str
    password: str
    name: str | None = None
