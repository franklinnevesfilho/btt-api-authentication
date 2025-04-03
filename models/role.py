from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class RoleBase(SQLModel):
    name: str = Field(default=None)

class Role(RoleBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

class RolePublic(RoleBase):
    id: UUID

class RoleCreate(RoleBase):
    pass

class RoleUpdate(SQLModel):
    name: str | None = None