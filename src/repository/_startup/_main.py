from src.pkg.driver.query import QueryExecute

__all__ = ["InitConnectionQuery"]


class InitConnectionQuery(QueryExecute):
    """
    This class is responsible for initializing a connection by executing a simple query.
    It inherits from QueryForceSelect and overrides the execute method to perform the query.
    """

    query = """
        select 1;
    """

    def __init__(self) -> None:
        super().__init__()

    async def execute(self) -> int:
        return await super().execute()
