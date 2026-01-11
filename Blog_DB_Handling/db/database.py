from sqlalchemy import create_engine, Connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
# from contextlib import contextmanager
# from fastapi import status
# from fastapi.exceptions import HTTPException
# from dotenv import load_dotenv
# import os

DATABASE_CONN = "mysql+mysqlconnector://root:1548@localhost:3306/blog_db"

# load_dotenv()
#
# DATABASE_CONN = os.getenv("DATABASE_CONN")
# print("########", DATABASE_CONN)

engine = create_engine(DATABASE_CONN, poolclass=QueuePool, pool_size=10, max_overflow=0, pool_recycle=300)

#raw sql용
def direct_get_conn():
    conn = None
    try:
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        print(e)
        raise e

def context_get_conn():
    try:
        with engine.connect() as conn:
            yield conn
    except SQLAlchemyError as e:
        print(e)
        raise e

# 아래는 Orm 변환 코드
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
