from enum import Enum
from fastapi import FastAPI
import uvicorn

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/")
def home():
    return {"message": "TheQuietBuilder's first API"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW! "}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "leCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)