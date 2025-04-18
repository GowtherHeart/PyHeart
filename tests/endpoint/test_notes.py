import json
from uuid import uuid4

import pytest
from starlette import status

from src.models.db.notes import NoteCoreModel
from tests.pkg.utils import get_client


@pytest.mark.asyncio
async def test_get(note: NoteCoreModel):
    async with get_client() as client:
        response = await client.get(f"/v1/notes/", params={"name": note.name})
        assert response.status_code == status.HTTP_200_OK

        body = response.json()
        assert body[0]["name"] == note.name


@pytest.mark.asyncio
async def test_create_notes():
    async with get_client() as client:
        data = {
            "content": "string",
            "name": uuid4().hex,
        }
        response = await client.post(f"/v1/notes/", content=json.dumps(data))
        assert response.status_code == status.HTTP_201_CREATED
