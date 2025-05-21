from starlette import status

from src.entity.db.types.core import CoreTyping
from src.entity.db.types.internal import (
    InternalPgCustomTyping,
    InternalPgTyping,
)
from src.internal.fastapi.controller import HttpController
from src.models.request.internal import (
    PgCreatePldModel,
    PgDeletePrmModel,
    PgPldModel,
    PgPrmModel,
)
from src.models.response.internal import InternalPgCoreRespModel
from src.pkg.abc.controller import router
from src.usecase.internal import InternalPgV1US


class InternalPostgresSimpleControllerV1(HttpController):
    """Internal API controller for simple PostgreSQL operations without transactions.

    This controller provides internal/administrative endpoints for direct database
    operations without transaction management. These endpoints are intended for:
    - System administration and maintenance
    - Development and debugging purposes
    - Direct database operations that don't require transaction isolation

    ⚠️  WARNING: These are internal endpoints and should not be exposed to end users.
    They provide direct database access and bypass business logic validation.

    The controller handles:
    - GET /_internal/v1/postgres/simple/ - Retrieve internal records
    - POST /_internal/v1/postgres/simple/ - Create internal records
    - PATCH /_internal/v1/postgres/simple/ - Update internal records
    - DELETE /_internal/v1/postgres/simple/ - Delete internal records

    All operations are performed without transaction management for maximum
    performance and direct database access.

    Attributes:
        prefix (str): URL prefix for internal PostgreSQL endpoints
        tags (list[str]): OpenAPI tags for documentation grouping
    """

    prefix = "/v1/postgres/simple"
    tags = ["postgres"]

    @router(path="/", status_code=status.HTTP_200_OK)
    async def get(
        self,
        name: InternalPgCustomTyping.name = None,
        limit: CoreTyping.limit = 100,
        offset: CoreTyping.offset = 0,
    ) -> list[InternalPgCoreRespModel]:
        """Retrieve internal PostgreSQL records with optional filtering.

        This endpoint provides direct access to internal database records for
        administrative purposes. It supports filtering by name and pagination.

        ⚠️  Internal Use Only: This endpoint bypasses business logic and provides
        direct database access. Use with caution.

        Query Parameters:
            name (str, optional): Filter records by name. Supports partial matching.
                                 Example: ?name=config will match configuration records
            limit (int, optional): Maximum number of records to return. Default: 100
            offset (int, optional): Number of records to skip for pagination. Default: 0

        Returns:
            list[InternalPgCoreRespModel]: Array of internal records containing:
                - id: Unique identifier of the record
                - name: Name/key of the internal record
                - value: Value/data stored in the record
                - Additional internal fields as defined in the schema

        Status Codes:
            200: Records retrieved successfully
            400: Invalid query parameters
            500: Database error

        Example Request:
            GET /_internal/v1/postgres/simple/?name=config&limit=10

        Example Response:
            [
                {
                    "id": 1,
                    "name": "config.database.timeout",
                    "value": "30"
                },
                {
                    "id": 2,
                    "name": "config.cache.ttl",
                    "value": "3600"
                }
            ]
        """
        model = PgPrmModel(
            name=name,
            limit=limit,
            offset=offset,
        )
        result = await InternalPgV1US().get(model=model)
        return [InternalPgCoreRespModel(**e.model_dump()) for e in result]

    @router(path="/", status_code=status.HTTP_201_CREATED)
    async def post(self, payload: PgCreatePldModel) -> InternalPgCoreRespModel:
        result = await InternalPgV1US().create(payload=payload)
        return InternalPgCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def patch(self, payload: PgPldModel) -> InternalPgCoreRespModel:
        result = await InternalPgV1US().update(payload=payload)
        return InternalPgCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def delete(self, name: InternalPgTyping.name) -> InternalPgCoreRespModel:
        model = PgDeletePrmModel(
            name=name,
        )
        result = await InternalPgV1US().delete(model=model)
        return InternalPgCoreRespModel(**result.model_dump())


class InternalPostgresTransactionControllerV1(HttpController):
    """Internal API controller for PostgreSQL operations with transaction management.

    This controller provides internal/administrative endpoints for database
    operations with full transaction support. These endpoints ensure ACID
    properties and data consistency through proper transaction management.

    ⚠️  WARNING: These are internal endpoints and should not be exposed to end users.
    They provide direct database access with transaction guarantees.

    The controller handles:
    - POST /_internal/v1/postgres/transaction/ - Create records with transaction
    - PATCH /_internal/v1/postgres/transaction/ - Update records with transaction
    - DELETE /_internal/v1/postgres/transaction/ - Delete records with transaction

    All operations are wrapped in database transactions to ensure:
    - Atomicity: Operations either complete fully or not at all
    - Consistency: Database remains in valid state
    - Isolation: Concurrent operations don't interfere
    - Durability: Committed changes are permanent

    Attributes:
        prefix (str): URL prefix for transactional PostgreSQL endpoints
        tags (list[str]): OpenAPI tags for documentation grouping
    """

    prefix = "/v1/postgres/transaction"
    tags = ["postgres"]

    @router(path="/", status_code=status.HTTP_201_CREATED)
    async def post(self, payload: PgCreatePldModel) -> InternalPgCoreRespModel:
        result = await InternalPgV1US().create_tx(payload=payload)
        return InternalPgCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def patch(self, payload: PgPldModel) -> InternalPgCoreRespModel:
        result = await InternalPgV1US().update_tx(payload=payload)
        return InternalPgCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def delete(self, name: InternalPgTyping.name) -> InternalPgCoreRespModel:
        model = PgDeletePrmModel(
            name=name,
        )
        result = await InternalPgV1US().delete_tx(model=model)
        return InternalPgCoreRespModel(**result.model_dump())


class InternalPostgresTransactionExcControllerV1(HttpController):
    """Internal API controller for PostgreSQL operations with transaction management and enhanced exception handling.

    This controller provides internal/administrative endpoints for database operations
    with full transaction support and comprehensive exception handling. These endpoints
    are designed for testing transaction rollback scenarios and debugging database issues.

    ⚠️  WARNING: These are internal endpoints with intentional exception handling for
    testing purposes. They should not be exposed to end users.

    The controller handles:
    - POST /_internal/v1/postgres/transaction_exception/ - Create with exception handling
    - PATCH /_internal/v1/postgres/transaction_exception/ - Update with exception handling
    - DELETE /_internal/v1/postgres/transaction_exception/ - Delete with exception handling

    This controller is specifically designed to:
    - Test transaction rollback mechanisms
    - Simulate database error conditions
    - Validate exception handling in transactional contexts
    - Debug complex database operation scenarios

    All operations include enhanced error handling and detailed exception information
    for development and testing purposes.

    Attributes:
        prefix (str): URL prefix for exception-handling PostgreSQL endpoints
        tags (list[str]): OpenAPI tags for documentation grouping
    """

    prefix = "/v1/postgres/transaction_exception"
    tags = ["postgres"]

    @router(path="/", status_code=status.HTTP_201_CREATED)
    async def post(self, payload: PgCreatePldModel) -> InternalPgCoreRespModel:
        result = await InternalPgV1US().create_tx_exc(payload=payload)
        return InternalPgCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def patch(self, payload: PgPldModel) -> InternalPgCoreRespModel:
        result = await InternalPgV1US().update_tx_exc(payload=payload)
        return InternalPgCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def delete(self, name: InternalPgTyping.name) -> InternalPgCoreRespModel:
        model = PgDeletePrmModel(
            name=name,
        )
        result = await InternalPgV1US().delete_tx_exc(model=model)
        return InternalPgCoreRespModel(**result.model_dump())
