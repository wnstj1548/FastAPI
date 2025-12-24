from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Annotated
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory ="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=-1
)

class Item(BaseModel):
    name: str
    description: str
    #description: Optional[str] = None
    price: float
    tax: float | None = None
    #tax: Optional[float] = None

class User(BaseModel):
    username: str
    full_name: str | None = None

@app.post("/items")
async def create_item(item: Item):
    print("###### item_type:", type(item))
    print("###### item:", item)
    return item

@app.post("/items_tax/")
async def create_item_tax(item: Item):
    item_dict = item.model_dump()
    print("#### item_dict:", item_dict)
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    print("#### result:", result)
    return result

@app.put("/items_mt/{item_id}")
async def update_item_mt(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results