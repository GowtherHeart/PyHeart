from pydantic import Field

from src.pkg.abc.entity import Entity, FieldEntity

from .types.notes import NotesCustomTyping, NotesTyping


class NotesEntity(Entity):
    """Database entity representing notes with all core fields."""

    class id(FieldEntity):
        """Note unique identifier field entity."""

        id: NotesTyping.id = Field(...)

    class name(FieldEntity):
        """Note title/name field entity."""

        name: NotesTyping.name = Field(...)

    class content(FieldEntity):
        """Note content/body field entity."""

        content: NotesTyping.content = Field(...)

    class date_create(FieldEntity):
        """Note creation timestamp field entity."""

        date_create: NotesTyping.date_create = Field(...)

    class date_update(FieldEntity):
        """Note last update timestamp field entity."""

        date_update: NotesTyping.date_update = Field(...)

    class deleted(FieldEntity):
        """Note soft deletion flag field entity."""

        deleted: NotesTyping.deleted = Field(...)


class NotesCustomEntity(Entity):
    """Custom database entity for optional note fields and operations."""

    class name_op(FieldEntity):
        """Optional note name field entity for custom operations."""

        name: NotesCustomTyping.name = Field(None)

    class date_create_op(FieldEntity):
        """Optional note creation date field entity for custom operations."""

        date_create: NotesCustomTyping.date_create = Field(None)
