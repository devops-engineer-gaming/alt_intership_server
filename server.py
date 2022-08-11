from lib2to3.pgen2.token import OP
from fastapi import FastAPI, HTTPException
from typing import List
from sqlmodel import create_engine, SQLModel
from sqlmodel import Session
from sqlalchemy import select
from fastapi.middleware.cors import CORSMiddleware
import models, settings

engine = create_engine(settings.DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
def on_startup():
    create_db_and_tables()


## Routing ##

@app.get('/todos', response_model = List)
def get_todos():
        with Session(engine) as session:
            todos = session.exec(select(models.Todo)).all()
            return [todo.Todo for todo in todos]

@app.post("/todos/")
def create_hero(todo: models.Todo):
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

@app.post("/todos/{todo_id}")
def update_hero(todo_id: int, todo: models.TodoUpdate):
    with Session(engine) as session:
        db_todo = session.get(models.Todo, todo_id)
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo_data = todo.dict(exclude_unset=True)
        for key, value in todo_data.items():
            setattr(db_todo, key, value)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo


@app.delete("/todos/{todo_id}")
def delete_hero(todo_id: int):
    with Session(engine) as session:
        todo = session.get(models.Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        session.delete(todo)
        session.commit()
        return {"ok": True}