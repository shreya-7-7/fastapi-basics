from sqlalchemy import create_engine
from sqlalchemy.orm import identity, sessionmaker, declarative_base, Session
from sqlalchemy import Column,Integer,String
from fastapi import FastAPI,Depends

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

sessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home(db: Session = Depends(get_db)):
    return {
        "message":"DB connected Fine"
    }
