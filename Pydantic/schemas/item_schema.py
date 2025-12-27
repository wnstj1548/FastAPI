from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError, BaseModel, model_validator, Field
from fastapi import Form
from typing import Annotated

class Item(BaseModel):
    name: str = Field(..., min_length=2, max_length=10)
    description: str = Field(None, max_length=500)
    price: float = Field(..., ge=0)
    tax: float = None

    @model_validator(mode = 'after')
    def tax_must_be_less_than_price(cls, values):
        if values.price < values.tax:
            raise ValueError("tax must be less than price")
        return values

def parse_user_form(
        name: str = Form(..., min_length=2, max_length=50),
        description: Annotated[str, Form(..., max_length=50)] = None,
        price: float = Form(..., ge=0),
        tax: Annotated[float, Form()] = None,
) -> Item:
    try:
        item = Item(name=name, description=description, price=price, tax=tax)
        return item
    except ValidationError as e:
        raise RequestValidationError(e.errors())