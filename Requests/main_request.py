from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/items")
async def read_item(request: Request):
    client_host = request.client.host
    headers= request.headers
    query_params = request.query_params
    url = request.url
    path_params = request.path_params
    http_method = request.method

    return {
        "client_host": client_host,
        "headers": headers,
        "query_params": query_params,
        "url": url,
        "path_params": path_params,
        "http_method": http_method
    }

@app.post("/items_json")
async def create_item_json(request: Request):
    data = await request.json()
    print("received_data:", data)
    return {"received_data": data}

@app.post("/items_form")
async def create_item_json(request: Request):
    data = await request.form()
    print("received_data:", data)
    return {"received_data": data}