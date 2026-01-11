from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from db.database import direct_get_conn, context_get_conn, get_db
from sqlalchemy import text, Connection
from schemas.blog_schema import Blog, BlogData
from sqlalchemy.orm.session import Session

from models.blog import Blog
from schemas.blog_schema import ReadBlogResponse, CreateBlogRequest, CreateBlogResponse, UpdateBlogRequest

router = APIRouter(prefix= "/blogs", tags=["blogs"])

@router.get("/", response_model=List[ReadBlogResponse])
async def get_all_blogs(db: Session = Depends(get_db)):
    return db.query(Blog).all()

@router.get("/{id}", response_model=ReadBlogResponse)
async def get_blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"해당 id {id}는(은) 존재하지 않습니다.")
    return blog

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateBlogResponse)
async def create_blog(data: CreateBlogRequest, db: Session = Depends(get_db)):
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

@router.put("/{id}", response_model=ReadBlogResponse)
async def update_blog(id: int, data: UpdateBlogRequest, db: Session = Depends(get_db)):
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

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id: int, db: Session = Depends(get_db)):
    try:
        blog = db.query(Blog).filter(Blog.id == id).first()

        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"해당 id {id}는(은) 존재하지 않습니다.")

        db.delete(blog)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Error")

# @router.get("/")
# async def get_all_blogs():
#     conn = None
#     try:
#         conn = direct_get_conn()
#         query = """
#             select id, title, author, content, image_loc, modified_dt from blog
#         """
#
#         result = conn.execute(text(query))
#         # rows = result.fetchall()
#         rows = [BlogData(id = row.id,
#                      title = row.title,
#                      author= row.author,
#                      content = row.content,
#                      image_loc = row.image_loc,
#                      modified_dt = row.modified_dt
#                     ) for row in result]
#
#         result.close()
#         return rows
#     except SQLAlchemyError as e:
#         print(e)
#         raise e
#     finally:
#         if conn:
#             conn.close()


# @router.get("/{id}")
# async def get_blog_by_id(id: int,
#                          conn: Connection = Depends(context_get_conn)):
#     try:
#         query = f"""
#         select id, title, author, content, image_loc, modified_dt
#         from blog
#         where id = :id
#         """
#
#         stmt = text(query)
#         bind_stmt = stmt.bindparams(id = id)
#         result = conn.execute(bind_stmt)
#
#         if result.rowcount == 0:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"해당 id {id}는(은) 존재하지 않습니다.")
#
#
#         row = result.fetchone()
#         return BlogData(
#             id = row.id,
#                  title = row.title,
#                  author = row.author,
#                  content = row.content,
#                  image_loc = row.image_loc,
#                  modified_dt = row.modified_dt
#                  )
#     except SQLAlchemyError as e:
#         print(e)
#         raise e