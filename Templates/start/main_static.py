from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

app = FastAPI()

# 1번째 인자는 url path / 2번째 인자는 directory명, 3번째 인자는 url_for등에서 참조하는 이름
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str, q: str | None = None):
    html_name = "item_static.html"
    return templates.TemplateResponse(
        request=request,
        name=html_name,
        context={"id": id, "q_str": q}
    )