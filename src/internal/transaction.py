from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, AsyncGenerator

from src.config.app import get_config
from src.pkg.context import get_tx_id
from src.pkg.driver.postgres import PostgresDriver


def transaction(func):
    """
    A decorator that wraps a function to provide a transactional context using a PostgreSQL database connection.
    It checks if a connection already exists for the current transaction ID. If not, it initializes a new connection pool,
    acquires a connection, and starts a transaction. The wrapped function is then executed within this transactional context.
    After the function execution, the connection is removed from the transaction context.

    Args:
        func (Callable): The function to be wrapped in a transactional context.

    Returns:
        Callable: The wrapped function with transactional support.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        driver = PostgresDriver(
            host=get_config().POSTGRES.HOST,
            port=get_config().POSTGRES.PORT,
            username=get_config().POSTGRES.USERNAME,
            password=get_config().POSTGRES.PASSWORD,
            db=get_config().POSTGRES.DB,
        )
        conn = driver.conn.get(get_tx_id())
        if conn is not None:
            return await func(*args, **kwargs)

        await driver._init_pool()
        try:
            async with driver.pool.acquire() as conn:
                async with conn.transaction():
                    driver.conn[get_tx_id()] = conn
                    return await func(*args, **kwargs)
        finally:
            del driver.conn[get_tx_id()]

    return wrapper


@asynccontextmanager
async def tx() -> AsyncGenerator[Any, None]:
    """
    An asynchronous context manager that provides a transactional connection to the PostgreSQL database.
    It checks if a connection already exists for the current transaction ID. If not, it initializes a new connection pool,
    acquires a connection, and starts a transaction. The connection is yielded for use within the context block.
    After the block is executed, the connection is removed from the transaction context.

    Yields:
        AsyncGenerator[Any, None]: The database connection for the current transaction.
    """
    driver = PostgresDriver(
        host=get_config().POSTGRES.HOST,
        port=get_config().POSTGRES.PORT,
        username=get_config().POSTGRES.USERNAME,
        password=get_config().POSTGRES.PASSWORD,
        db=get_config().POSTGRES.DB,
    )
    conn = driver.conn.get(get_tx_id())
    if conn is not None:
        yield conn

    else:
        await driver._init_pool()
        async with driver.pool.acquire() as conn:
            async with conn.transaction():
                driver.conn[get_tx_id()] = conn
                yield conn

        del driver.conn[get_tx_id()]
