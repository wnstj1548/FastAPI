from typing import Annotated

from fastapi import FastAPI, Path, Query, Form, Depends
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, ValidationError, model_validator
from schemas.item_schema import Item, parse_user_form

app = FastAPI()

@app.put("/items/{item_id}")
async def update_item(item_id: int = Path(...), q: str = Query(...), item: Item=None):
    return {"item_id": item_id, "q": q, "item": item}

@app.put("/items_json/{item_id}")
async def update_item_json(
        item_id: int = Path(..., gt=0, title="The id of the Item to get"),
        q1: str = Query(None, max_length=50),
        q2: str = Query(None, min_length=3),
        item: Item = None
):
    return {"item_id": item_id, "q1": q1, "q2": q2, "item": item}

@app.post("/items_form/{item_id}")
async def update_item_form(
        item_id: int = Path(..., gt=0, title="The id of the Item to get"),
        q: str = Query(None, max_length=50),
        name: str = Form(..., min_length=2, max_length=50),
        description: Annotated[str, Form(max_length=500)] = None,
        price: float = Form(..., gt=0),
        tax: Annotated[float, Form()] = None
):
    return {"item_id": item_id, "q": q, "name": name, "description": description, "price": price, "tax": tax}

@app.post("/items_form_01/{item_id}")
async def update_item_form_01(
        item_id: int = Path(..., gt=0, title="The id of the Item to get"),
        q: str = Query(None, max_length=50),
        name: str = Form(..., min_length=2, max_length=50),
        description: Annotated[str, Form(max_length=500)] = None,
        price: float = Form(..., gt=0),
        tax: Annotated[float, Form()] = None
):
    try:
        item = Item(name=name, description=description, price=price, tax=tax)
        return item
    except ValidationError as e:
        raise RequestValidationError(e.errors())

@app.post("/items_form_02/{item_id}")
async def update_item_form_02(
        item_id: int = Path(..., gt=0, title="The id of the Item to get"),
        q: str = Query(None, max_length=50),
        item: Item = Depends(parse_user_form),
):
    return {"item_id": item_id, "q": q, "item": item}