from src.entity.db.tasks import TasksEntity
from src.pkg.abc.model import ResponseModel

__all__ = ["TasksCoreRespModel"]


class TasksCoreRespModel(
    ResponseModel,
    TasksEntity.name,
    TasksEntity.content,
    TasksEntity.complete,
    TasksEntity.date_create,
    TasksEntity.date_update,
    TasksEntity.deleted,
):
    """
    A response model for tasks that combines fields from both the ResponseModel and TasksEntity.
    This model includes task attributes such as name, content, completion status, creation date,
    update date, and deletion status.
    """
