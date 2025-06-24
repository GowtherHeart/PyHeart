from src.entity.db.core import CoreEntity
from src.entity.db.tasks import TasksCustomEntity, TasksEntity
from src.pkg.abc.model import ParamsModel, PayloadModel

__all__ = ["CreatePldModel", "UpdatePldModel", "GetPrmModel"]


class GetPrmModel(
    ParamsModel,
    TasksCustomEntity.name_op,
    TasksCustomEntity.date_create_op,
    CoreEntity.limit,
    CoreEntity.offset,
):
    """Parameters model for retrieving tasks with filters."""


class DeletePrmModel(
    ParamsModel,
    TasksEntity.name,
):
    """Parameters model for deleting tasks."""


class CreatePldModel(
    PayloadModel,
    TasksEntity.name,
    TasksEntity.content,
):
    """Payload model for creating a new task."""


class UpdatePldModel(
    PayloadModel,
    TasksEntity.name,
    TasksEntity.content,
    TasksEntity.complete,
):
    """Payload model for updating an existing task."""
