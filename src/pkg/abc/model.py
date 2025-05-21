from pydantic import BaseModel


class DbModel(BaseModel):
    """Base Pydantic model for database operations and data persistence.

    This class serves as the foundation for all database-related models in the
    application. It provides type-safe data structures for database operations
    including queries, inserts, updates, and deletes.

    The model handles:
    - Database field validation
    - Type coercion for database operations
    - Serialization for database storage
    - Data integrity constraints

    Examples:
        class UserDbModel(DbModel):
            id: Optional[int] = None
            username: str
            email: str
            created_at: Optional[datetime] = None
    """


class ParamsModel(BaseModel):
    """Base Pydantic model for HTTP request parameters and query parameters.

    This class provides a foundation for validating and parsing URL parameters,
    query strings, and path parameters in HTTP requests. It ensures type safety
    and validation for incoming request parameters.

    Features:
    - Automatic parameter validation
    - Type coercion from string values
    - Default value handling
    - Custom validation rules

    Examples:
        class UserParamsModel(ParamsModel):
            user_id: int
            include_deleted: bool = False
            limit: int = Field(default=10, ge=1, le=100)
    """


class PayloadModel(BaseModel):
    """Base Pydantic model for HTTP request payloads and body data.

    This class serves as the foundation for validating and parsing JSON payloads
    in HTTP POST, PUT, and PATCH requests. It ensures data integrity and type
    safety for incoming request bodies.

    Features:
    - JSON schema validation
    - Nested object validation
    - Custom field validators
    - Automatic type conversion
    - Required/optional field handling

    Examples:
        class CreateUserPayloadModel(PayloadModel):
            username: str = Field(min_length=3, max_length=50)
            email: EmailStr
            password: str = Field(min_length=8)
            profile: Optional[UserProfileModel] = None
    """


class ResponseModel(BaseModel):
    """Base Pydantic model for HTTP response data and API responses.

    This class provides a foundation for structuring and validating API response
    data. It ensures consistent response formatting, type safety, and automatic
    JSON serialization for client consumption.

    Features:
    - Consistent response structure
    - Automatic JSON serialization
    - Response schema generation
    - Type-safe response building
    - Custom serialization rules

    Examples:
        class UserResponseModel(ResponseModel):
            id: int
            username: str
            email: str
            created_at: datetime

            class Config:
                json_encoders = {
                    datetime: lambda v: v.isoformat()
                }
    """


class Model(BaseModel):
    """Generic base Pydantic model for general-purpose data structures.

    This class serves as a catch-all base model for data structures that don't
    fit into the more specific model categories (DbModel, ParamsModel, etc.).
    It provides basic Pydantic functionality for any data validation needs.

    Use this class when you need a simple Pydantic model for:
    - Internal data transfer objects
    - Configuration structures
    - Temporary data containers
    - Generic validation needs

    Examples:
        class ConfigModel(Model):
            debug: bool = False
            timeout: int = 30
            features: List[str] = []
    """

    ...
