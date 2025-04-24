from src.entity.db.internal import InternalPostgresEntity
from src.pkg.abc.model import DbModel

__all__ = ["InternalPostgresCoreModel"]


class InternalPostgresCoreModel(
    DbModel,
    InternalPostgresEntity.id,
    InternalPostgresEntity.name,
    InternalPostgresEntity.value,
): ...
