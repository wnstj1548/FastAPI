from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db.database import Base


class Blog(Base):
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    content = Column(String(4000), nullable=False)
    image_loc = Column(String(300), nullable=True)
    modified_dt = Column(DateTime, nullable=False, default=func.now())