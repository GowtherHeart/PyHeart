import hashlib
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import redis.asyncio as aioredis
from loguru import logger

__all__ = ["RedisDriver"]


class _Singleton(type):
    """
    A metaclass for creating singleton classes with parameter-based instantiation.

    Unlike the traditional singleton pattern, this implementation allows for multiple
    instances of a class, each associated with a unique set of initialization parameters.
    The uniqueness of each instance is determined by hashing the provided arguments and
    keyword arguments. If an instance with the same parameter hash already exists, it is
    returned; otherwise, a new instance is created and stored.

    Attributes:
        _inst_map (dict): A dictionary mapping parameter hashes to their corresponding instances.
    """

    _inst_map: dict = {}

    def _merge_param(cls, *args, **kwargs) -> str:
        result = []
        for v in args:
            result.append(str(v))
        for _, v in kwargs.items():
            result.append(str(v))

        m = hashlib.sha256()
        m.update("".join(result).encode("utf-8"))
        return m.hexdigest()

    def __call__(cls, *args, **kwargs):
        param_hex = cls._merge_param(*args, **kwargs)
        if param_hex not in cls._inst_map:
            cls._inst_map[param_hex] = super(_Singleton, cls).__call__(*args, **kwargs)

        return cls._inst_map[param_hex]


class RedisDriver(metaclass=_Singleton):
    """
    A singleton Redis driver that manages connections to a Redis database using aioredis.

    This class provides async methods for basic Redis operations (get, set, delete)
    with connection pooling and automatic connection management. It ensures that only
    one instance is created for a given set of connection parameters.

    Attributes:
        _connector (Optional[aioredis.Redis]): The Redis connection instance.
        pool (aioredis.ConnectionPool): Connection pool for Redis connections.

    Example:
        ```python
        driver = RedisDriver(
            host="localhost",
            port=6379,
            username="user",
            password="pass",
            db="0"
        )

        await driver.set("key", "value", expire=3600)
        value = await driver.get("key")
        await driver.delete("key")
        ```
    """

    _connector: Optional[aioredis.Redis] = None

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        db: str,
        max_connection: int = 10,
    ) -> None:
        """
        Initialize the Redis driver with connection parameters.

        Args:
            host (str): Redis server hostname or IP address.
            port (int): Redis server port number.
            username (str): Username for Redis authentication.
            password (str): Password for Redis authentication.
            db (str): Redis database number to connect to.
            max_connection (int, optional): Maximum number of connections in the pool. Defaults to 10.
        """
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__db = db
        self.pool = aioredis.ConnectionPool.from_url(
            self.__create_dsn(), max_connections=max_connection
        )

    def __create_dsn(self) -> str:
        """
        Create a Redis Data Source Name (DSN) string from connection parameters.

        Returns:
            str: A properly formatted Redis connection string.

        Example:
            "redis://username:password@localhost:6379/0"
        """
        return (
            f"redis://{self.__username}:{self.__password}"
            + f"@{self.__host}:{self.__port}/{self.__db}"
        )

    @asynccontextmanager
    async def _create_connector(self) -> AsyncGenerator[aioredis.Redis, None]:
        """
        Create and manage a Redis connection context.

        Creates a Redis connection from the pool if one doesn't exist,
        yields it for use, and ensures proper cleanup on exit.

        Yields:
            AsyncGenerator[aioredis.Redis, None]: A Redis connection instance.

        Raises:
            Exception: Re-raises any exceptions that occur during Redis operations.
        """
        if self._connector is None:
            self._connector = aioredis.Redis(connection_pool=self.pool)

        try:
            yield self._connector
        except Exception as exc:
            logger.exception(f"[redis] {exc}")
            raise exc
        finally:
            await self._connector.close()

    async def set(self, name: str, value: str, expire: Optional[int] = None) -> None:
        """
        Set a key-value pair in Redis with optional expiration.

        Args:
            name (str): The key name to set.
            value (str): The value to store.
            expire (Optional[int], optional): Expiration time in seconds. Defaults to None (no expiration).

        Example:
            ```python
            await driver.set("user:123", "john_doe", expire=3600)  # Expires in 1 hour
            await driver.set("config", "value")  # No expiration
            ```
        """
        async with self._create_connector() as redis:
            async with redis.client() as conn:
                await conn.set(name=name, value=value, ex=expire)

    async def get(self, name: str) -> str:
        """
        Retrieve a value from Redis by key.

        Args:
            name (str): The key name to retrieve.

        Returns:
            str: The value stored at the key, or None if key doesn't exist.

        Example:
            ```python
            value = await driver.get("user:123")
            if value:
                print(f"User: {value}")
            ```
        """
        async with self._create_connector() as redis:
            async with redis.client() as conn:
                return await conn.get(name=name)

    async def delete(self, name: str) -> None:
        """
        Delete a key from Redis.

        Args:
            name (str): The key name to delete.

        Example:
            ```python
            await driver.delete("user:123")
            ```
        """
        async with self._create_connector() as redis:
            async with redis.client() as conn:
                await conn.delete(name)
