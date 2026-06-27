from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# class User(BaseModel):
#     name:str
#     age:int
#     email:str

# @app.post("/Create_user")
# def create_user(user:User):
#     return{
#         "message":"User Created",
#         "data":user
#     }

class Address(BaseModel):
    city:str
    pincode:int

class User(BaseModel):
    name:str
    age:int
    address:Address

@app.post("/Create_users")
def create_users(user: User):
    return{
        "message":"User Created",
        "User":user
    }
