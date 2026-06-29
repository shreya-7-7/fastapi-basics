from sqlalchemy import create_engine
from sqlalchemy.orm import identity, sessionmaker, declarative_base, Session
from sqlalchemy import Column,Integer,String
from fastapi import FastAPI,Depends, HTTPException

app = FastAPI()

#Database URL
DATABASE_URL = "sqlite:///./test.db"

# Engine create (DB connection)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

# Session (For DB Operations)
sessionLocal = sessionmaker(bind=engine)

# Base (For Base Model)
Base = declarative_base()

# Table (Model)
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(String)

# Table create
Base.metadata.create_all(bind=engine)

# Dependency (It will provide DB session)
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.get("/")
# def home(db: Session = Depends(get_db)):
#     return {
#         "message":"DB connected Fine"
#     }


# Create API (Using POST)
@app.post("/todos")
def create_todo(title:str, db: Session = Depends(get_db)):
    todo = Todo(title=title, completed = "False") #object created (initially value is false if there is nothing) 
    db.add(todo) #add to DB
    db.commit() #save to DB
    db.refresh(todo) #to get id of latest data
    return {
        "message":"Todo Created",
        "data":todo
    }


# Read All data
@app.get("/todos")
def get_todos(db:Session = Depends(get_db)):
    todos = db.query(Todo).all()

    return {
        "Total":len(todos),
        "data": todos
    }

# Read One By One data (Through ID)
@app.get("/todos/{todo_id}")
def get_todo(todo_id=int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    return todo 

# Data update
@app.put("/todos/{todo_id}")
def date_todo(todo_id:int, title:str, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    
    todo.title = title

    db.commit()
    db.refresh(todo)

    return {
        "message":"Todo Updated",
        "data":todo
    }