import uuid
from datetime import datetime, timezone
from enum import Enum

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import table
from sqlmodel import Field, Session, SQLModel, create_engine, select


class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"


# class User(SQLModel):
#     id: int | None = Field(default=None, primary_key=True)
#     username: str = Field(unique=True)
#     email: str | None = Field(default=None, unique=True, index=True)
#     hashed_password: str
#     name: str
#     status: UserStatus = Field(default=UserStatus.active)
#     registered_at: str = Field(default_factory=lambda: str(datetime.now()))

class UserBase(SQLModel):
    username: str
    email: str | None = None
    name: str
    status: UserStatus | None = UserStatus.active


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    hashed_password: str | None = None
    status: UserStatus | None = None


class UserPersistence(UserBase, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    public_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str = Field(unique=True, index=True)
    email: str | None = Field(default=None, unique=True, index=True)
    hashed_password: str
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserInternalCredentials(SQLModel):
    username: str
    hashed_password: str
    status: UserStatus


class UserLogin(SQLModel):
    username: str
    password: str

class LoginResponse(SQLModel):
    access_token: str

class UserPublic(UserBase):
    public_id: str
    registered_at: datetime
