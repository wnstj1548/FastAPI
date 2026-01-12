from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from schemas.blog_schema import Blog, BlogData
from sqlalchemy.orm.session import Session

from models.blog import Blog
from schemas.blog_schema import ReadBlogResponse, CreateBlogRequest, CreateBlogResponse, UpdateBlogRequest

async def get_all_blogs(db: Session):
    return db.query(Blog).all()

async def get_blog_by_id(id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"해당 id {id}는(은) 존재하지 않습니다.")
    return blog

async def create_blog(data: CreateBlogRequest, db: Session):
    try :
        blog = Blog(
            title=data.title,
            content=data.content,
            author=data.author
        )
        db.add(blog)
        db.commit()
        db.refresh(blog)

        return blog
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")

async def update_blog(id: int, data: UpdateBlogRequest, db: Session):
    try:
        blog = db.query(Blog).filter(Blog.id == id).first()

        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"해당 id {id}는(은) 존재하지 않습니다.")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(blog, key, value)

        db.commit()
        db.refresh(blog)
        return blog
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")

async def delete_blog(id: int, db: Session):
    try:
        blog = db.query(Blog).filter(Blog.id == id).first()

        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"해당 id {id}는(은) 존재하지 않습니다.")

        db.delete(blog)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")