from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError

DATABASE_CONN = "mysql+mysqlconnector://root:1548@localhost:3306/blog_db"

engine = create_engine(DATABASE_CONN, poolclass=QueuePool, pool_size=10, max_overflow=0)
print("engine created")

# conn = engine.connect()

try:
    with engine.connect() as conn:
        query = "select id, title from blog"
        stmt = text(query)
        result = conn.execute(stmt)

        rows = result.fetchall()
        print(rows)
        result.close()
except SQLAlchemyError as e:
    print(e)