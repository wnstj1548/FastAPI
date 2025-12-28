from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from database import direct_get_conn
from datetime import datetime

try:
    with direct_get_conn() as conn:

        query = "select id, title, author from blog where id = :id and author = :author \
                 and modified_dt < :modified_dt"
        stmt = text(query)
        bind_stmt = stmt.bindparams(id=1, author='둘리', modified_dt=datetime.now())

        result = conn.execute(bind_stmt)
        rows = result.fetchall()
        print(rows)
        result.close()
except SQLAlchemyError as e:
    print("############# ", e)
    raise e