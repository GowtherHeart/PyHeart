from src.entity.db.internal import InternalPostgresEntity
from src.pkg.abc.model import ResponseModel

__all__ = ["InternalPgCoreRespModel"]


class InternalPgCoreRespModel(
    ResponseModel,
    InternalPostgresEntity.id,
    InternalPostgresEntity.name,
    InternalPostgresEntity.value,
): ...
