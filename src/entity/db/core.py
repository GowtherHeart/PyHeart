from pydantic import Field

from src.pkg.abc.entity import Entity, FieldEntity

from .types.core import CoreTyping


class CoreEntity(Entity):
    """
    CoreEntity is a subclass of Entity that defines two nested classes, limit and offset,
    each inheriting from FieldEntity. These classes represent fields with specific types
    defined in CoreTyping, and are used to enforce constraints on the values assigned to
    these fields.
    """

    class limit(FieldEntity):
        limit: CoreTyping.limit = Field(...)

    class offset(FieldEntity):
        offset: CoreTyping.offset = Field(...)
