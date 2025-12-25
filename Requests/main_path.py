from fastapi import FastAPI
from enum import Enum

app = FastAPI()

@app.get("/items/all")
async def get_items():
    return {"message": "all_items"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}