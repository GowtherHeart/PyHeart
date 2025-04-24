class InternalPgTyping:
    type id = int
    type name = str
    type value = float


class InternalPgCustomTyping:
    type name = InternalPgTyping.name | None
    type value = InternalPgTyping.value | None
