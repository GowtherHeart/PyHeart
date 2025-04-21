from starlette import status

from src.entity.db.types.core import CoreTyping
from src.entity.db.types.tasks import TasksCustomTyping, TasksTyping
from src.internal.fastapi.controller import HttpController
from src.models.request.tasks import (
    TasksCreatePldModel,
    TasksDeletePrmModel,
    TasksGetPrmModel,
    TasksUpdatePldModel,
)
from src.models.response.tasks import TasksCoreRespModel
from src.pkg.abc.controller import router
from src.usecase.tasks import TasksV1US


class TasksCoreControllerV1(HttpController):
    """
    TasksCoreControllerV1 is responsible for handling HTTP requests related to task operations.
    It provides endpoints for creating, retrieving, updating, and deleting tasks.
    The controller uses the TasksV1US use case to perform operations and returns responses
    in the form of TasksCoreResponseModel.
    """

    prefix = "/tasks"
    tags = ["tasks"]

    @router(path="/", status_code=status.HTTP_200_OK)
    async def get(
        self,
        name: TasksCustomTyping.name = None,
        date_create: TasksCustomTyping.date_create = None,
        limit: CoreTyping.limit = 100,
        offset: CoreTyping.offset = 0,
    ) -> list[TasksCoreRespModel]:
        model = TasksGetPrmModel(
            name=name,
            date_create=date_create,
            limit=limit,
            offset=offset,
        )
        result = await TasksV1US().get(model=model)
        return [TasksCoreRespModel(**e.model_dump()) for e in result]

    @router(path="/", status_code=status.HTTP_201_CREATED)
    async def post(self, payload: TasksCreatePldModel) -> TasksCoreRespModel:
        result = await TasksV1US().create(payload=payload)
        return TasksCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def patch(self, payload: TasksUpdatePldModel) -> list[TasksCoreRespModel]:
        result = await TasksV1US().update(payload=payload)
        # return TasksCoreResponseModel(**result.model_dump())
        return [TasksCoreRespModel(**e.model_dump()) for e in result]

    @router(path="/", status_code=status.HTTP_200_OK)
    async def delete(self, name: TasksTyping.name) -> list[TasksCoreRespModel]:
        model = TasksDeletePrmModel(name=name)
        result = await TasksV1US().delete(model=model)
        # return TasksCoreResponseModel(**result.model_dump())
        return [TasksCoreRespModel(**e.model_dump()) for e in result]
