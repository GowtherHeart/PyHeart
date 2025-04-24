from pydantic import Field

from src.pkg.abc.entity import Entity, FieldEntity

from .types.internal import InternalPgCustomTyping, InternalPgTyping


class InternalPostgresEntity(Entity):

    class id(FieldEntity):
        id: InternalPgTyping.id = Field(...)

    class name(FieldEntity):
        name: InternalPgTyping.name = Field(...)

    class value(FieldEntity):
        value: InternalPgTyping.value = Field(...)


class InternalPostgresCustomEntity(Entity):

    class name_op(FieldEntity):
        name: InternalPgCustomTyping.name = Field(...)
