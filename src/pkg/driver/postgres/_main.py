import hashlib
from abc import abstractmethod
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, List, Self

import asyncpg  # type: ignore

from src.pkg.context import get_tx_id

__all__ = ["PostgresDriver"]


class Cursor:
    @abstractmethod
    async def fetchrow(self) -> Dict[Any, Any]: ...

    @abstractmethod
    async def fetch(self, value: int) -> List[Dict[Any, Any]]: ...

    @abstractmethod
    async def forward(self, value: int) -> None: ...


class Connector:
    @abstractmethod  # type: ignore
    @asynccontextmanager  # type: ignore
    async def transaction(self) -> AsyncGenerator[Self, None]: ...

    @abstractmethod
    async def cursor(self, query: str, *args: Any) -> Cursor: ...

    @abstractmethod
    async def execute(self, query: str, *args: Any) -> None: ...

    @abstractmethod
    async def executemany(self, query: str, *args: Any) -> None: ...

    @abstractmethod
    async def fetchrow(self, query: str, *args: Any) -> Dict[Any, Any]: ...

    @abstractmethod
    async def fetchval(self, query: str, *args: Any) -> Dict[Any, Any]: ...

    @abstractmethod
    async def fetch(self, query: str, *args: Any) -> List[Dict[Any, Any]]: ...


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


class PostgresDriver(metaclass=_Singleton):
    """
    A singleton class that manages a connection pool to a PostgreSQL database using asyncpg.

    This class provides methods to execute queries and transactions asynchronously. It ensures
    that only one instance of the connection pool is created for a given set of connection parameters.

    Attributes:
        pool (asyncpg.Pool): The connection pool for the PostgreSQL database.
        _host (str): The hostname of the PostgreSQL server.
        _port (int): The port number on which the PostgreSQL server is listening.
        _username (str): The username for authenticating with the PostgreSQL server.
        _password (str): The password for authenticating with the PostgreSQL server.
        db (str): The name of the database to connect to.
        min_size (int): The minimum number of connections in the pool.
        max_size (int): The maximum number of connections in the pool.
        max_inactive_connection_lifetime (int): The maximum lifetime of inactive connections in the pool.
        conn (dict): A dictionary to manage transaction-specific connections.
    """

    pool: asyncpg.Pool = None  # type: ignore

    _host: str
    _port: int
    _username: str
    _password: str
    db: str

    conn: dict = {}

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        db: str,
        min_size: int = 2,
        max_size: int = 10,
        max_inactive_connection_lifetime: int = 50,
    ) -> None:
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self.db = db
        self.min_size = min_size
        self.max_size = max_size
        self.max_inactive_connection_lifetime = max_inactive_connection_lifetime

    async def _init_pool(self) -> None:
        if self.pool is None:
            self.pool = await asyncpg.create_pool(
                database=self.db,
                user=self._username,
                port=self._port,
                password=self._password,
                host=self._host,
                min_size=self.min_size,
                max_size=self.max_size,
                max_inactive_connection_lifetime=self.max_inactive_connection_lifetime,
            )

    async def force_select(self, query: str, *args) -> Any:
        await self._init_pool()
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def transaction_select(self, query, *args) -> Any:
        if self.conn.get(get_tx_id(), None) is not None:
            return await self.conn[get_tx_id()].fetch(query, *args)

        await self._init_pool()
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                return await conn.fetch(query, *args)

    async def force_execute(self, query: str, *args) -> None:
        await self._init_pool()
        async with self.pool.acquire() as conn:
            await conn.execute(query, *args)

    async def transaction_execute(self, query, *args) -> None:
        if self.conn.get(get_tx_id(), None) is not None:
            return await self.conn[get_tx_id()].fetch(query, *args)

        await self._init_pool()
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                return await conn.execute(query, *args)
