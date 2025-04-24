# import sys
import asyncio
import os
from uuid import uuid4

import pytest

os.environ["TESTING"] = "true"


# if sys.platform == "linux":
#     asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())


@pytest.yield_fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


from src.pkg.context import make_tx_id
from tests.pkg.apps import HttpApp

make_tx_id()

#################################
### INIT APPS
#################################
HttpApp()


@pytest.fixture
async def note():
    from src.repository import notes as notes_repo

    return await notes_repo.CreateQuery(name=uuid4().hex, content=uuid4().hex).execute()


@pytest.fixture
async def task():
    from src.repository import tasks as task_repo

    return await task_repo.CreateQuery(name=uuid4().hex, content=uuid4().hex).execute()
