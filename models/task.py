from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field

class TaskBase(SQLModel):
    description: str = Field(default="")
    is_complete: bool = Field(default=False)
    
class Task(TaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)

class TaskCreate(TaskBase):
    pass

class TaskPublic(TaskBase):
    id: UUID

class TaskUpdate(SQLModel):
    description: str | None = None
    is_complete: bool | None = None

