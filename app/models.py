from typing import Optional
from sqlmodel import SQLModel, Field

class TodosBase(SQLModel):
    title: Optional[str] 
    description: Optional[str]

class Todos(TodosBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class TodosCreate(TodosBase):
    pass


class TodoRead(TodosBase):
    id: int


class TodosUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None