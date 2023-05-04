import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient

from main import app


@pytest.yield_fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def my_app(event_loop):
    return app


@pytest_asyncio.fixture(scope="function")
async def ac(my_app):
    async with AsyncClient(app=my_app, base_url="http://test") as c:
        yield c
