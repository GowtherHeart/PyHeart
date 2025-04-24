from asyncpg import UniqueViolationError

from src.entity.db.types.core import CoreTyping
from src.entity.db.types.notes import NotesCustomTyping, NotesTyping
from src.internal.exception.notes import NoteCreateException, NoteUpdateException
from src.models.db.notes import NoteCoreModel
from src.pkg.driver.query import QueryExecute, QueryTxExecute

__all__ = ["CreateQuery", "UpdateQuery", "SelectQuery"]


class CreateQuery(QueryTxExecute):
    query = """
        insert into notes(name, content)
        values($1, $2)
        returning id, name, content, date_create, date_update, deleted;
    """

    exception_map = {UniqueViolationError: NoteCreateException}

    def __init__(
        self,
        name: NotesTyping.name,
        content: NotesTyping.content,
    ) -> None:
        super().__init__(name, content)

    async def execute(self) -> NoteCoreModel:
        return await super().execute()


class UpdateQuery(QueryExecute):
    query = """
        update notes set
            content = COALESCE($1, content),
            deleted = COALESCE($3, deleted)
        where true
            and name = $2
        returning id, name, content, date_create, date_update, deleted;
    """
    exception_map = {UniqueViolationError: NoteUpdateException}

    def __init__(
        self,
        name: NotesCustomTyping.name = None,
        content: NotesTyping.content = None,
        deleted: NotesCustomTyping.deleted = None,
    ) -> None:
        super().__init__(content, name, deleted)

    async def execute(self) -> list[NoteCoreModel]:
        return await super().execute()


class SelectQuery(QueryExecute):
    query = """
        select
            n.id as id,
            n.name as name,
            n.content as content,
            n.date_create as date_create,
            n.date_update as date_update,
            n.deleted as deleted
        from notes n
        where true
            and ($1::text is null or n.name = $1)
            and ($2::timestamp is null or n.date_create = $2)
        limit $3
        offset $4;
    """

    def __init__(
        self,
        name: NotesCustomTyping.name,
        date_create: NotesCustomTyping.date_create,
        limit: CoreTyping.limit = 100,
        offset: CoreTyping.offset = 0,
    ) -> None:
        super().__init__(name, date_create, limit, offset)

    async def execute(self) -> list[NoteCoreModel]:
        return await super().execute()
