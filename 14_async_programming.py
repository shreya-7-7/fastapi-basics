import time
from fastapi import FastAPI 
import asyncio   # async programming

app = FastAPI()

@app.get("/")
async def home():
    await asyncio.sleep(3)
    return {
        "message":"Async API"
    }

# Synchronous prograamming
# def task():
#     time.sleep(3)
#     return "Done"


#   Asynchronous Programming
# async def task():
#     await asyncio.sleep(3)
#     return "Done"