from pydantic import BaseModel


class Entity:
    """Abstract base class for database entities."""

    ...


class FieldEntity(BaseModel):
    """Pydantic-based entity class with automatic validation and serialization."""

    ...
