from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import Optional, Annotated

app = FastAPI()


# Form(...) -> 필수값일 때 사용 요즘에는 사용 x
# Form은 하나씩 쓰고 json일 때만 pydantic model 사용
@app.post("/login")
async def login(username: str = Form(),
                email: str = Form(),
                country: Annotated[str, Form()] = None):
    return {"username": username, "email": email, "country": country}