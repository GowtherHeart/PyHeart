from pydantic import BaseModel


class Entity:
    """
    Represents an entity used for registration in a database or other field types.
    This class serves as a base for defining entities with specific attributes
    and behaviors required for database operations or other field-related tasks.
    """

    ...


class FieldEntity(BaseModel):
    """
    Represents a field entity with attributes and validation rules.
    This class is used to define the structure and constraints of a field
    within a database or application context, leveraging Pydantic for data validation.
    """

    ...
