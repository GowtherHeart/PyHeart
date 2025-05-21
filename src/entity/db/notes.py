from pydantic import Field

from src.pkg.abc.entity import Entity, FieldEntity

from .types.notes import NotesCustomTyping, NotesTyping


class NotesEntity(Entity):
    """Database entity representing notes with all core fields.

    This entity defines the complete structure for notes stored in the database,
    including all required fields with proper type validation. It serves as the
    primary entity for note-related database operations and ensures data integrity
    through field validation.

    The entity contains all essential note attributes including identification,
    content, timestamps, and deletion status, making it suitable for full CRUD
    operations on notes.

    Attributes:
        id: Unique identifier field entity
        name: Note title/name field entity
        content: Note body/content field entity
        date_create: Creation timestamp field entity
        date_update: Last update timestamp field entity
        deleted: Soft deletion flag field entity

    Examples:
        # Create note fields for database operations
        note_id = NotesEntity.id(id=123)
        note_name = NotesEntity.name(name="My Note")
        note_content = NotesEntity.content(content="Note body text")
    """

    class id(FieldEntity):
        """Note unique identifier field entity.

        Attributes:
            id (NotesTyping.id): Primary key identifier for the note
        """

        id: NotesTyping.id = Field(...)

    class name(FieldEntity):
        """Note title/name field entity.

        Attributes:
            name (NotesTyping.name): Display name or title of the note
        """

        name: NotesTyping.name = Field(...)

    class content(FieldEntity):
        """Note content/body field entity.

        Attributes:
            content (NotesTyping.content): Main text content of the note
        """

        content: NotesTyping.content = Field(...)

    class date_create(FieldEntity):
        """Note creation timestamp field entity.

        Attributes:
            date_create (NotesTyping.date_create): When the note was created
        """

        date_create: NotesTyping.date_create = Field(...)

    class date_update(FieldEntity):
        """Note last update timestamp field entity.

        Attributes:
            date_update (NotesTyping.date_update): When the note was last modified
        """

        date_update: NotesTyping.date_update = Field(...)

    class deleted(FieldEntity):
        """Note soft deletion flag field entity.

        Attributes:
            deleted (NotesTyping.deleted): Boolean flag indicating if note is deleted
        """

        deleted: NotesTyping.deleted = Field(...)


class NotesCustomEntity(Entity):
    """Custom database entity for optional note fields and operations.

    This entity provides optional field variants for notes, typically used in
    scenarios where certain fields may or may not be present, such as search
    operations, partial updates, or conditional queries.

    All fields in this entity are optional (default None) allowing for flexible
    usage in various database operations that don't require all note fields.

    Attributes:
        name_op: Optional note name field entity
        date_create_op: Optional note creation date field entity

    Examples:
        # Create optional note fields for search operations
        optional_name = NotesCustomEntity.name_op(name="Search Term")
        optional_date = NotesCustomEntity.date_create_op(date_create=datetime.now())

        # Or create with None values for flexible queries
        empty_name = NotesCustomEntity.name_op(name=None)
    """

    class name_op(FieldEntity):
        """Optional note name field entity for custom operations.

        Attributes:
            name (NotesCustomTyping.name): Optional note name, defaults to None
        """

        name: NotesCustomTyping.name = Field(None)

    class date_create_op(FieldEntity):
        """Optional note creation date field entity for custom operations.

        Attributes:
            date_create (NotesCustomTyping.date_create): Optional creation date, defaults to None
        """

        date_create: NotesCustomTyping.date_create = Field(None)
