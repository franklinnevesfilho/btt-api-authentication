from uuid import UUID, uuid4
from pydantic import EmailStr
from .task import TaskPublic
from sqlmodel import SQLModel, Field, String

class UserBase(SQLModel):
    name: str = Field(default=None)
    email: EmailStr = Field(unique=True, index=True, nullable=False)

class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str = Field()

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    id: UUID

class UserTasks(UserPublic):
    tasks: list[TaskPublic]

class UserUpdate(SQLModel):
    name: str | None = None 
    email: EmailStr | None = None
    password: str | None = None

