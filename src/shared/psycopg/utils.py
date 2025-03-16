from psycopg import connect

from shared.psycopg import db_pool


def is_pg_engine_reachable():
    try:
        connection = connect(f"{db_pool.connection_string}?connect_timeout=5")
        connection.close()
        return True
    except:
        return False
