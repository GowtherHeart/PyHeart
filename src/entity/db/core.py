from pydantic import Field

from src.pkg.abc.entity import Entity, FieldEntity

from .types.core import CoreTyping


class CoreEntity(Entity):
    """Core database entity providing pagination and query constraint fields."""

    class limit(FieldEntity):
        """Field entity for database query result limiting."""

        limit: CoreTyping.limit = Field(...)

    class offset(FieldEntity):
        """Field entity for database query result offsetting."""

        offset: CoreTyping.offset = Field(...)
