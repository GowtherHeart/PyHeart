from pydantic import Field

from src.pkg.abc.entity import Entity, FieldEntity

from .types.notes import NotesCustomTyping, NotesTyping


class NotesEntity(Entity):
    """
    NotesEntity is a core entity class that extends the base Entity class.
    It is designed to represent the essential fields of a note, ensuring
    that all necessary attributes are present and validated. This class
    includes fields such as 'id', 'name', 'content', 'date_create',
    'date_update', and 'deleted', which are crucial for managing note
    data within the application.
    """

    class id(FieldEntity):
        id: NotesTyping.id = Field(...)

    class name(FieldEntity):
        name: NotesTyping.name = Field(...)

    class content(FieldEntity):
        content: NotesTyping.content = Field(...)

    class date_create(FieldEntity):
        date_create: NotesTyping.date_create = Field(...)

    class date_update(FieldEntity):
        date_update: NotesTyping.date_update = Field(...)

    class deleted(FieldEntity):
        deleted: NotesTyping.deleted = Field(...)


class NotesCustomEntity(Entity):
    """
    NotesCustomEntity is a specialized entity class that extends the base Entity class.
    It is designed to handle custom fields specific to notes, allowing for optional
    attributes that can be used in various operations. This class includes fields
    such as 'name_op' and 'date_create_op', which are optional and can be utilized
    for custom note operations.
    """

    class name_op(FieldEntity):
        name: NotesCustomTyping.name = Field(None)

    class date_create_op(FieldEntity):
        date_create: NotesCustomTyping.date_create = Field(None)
