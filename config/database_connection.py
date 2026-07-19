import logging
import os
from collections.abc import Iterator
from contextlib import contextmanager

from dotenv import load_dotenv
from psycopg2.extensions import connection, cursor
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool

load_dotenv()

logger = logging.getLogger(__name__)


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        logger.error(f"Environment Variable: '{name}' missing!")
        raise RuntimeError(f"Environment Variable '{name}' Not Set!")
    return value


DB_HOST: str = get_required_env("DB_HOST")
DB_NAME: str = get_required_env("DB_NAME")
DB_PASSWORD: str = get_required_env("DB_PASS")
DB_USER: str = get_required_env("DB_USER")
DB_PORT: int = int(get_required_env("DB_PORT"))

pool: SimpleConnectionPool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=DB_HOST,
    user=DB_USER,
    database=DB_NAME,
    password=DB_PASSWORD,
    port=DB_PORT,
)


@contextmanager
def get_connection() -> Iterator[connection]:
    conn: connection = pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        logger.exception("Database Transaction Failed")
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)


@contextmanager
def get_cursor(conn: connection | None = None) -> Iterator[cursor]:
    if conn is None:
        with (
            get_connection() as conn,
            conn.cursor(cursor_factory=RealDictCursor) as cur,
        ):
            yield cur
    else:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            yield cur


def close_pool() -> None:
    pool.closeall()
