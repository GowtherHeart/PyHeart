from pydantic import Field

from src.pkg.abc.entity import Entity, FieldEntity

from .types.tasks import TasksCustomTyping, TasksTyping


class TasksEntity(Entity):
    """
    Represents a task entity with various fields such as id, name, content,
    completion status, creation date, update date, and deletion status.
    Each field is defined as a subclass of FieldEntity, ensuring type safety
    and validation using Pydantic's Field.
    """

    class id(FieldEntity):
        id: TasksTyping.id = Field(...)

    class name(FieldEntity):
        name: TasksTyping.name = Field(...)

    class content(FieldEntity):
        content: TasksTyping.content = Field(...)

    class complete(FieldEntity):
        complete: TasksTyping.complete = Field(...)

    class date_create(FieldEntity):
        date_create: TasksTyping.date_create = Field(...)

    class date_update(FieldEntity):
        date_update: TasksTyping.date_update = Field(...)

    class deleted(FieldEntity):
        deleted: TasksTyping.deleted = Field(...)


class TasksCustomEntity(Entity):
    """
    Represents a custom task entity with optional fields for name and creation date.
    Each field is defined as a subclass of FieldEntity, allowing for type safety
    and validation using Pydantic's Field. This class is designed for scenarios
    where only a subset of task attributes are required.
    """

    class name_op(FieldEntity):
        name: TasksCustomTyping.name = Field(None)

    class date_create_op(FieldEntity):
        date_create: TasksCustomTyping.date_create = Field(None)
