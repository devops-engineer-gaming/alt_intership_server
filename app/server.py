from lib2to3.pgen2.token import OP
from fastapi import FastAPI, HTTPException
from typing import List
from sqlmodel import create_engine, SQLModel
from sqlmodel import Session
from sqlalchemy import select, text
from fastapi.middleware.cors import CORSMiddleware
import models, settings
import  subprocess

engine = create_engine(settings.DATABASE_URL)

'''
def create_db_and_tables():
   with Session(engine) as session:
      statement = text("""
      CREATE TABLE IF NOT EXISTS public.todo
(
    title character varying COLLATE pg_catalog."default",
    description character varying COLLATE pg_catalog."default",
    id serial primary key NOT NULL 
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.todo
    OWNER to postgres_lyagushka;""")
      session.execute(statement)
      session.commit()
'''

def create_db_and_tables():
    subprocess.run(["alembic","upgrade","47de46f187a3"])
    with Session(engine) as session:
        session.commit()

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
    print(settings.DATABASE_URL)


## Routing ##

@app.get('/api/todos', response_model = List)
def get_todos():
        with Session(engine) as session:
            todos = session.exec(select(models.Todos)).all()
            return [todo.Todos for todo in todos]

@app.post("/api/todos/")
def create_todo(todos: models.Todos):
    with Session(engine) as session:
        session.add(todos)
        session.commit()
        session.refresh(todos)
        return todos

@app.patch("/api/todos/{todo_id}")
def update_todo(todo_id: int, todo: models.TodosUpdate):
    with Session(engine) as session:
        db_todo = session.get(models.Todos, todo_id)
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo_data = todo.dict(exclude_unset=True)
        for key, value in todo_data.items():
            setattr(db_todo, key, value)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo


@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(models.Todos, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        session.delete(todo)
        session.commit()
        return {"ok": True}