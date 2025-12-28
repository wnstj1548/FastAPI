from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError

DATABASE_CONN = "mysql+mysqlconnector://root:1548@localhost:3306/blog_db"

engine = create_engine(DATABASE_CONN, poolclass=QueuePool, pool_size=10, max_overflow=0)

def direct_get_conn():
    try:
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        print(e)
        raise e

#with 절 사용시 이슈
# def context_get_conn():
#     try:
#         with engine.connect() as conn:
#             yield conn
#     except SQLAlchemyError as e:
#         print(e)
#         raise e
#     finally:
#         conn.close()
#         print("###### connection yield is finished")

@contextmanager
def context_get_conn():
    try:
        with engine.connect() as conn:
            yield conn
    except SQLAlchemyError as e:
        print(e)
        raise e
    # finally:
    #     conn.close()