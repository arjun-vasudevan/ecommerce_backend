from sqlalchemy import Column, Integer, String, Boolean

from services.user_service.models import Role
from services.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    role = Column(String, default=Role.user)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
