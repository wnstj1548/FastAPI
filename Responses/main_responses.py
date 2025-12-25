from fastapi import FastAPI, Form, status
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
    RedirectResponse
)
from pydantic import BaseModel

app = FastAPI()

@app.get("/resp_json/{item_id}", response_class=JSONResponse)
async def response_json(item_id: int, q: str | None = None):
    return JSONResponse(content={"message" : "Hello World",
                                 "item_id": item_id,
                                 "q": q},
                        status_code=status.HTTP_200_OK)

@app.get("/resp_html/{item_id}", response_class=HTMLResponse)
async def response_html(item_id: int, item_name: str | None = None):
    html_str = f'''
        <html>
        <body>
            <h2>HTML Response</h2>
            <p>item_id: {item_id}</p>
            <p>item_name: {item_name}</p>
        </body>
        </html>
        '''

    return HTMLResponse(content=html_str, status_code=status.HTTP_200_OK)

@app.get("/redirect")
async def redirect_only(comment: str | None = None):
    print(f"redirect: {comment}")
    return RedirectResponse(url=f"/resp_html/3?item_name={comment}")

@app.post("/create_redirect")
async def create_redirect(item_id: int = Form(), item_name: str = Form()):
    print(f"item_id: {item_id}, item_name: {item_name} has been created")

    return RedirectResponse(url=f"/resp_html/{item_id}?item_name={item_name}", status_code=status.HTTP_302_FOUND)

class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float | None = None

class ItemResp(BaseModel):
    name: str
    description: str
    price_with_tax: float

@app.post("/create_item", response_model=ItemResp, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    if item.tax:
        price_with_tax = item.price + item.tax
    else:
        price_with_tax = item.price

    item_resp = ItemResp(
        name=item.name,
        description=item.description,
        price_with_tax=price_with_tax
    )
    
    return item_resp


