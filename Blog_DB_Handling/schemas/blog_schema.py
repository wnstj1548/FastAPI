from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime
from pydantic.dataclasses import dataclass

class BlogInput(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    author: str = Field(..., max_length=100)
    content: str = Field(..., min_length=2, max_length=4000)
    image_loc: Optional[str] = Field(None, max_length=400)

class Blog(BlogInput):
    id: int
    modified_dt: datetime

# default값으로 None을 주는거는 마지막에 위치해야한다. (dataclass 사용할 때만)
@dataclass
class BlogData:
    id: int
    title: str
    author: str
    content: str
    modified_dt: datetime
    image_loc: str | None = None

# 아래는 orm으로 변경
class CreateBlogRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    author: str = Field(..., max_length=100)
    content: str = Field(..., min_length=2, max_length=4000)
    image_loc: Optional[str] = Field(None, max_length=400)

class ReadBlogResponse(BaseModel):
    id: int
    title: str
    author: str
    content: str
    image_loc: Optional[str] = None
    modified_dt: datetime

    class Config:
        from_attributes = True  # ORM → Pydantic 변환 허용