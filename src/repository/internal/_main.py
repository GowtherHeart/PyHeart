from src.entity.db.types.core import CoreTyping
from src.entity.db.types.internal import (
    InternalPgCustomTyping,
    InternalPgTyping,
)
from src.models.db.internal import InternalPostgresCoreModel
from src.pkg.driver.query import QueryExecute, QueryTxExecute

__all__ = [
    "CreateQuery",
    "UpdateQuery",
    "SelectQuery",
    "DeleteQuery",
]


class CreateQuery(QueryTxExecute):
    query = """
        insert into internal(name, value)
        values($1, $2)
        returning id, name, value;
    """

    def __init__(
        self,
        name: InternalPgTyping.name,
        value: InternalPgTyping.value,
    ) -> None:
        super().__init__(name, value)

    async def execute(self) -> InternalPostgresCoreModel:
        return await super().execute()


class UpdateQuery(QueryExecute):
    query = """
        update internal set
            value = COALESCE($1, value)
        where true
            and name = $2
        returning id, name, value;
    """

    def __init__(
        self,
        name: InternalPgCustomTyping.name = None,
        value: InternalPgCustomTyping.value = None,
    ) -> None:
        super().__init__(value, name)

    async def execute(self) -> InternalPostgresCoreModel:
        return await super().execute()


class DeleteQuery(QueryExecute):
    query = """
        delete from internal where name = $1
        returning id, name, value;
    """

    def __init__(
        self,
        name: InternalPgCustomTyping.name = None,
    ) -> None:
        super().__init__(name)

    async def execute(self) -> InternalPostgresCoreModel:
        return await super().execute()


class SelectQuery(QueryExecute):
    query = """
        select
            i.id as id,
            i.name as name,
            i.value as value
        from internal i
        where true
            and ($1::text is null or i.name = $1)
        limit $2
        offset $3;
    """

    def __init__(
        self,
        name: InternalPgCustomTyping.name,
        limit: CoreTyping.limit = 100,
        offset: CoreTyping.offset = 0,
    ) -> None:
        super().__init__(name, limit, offset)

    async def execute(self) -> list[InternalPostgresCoreModel]:
        return await super().execute()
