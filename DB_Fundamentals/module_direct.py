from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from database import direct_get_conn

def execute_query(conn: Connection):
    query = "select * from blog"
    stmt = text(query)
    result = conn.execute(stmt)

    rows = result.fetchall()
    print(rows)
    result.close()

def execute_sleep(conn: Connection):
    query = "select sleep(5)"
    result = conn.execute(text(query))
    result.close()

for ind in range(20):
    try:
        with direct_get_conn() as conn:
            execute_sleep(conn)
            print("loop index: ", ind)
    except SQLAlchemyError as e:
        print(e)

print("end of loop")