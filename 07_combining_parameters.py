from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# FIX: Changed list name from 'user' to 'users' to avoid naming conflicts
users = []

class User(BaseModel):
    name: str
    age: int

@app.post("/users")
def create_user(user: User):
    users.append(user) # FIX: Appending to the 'users' list
    return {
        "message": "User Created",
        "data": user
    }

@app.put("/users/{user_id}")
def updated_user(user_id: int, user: User, notify: bool = False):
    if user_id < len(users): # FIX: Checking length of 'users' list
        users[user_id] = user # FIX: Updating the 'users' list

        return {
            "message": "User Updated",
            "notify": notify,
            "data": user
        }
    return {
        "error": "user not found"
    }