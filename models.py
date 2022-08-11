from typing import Optional
from sqlmodel import SQLModel, Field

class TodoBase(SQLModel):
    title: Optional[str] 
    description: Optional[str]

class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class TodoCreate(TodoBase):
    pass


class TodoRead(TodoBase):
    id: int


class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None