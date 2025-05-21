from pydantic import Field

from src.pkg.abc.entity import Entity, FieldEntity

from .types.core import CoreTyping


class CoreEntity(Entity):
    """Core database entity providing pagination and query constraint fields.

    This entity defines common pagination fields (limit and offset) that can be
    used across different database operations. It serves as a base for query
    parameters that need pagination support.

    The entity contains field definitions with type validation through CoreTyping
    to ensure proper constraint handling in database queries.

    Attributes:
        limit: Field entity for query result limiting
        offset: Field entity for query result offsetting

    Examples:
        # Create pagination parameters
        pagination = CoreEntity.limit(limit=10)
        offset_params = CoreEntity.offset(offset=20)
    """

    class limit(FieldEntity):
        """Field entity for database query result limiting.

        This nested class defines the limit field used for paginating query results.
        It enforces type validation and constraints through CoreTyping to ensure
        valid limit values are provided to database queries.

        Attributes:
            limit (CoreTyping.limit): Maximum number of results to return
        """

        limit: CoreTyping.limit = Field(...)

    class offset(FieldEntity):
        """Field entity for database query result offsetting.

        This nested class defines the offset field used for skipping records
        in paginated query results. It enforces type validation and constraints
        through CoreTyping to ensure valid offset values.

        Attributes:
            offset (CoreTyping.offset): Number of results to skip before returning data
        """

        offset: CoreTyping.offset = Field(...)
