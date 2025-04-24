from src.internal.exception import EmptyResultException
from src.internal.transaction import transaction
from src.models.db.tasks import TaskCoreModel
from src.models.request import tasks as task_req
from src.pkg.abc.usecase import Usecase
from src.repository import tasks as task_repo


class TasksV1US(Usecase):
    async def get(self, model: task_req.GetPrmModel) -> list[TaskCoreModel]:
        return await task_repo.SelectQuery(
            name=model.name,
            date_create=model.date_create,
            limit=model.limit,
            offset=model.offset,
        ).execute()

    @transaction
    async def create(self, payload: task_req.CreatePldModel) -> TaskCoreModel:
        return await task_repo.CreateQuery(
            name=payload.name,
            content=payload.content,
        ).execute()

    @transaction
    async def update(self, payload: task_req.UpdatePldModel) -> TaskCoreModel:
        effect = await task_repo.UpdateQuery(
            name=payload.name,
            content=payload.content,
        ).execute()
        if len(effect) == 0:
            raise EmptyResultException()

        return effect[0]

    async def delete(self, model: task_req.DeletePrmModel) -> TaskCoreModel:
        effect = await task_repo.UpdateQuery(
            name=model.name,
            deleted=True,
        ).execute()
        if len(effect) == 0:
            raise EmptyResultException()

        return effect[0]
