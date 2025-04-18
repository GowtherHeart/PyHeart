import inspect
from typing import Any, Sequence

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
    catch_exception: list[Exception] | None = None
    return_exception: Exception | None = None

    def __init__(self, *args) -> None:
        self.param = args

    async def _execute(self) -> Any:
        raise NotImplementedError()

    async def execute(self) -> Any:
        try:
            result = await self._execute()
        except Exception as exc:
            if self.catch_exception is not None and exc not in self.catch_exception:
                raise exc

            raise self.return_exception or exc

        if self.skip is True:
            return result

        if self.array is False:
            return self.model(**result[0])

        return [self.model(**el) for el in result]


class QueryForceSelect(Query):
    async def _execute(self) -> Any:
        return await self.driver.force_select(self.query, *self.param)


class QueryTransactionSelect(Query):
    async def _execute(self) -> Any:
        return await self.driver.transaction_select(self.query, *self.param)


class QueryTransactionExecute(Query):
    async def _execute(self) -> Any:
        return await self.driver.transaction_execute(self.query, *self.param)


class QueryForceExecute(Query):
    async def _execute(self) -> Any:
        return await self.driver.transaction_execute(self.query, *self.param)


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

    for obj in result:
        data = obj.execute.__annotations__
        if "__args__" not in dir(data["return"]):
            obj.model = data["return"]
            if data["return"] in (int, str):
                obj.skip = True

            obj.driver = driver
            obj.array = False
        else:
            obj.model = data["return"].__args__[0]
            obj.driver = driver
            obj.array = True
