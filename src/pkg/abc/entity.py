from pydantic import BaseModel


class Entity:
    """Abstract base class for database entities.

    This class serves as the foundation for all database entity representations
    in the application. Entities are domain objects that have a distinct identity
    and lifecycle, typically corresponding to database tables or document collections.

    The Entity class provides a common interface for database operations and
    ensures consistent behavior across different entity types. It handles
    basic entity concerns like identity management and persistence lifecycle.

    Examples:
        class UserEntity(Entity):
            def __init__(self, user_id: int, name: str):
                self.id = user_id
                self.name = name
    """

    ...


class FieldEntity(BaseModel):
    """Pydantic-based entity class with automatic validation and serialization.

    This class extends Pydantic's BaseModel to provide type-safe entity
    definitions with automatic validation, serialization, and deserialization.
    It's used for entities that require strict data validation and type checking.

    The class automatically handles:
    - Field validation based on type annotations
    - JSON serialization/deserialization
    - Data parsing and transformation
    - Schema generation for API documentation

    Examples:
        class UserFieldEntity(FieldEntity):
            id: int
            name: str
            email: EmailStr
            created_at: datetime
    """

    ...
