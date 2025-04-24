from src.entity.db.types.core import CoreTyping
from src.entity.db.types.tasks import TasksCustomTyping, TasksTyping
from src.models.db.tasks import TaskCoreModel
from src.pkg.driver.query import QueryExecute, QueryTxExecute

__all__ = ["CreateQuery", "UpdateQuery", "SelectQuery"]


class CreateQuery(QueryTxExecute):
    query = """
        insert into tasks(name, content)
        values($1, $2)
        returning id, name, content, complete, date_create, date_update, deleted;
    """

    def __init__(
        self,
        name: TasksTyping.name,
        content: TasksTyping.content,
    ) -> None:
        super().__init__(name, content)

    async def execute(self) -> TaskCoreModel:
        return await super().execute()


class UpdateQuery(QueryExecute):
    query = """
        update tasks set
            content = COALESCE($1, content),
            deleted = COALESCE($3, deleted),
            complete = COALESCE($4, complete)
        where true
            and name = $2
        returning id, name, content, complete, date_create, date_update, deleted;
    """

    def __init__(
        self,
        name: TasksCustomTyping.name = None,
        content: TasksTyping.content = None,
        deleted: TasksCustomTyping.deleted = None,
        complete: TasksCustomTyping.complete = None,
    ) -> None:
        super().__init__(content, name, deleted, complete)

    async def execute(self) -> list[TaskCoreModel]:
        return await super().execute()


class SelectQuery(QueryExecute):
    query = """
        select
            t.id as id,
            t.name as name,
            t.content as content,
            t.complete as complete,
            t.date_create as date_create,
            t.date_update as date_update,
            t.deleted as deleted
        from tasks t
        where true
            and ($1::text is null or t.name = $1)
            and ($2::timestamp is null or t.date_create = $2)

        limit $3
        offset $4;
    """

    def __init__(
        self,
        name: TasksCustomTyping.name = None,
        date_create: TasksCustomTyping.date_create = None,
        limit: CoreTyping.limit = 100,
        offset: CoreTyping.offset = 0,
    ) -> None:
        super().__init__(name, date_create, limit, offset)

    async def execute(self) -> list[TaskCoreModel]:
        return await super().execute()
