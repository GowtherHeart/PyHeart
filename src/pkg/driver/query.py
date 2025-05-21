import inspect
from typing import Any, Sequence

from loguru import logger

from src.pkg.driver.postgres import PostgresDriver


class Query:
    """
    Base class for executing database queries using a specified driver.

    This class provides a framework for executing queries with parameters and handling
    exceptions. It supports both single and array results, and allows for custom exception
    handling and result transformation using a model class.

    Attributes:
        query (str): The SQL query to be executed.
        param (Sequence): The parameters to be used in the query.
        driver (PostgresDriver): The database driver used to execute the query.
        model (Any): The model class used to transform query results.
        array (bool): Flag indicating if the result should be an array of models.
        skip (bool): Flag indicating if result transformation should be skipped.
        catch_exception (list[Exception] | None): List of exceptions to catch during execution.
        return_exception (Exception | None): Exception to raise if a caught exception occurs.

    Methods:
        __init__(*args): Initializes the query with the given parameters.
        _execute(): Abstract method to be implemented by subclasses for executing the query.
        execute(): Executes the query and handles exceptions and result transformation.
    """

    query: str = NotImplemented
    param: Sequence
    driver: PostgresDriver
    model: Any = None
    array: bool = False
    skip: bool = False
    exception_map: dict[type[Exception], type[Exception]] | None = None
    default_exception: type[Exception] | None = None

    def __init__(self, *args) -> None:
        """
        Initialize the query with parameters.

        Args:
            *args: Variable arguments to be used as query parameters.
        """
        self.param = args

    async def _execute(self) -> Any:
        """
        Abstract method for executing the database query.

        This method must be implemented by subclasses to define the specific
        execution strategy (e.g., with or without transactions).

        Returns:
            Any: Raw query results from the database driver.

        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError()

    async def execute(self) -> Any:
        """
        Execute the query with exception handling and result transformation.

        This method orchestrates the query execution process:
        1. Calls the abstract _execute() method
        2. Handles exceptions according to the configured exception mapping
        3. Transforms results using the configured model class
        4. Returns either single model instances or arrays based on configuration

        Returns:
            Any: Transformed query results - either model instances, arrays of models,
                 or raw results if skip=True.

        Raises:
            Exception: Mapped exceptions from exception_map, default_exception,
                      or the original exception if no mapping is configured.

        Example:
            ```python
            class GetUserQuery(QueryExecute):
                query = "SELECT * FROM users WHERE id = $1"
                model = User

            user = await GetUserQuery(123).execute()
            ```
        """
        try:
            result = await self._execute()
        except Exception as exc:
            if (
                self.exception_map is not None
                and (_exc := self.exception_map.get(type(exc), None)) is not None
            ):
                raise _exc

            logger.exception(f"[postgres] {exc}")
            if self.default_exception is not None:
                raise self.default_exception

            raise exc

        if self.skip is True or result is None or len(result) == 0:
            return result

        if self.array is False:
            return self.model(**result[0])

        return [self.model(**el) for el in result]


class QueryExecute(Query):
    """
    Query executor that runs queries without transaction context.

    This class executes queries using the driver's force_select method,
    which bypasses any existing transaction context and acquires a fresh
    connection from the pool.

    Use this for queries that don't need to be part of a transaction
    or when you need to ensure isolation from ongoing transactions.

    Example:
        ```python
        class GetAllUsersQuery(QueryExecute):
            query = "SELECT * FROM users"
            model = User
            array = True

        users = await GetAllUsersQuery().execute()
        ```
    """

    async def _execute(self) -> Any:
        """
        Execute query using force_select (non-transactional).

        Returns:
            Any: Raw query results from the PostgreSQL driver.
        """
        return await self.driver.force_select(self.query, *self.param)


class QueryTxExecute(Query):
    """
    Query executor that runs queries within transaction context.

    This class executes queries using the driver's transaction_select method,
    which either uses an existing transaction connection (if available) or
    creates a new transaction for the query.

    Use this for queries that need to be part of a transaction or when
    you need to maintain consistency with other transactional operations.

    Example:
        ```python
        class GetUserInTxQuery(QueryTxExecute):
            query = "SELECT * FROM users WHERE id = $1 FOR UPDATE"
            model = User

        # Within a transaction context
        user = await GetUserInTxQuery(user_id).execute()
        ```
    """

    async def _execute(self) -> Any:
        """
        Execute query using transaction_select (transactional).

        Returns:
            Any: Raw query results from the PostgreSQL driver.
        """
        return await self.driver.transaction_select(self.query, *self.param)


def inject(module, driver) -> None:
    """
    Injects a driver into Query subclasses within a given module.

    This function iterates over all classes in the provided module, identifies
    subclasses of the Query class, and sets their model, driver, and array attributes
    based on the return type annotations of their execute method.

    Args:
        module: The module containing Query subclasses to be processed.
        driver: The driver instance to be injected into the Query subclasses.
    """
    class_array = {
        name: cls for name, cls in vars(module).items() if inspect.isclass(cls)
    }
    result = []
    for _, v in class_array.items():
        if issubclass(v.__bases__[0], Query):
            result.append(v)

    logger.info(f"inject query: {result}")
    for obj in result:
        data = obj.execute.__annotations__
        if "__args__" not in dir(data["return"]):
            obj.model = data["return"]
            if data["return"] in (int, str, dict):
                obj.skip = True

            obj.driver = driver
            obj.array = False
        else:
            obj.model = data["return"].__args__[0]
            obj.driver = driver
            obj.array = True
