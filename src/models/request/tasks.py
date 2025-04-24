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
    """
    A model for retrieving task parameters, including operations on task name and creation date.
    """


class DeletePrmModel(
    ParamsModel,
    TasksEntity.name,
):
    """
    A model for deleting task parameters, specifically focusing on the task name.
    """


class CreatePldModel(
    PayloadModel,
    TasksEntity.name,
    TasksEntity.content,
):
    """
    A model for creating a task payload, including task name and content.
    """


class UpdatePldModel(
    PayloadModel,
    TasksEntity.name,
    TasksEntity.content,
    TasksEntity.complete,
):
    """
    A model for updating a task payload, including task name, content, and completion status.
    """
