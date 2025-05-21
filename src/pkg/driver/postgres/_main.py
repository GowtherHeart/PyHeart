import hashlib
from abc import abstractmethod
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, List, Self

import asyncpg  # type: ignore

from src.pkg.context import get_tx_id

__all__ = ["PostgresDriver"]


class Cursor:
    """
    Abstract base class for database cursor operations.

    Provides interface for navigating and fetching data from query results
    in a cursor-based manner. Implementations should provide efficient
    row-by-row data access for large result sets.

    Example:
        ```python
        cursor = await connection.cursor("SELECT * FROM users")
        row = await cursor.fetchrow()  # Get single row
        rows = await cursor.fetch(10)  # Get 10 rows
        await cursor.forward(5)  # Skip 5 rows
        ```
    """

    @abstractmethod
    async def fetchrow(self) -> Dict[Any, Any]:
        """
        Fetch the next row from the cursor.

        Returns:
            Dict[Any, Any]: A dictionary representing the next row,
                           or empty dict if no more rows available.
        """
        ...

    @abstractmethod
    async def fetch(self, value: int) -> List[Dict[Any, Any]]:
        """
        Fetch multiple rows from the cursor.

        Args:
            value (int): Number of rows to fetch.

        Returns:
            List[Dict[Any, Any]]: List of dictionaries representing the fetched rows.
        """
        ...

    @abstractmethod
    async def forward(self, value: int) -> None:
        """
        Move the cursor forward by the specified number of rows.

        Args:
            value (int): Number of rows to skip forward.
        """
        ...


class Connector:
    """
    Abstract base class for database connection operations.

    Provides interface for executing queries, managing transactions, and
    handling database connections. Implementations should provide methods
    for both simple queries and transaction-based operations.

    Example:
        ```python
        async with connector.transaction() as tx:
            await tx.execute("INSERT INTO users (name) VALUES ($1)", "John")
            result = await tx.fetchrow("SELECT * FROM users WHERE name = $1", "John")
        ```
    """

    @abstractmethod  # type: ignore
    @asynccontextmanager  # type: ignore
    async def transaction(self) -> AsyncGenerator[Self, None]:
        """
        Create a database transaction context manager.

        Yields:
            AsyncGenerator[Self, None]: A transaction-enabled connector instance.

        Example:
            ```python
            async with connector.transaction() as tx:
                await tx.execute("INSERT INTO table VALUES ($1)", value)
            ```
        """
        ...

    @abstractmethod
    async def cursor(self, query: str, *args: Any) -> Cursor:
        """
        Create a cursor for the given query.

        Args:
            query (str): SQL query to execute.
            *args (Any): Query parameters.

        Returns:
            Cursor: A cursor object for navigating query results.
        """
        ...

    @abstractmethod
    async def execute(self, query: str, *args: Any) -> None:
        """
        Execute a query without returning results.

        Used for INSERT, UPDATE, DELETE operations.

        Args:
            query (str): SQL query to execute.
            *args (Any): Query parameters.
        """
        ...

    @abstractmethod
    async def executemany(self, query: str, *args: Any) -> None:
        """
        Execute a query multiple times with different parameter sets.

        Efficient for bulk operations like batch inserts.

        Args:
            query (str): SQL query to execute.
            *args (Any): Multiple parameter sets for the query.
        """
        ...

    @abstractmethod
    async def fetchrow(self, query: str, *args: Any) -> Dict[Any, Any]:
        """
        Execute a query and fetch a single row.

        Args:
            query (str): SQL query to execute.
            *args (Any): Query parameters.

        Returns:
            Dict[Any, Any]: Dictionary representing the fetched row.
        """
        ...

    @abstractmethod
    async def fetchval(self, query: str, *args: Any) -> Dict[Any, Any]:
        """
        Execute a query and fetch a single value.

        Args:
            query (str): SQL query to execute.
            *args (Any): Query parameters.

        Returns:
            Dict[Any, Any]: The single value result.
        """
        ...

    @abstractmethod
    async def fetch(self, query: str, *args: Any) -> List[Dict[Any, Any]]:
        """
        Execute a query and fetch all results.

        Args:
            query (str): SQL query to execute.
            *args (Any): Query parameters.

        Returns:
            List[Dict[Any, Any]]: List of dictionaries representing all fetched rows.
        """
        ...


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
        """
        Initialize the PostgreSQL connection pool if not already created.

        Creates an asyncpg connection pool with the configured parameters.
        This method is idempotent - subsequent calls will not recreate the pool.
        """
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
        """
        Execute a SELECT query without transaction context.

        Acquires a connection from the pool, executes the query, and returns results.
        This method bypasses any existing transaction context.

        Args:
            query (str): SQL SELECT query to execute.
            *args: Query parameters.

        Returns:
            Any: Query results as returned by asyncpg.

        Example:
            ```python
            results = await driver.force_select(
                "SELECT * FROM users WHERE age > $1", 18
            )
            ```
        """
        await self._init_pool()
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def transaction_select(self, query, *args) -> Any:
        """
        Execute a SELECT query within transaction context.

        If a transaction is already active (identified by transaction ID),
        uses the existing connection. Otherwise, creates a new transaction.

        Args:
            query (str): SQL SELECT query to execute.
            *args: Query parameters.

        Returns:
            Any: Query results as returned by asyncpg.

        Note:
            Uses transaction ID from context to maintain connection consistency
            across multiple operations within the same transaction.
        """
        if self.conn.get(get_tx_id(), None) is not None:
            return await self.conn[get_tx_id()].fetch(query, *args)

        await self._init_pool()
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                return await conn.fetch(query, *args)

    async def force_execute(self, query: str, *args) -> None:
        """
        Execute a query without returning results, bypassing transaction context.

        Used for INSERT, UPDATE, DELETE operations that don't need to return data.
        Acquires a fresh connection from the pool for execution.

        Args:
            query (str): SQL query to execute.
            *args: Query parameters.

        Example:
            ```python
            await driver.force_execute(
                "INSERT INTO users (name, email) VALUES ($1, $2)",
                "John Doe", "john@example.com"
            )
            ```
        """
        await self._init_pool()
        async with self.pool.acquire() as conn:
            await conn.execute(query, *args)

    async def transaction_execute(self, query, *args) -> None:
        """
        Execute a query within transaction context without returning results.

        If a transaction is already active, uses the existing connection.
        Otherwise, creates a new transaction for the operation.

        Args:
            query (str): SQL query to execute.
            *args: Query parameters.

        Note:
            There appears to be a bug in the current implementation - it calls
            fetch() instead of execute() when using an existing transaction connection.
            This should be addressed in a future fix.
        """
        if self.conn.get(get_tx_id(), None) is not None:
            return await self.conn[get_tx_id()].fetch(query, *args)

        await self._init_pool()
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                return await conn.execute(query, *args)
