import json
from typing import Any, Mapping

from fastapi import BackgroundTasks
from fastapi.responses import Response


class MasterResponse(Response):
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
