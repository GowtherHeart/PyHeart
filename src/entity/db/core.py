from pydantic import Field

from src.pkg.abc.entity import Entity, FieldEntity

from .types.core import CoreTyping


class CoreEntity(Entity):

    class limit(FieldEntity):
        limit: CoreTyping.limit = Field(...)

    class offset(FieldEntity):
        offset: CoreTyping.offset = Field(...)
