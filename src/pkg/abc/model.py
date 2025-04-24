from pydantic import BaseModel


class DbModel(BaseModel):
    """
    Base model for database interactions.
    """


class ParamsModel(BaseModel):
    """
    Model for handling request params.
    """


class PayloadModel(BaseModel):
    """
    Model for handling request payloads.
    """


class ResponseModel(BaseModel):
    """
    Model for handling response payloads.
    """


class Model(BaseModel): ...
