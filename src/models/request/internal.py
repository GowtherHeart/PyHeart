from src.entity.db.core import CoreEntity
from src.entity.db.internal import InternalPostgresCustomEntity, InternalPostgresEntity
from src.pkg.abc.model import ParamsModel, PayloadModel


class PgPrmModel(
    ParamsModel,
    InternalPostgresCustomEntity.name_op,
    CoreEntity.limit,
    CoreEntity.offset,
): ...


class PgCreatePldModel(
    PayloadModel,
    InternalPostgresEntity.name,
    InternalPostgresEntity.value,
): ...


class PgPldModel(
    PayloadModel,
    InternalPostgresEntity.name,
    InternalPostgresEntity.value,
): ...


class PgDeletePrmModel(
    ParamsModel,
    InternalPostgresEntity.name,
): ...
