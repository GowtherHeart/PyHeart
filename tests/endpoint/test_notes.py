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
        assert body["payload"][0]["name"] == note.name


@pytest.mark.asyncio
async def test_create_notes():
    async with get_client() as client:
        data = {
            "content": "string",
            "name": uuid4().hex,
        }
        response = await client.post(f"/v1/notes/", content=json.dumps(data))
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_delete_note():
    async with get_client() as client:
        data = {
            "content": "string",
            "name": uuid4().hex,
        }
        create_response = await client.post(f"/v1/notes/", content=json.dumps(data))
        assert create_response.status_code == status.HTTP_201_CREATED

        delete_response = await client.delete(
            f"/v1/notes/", params={"name": create_response.json()["payload"]["name"]}
        )
        assert delete_response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_patch_note():
    async with get_client() as client:
        data = {
            "content": "string",
            "name": uuid4().hex,
        }
        create_response = await client.post(f"/v1/notes/", content=json.dumps(data))
        assert create_response.status_code == status.HTTP_201_CREATED

        patch_data = {
            "content": "updated content",
            "name": create_response.json()["payload"]["name"],
        }
        patch_response = await client.patch(
            f"/v1/notes/", content=json.dumps(patch_data)
        )
        assert patch_response.status_code == status.HTTP_200_OK

        get_response = await client.get(f"/v1/notes/", params={"name": data["name"]})
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["payload"][0]["content"] == patch_data["content"]
