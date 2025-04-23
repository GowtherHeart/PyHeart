import json
from typing import Any, Mapping

from fastapi import BackgroundTasks
from fastapi.responses import Response


class MasterResponse(Response):
    """
    A custom response class for FastAPI that extends the standard Response class.

    Attributes:
        media_type (str): The media type of the response, default is "application/json".
        status_code (int): The HTTP status code of the response, default is 200.
        content (Any): The content of the response, stored for custom processing before rendering.
        background (BackgroundTasks | None): Background tasks to be run after the response is sent.

    Methods:
        render(content: Any) -> bytes: Renders the content to a JSON-encoded byte string.
    """

    media_type = "application/json"

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTasks | None = None,
    ) -> None:

        self.status_code = status_code
        if media_type is not None:
            self.media_type = media_type

        self.background = background

        # self.body = self.render(content)
        self.custom_content = content
        self.init_headers(headers)

    def render(self, content: Any) -> bytes:
        return json.dumps(content).encode("utf-8")
