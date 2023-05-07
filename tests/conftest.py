import asyncio
import datetime
import uuid
import pytest
import pytest_asyncio
from httpx import AsyncClient
import random
import string

from main import app
from service.storage import s3


@pytest.fixture(scope='session')
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


@pytest.fixture
def get_json_data():
    data = {
        'first_name': uuid.uuid4().hex,
        'last_name': uuid.uuid4().hex,
        'birthdate': datetime.date.today().strftime("%Y-%m-%d")
    }
    yield data


@pytest.fixture
def get_random_string(length: int = 1000):
    # random string for writing to a temp file
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    yield random_string


@pytest.fixture()
def get_random_file(get_random_string, tmp_path):
    d = tmp_path / 'sub'
    d.mkdir()
    file = d / 'temp.txt'
    file.write_text(get_random_string)
    yield file


@pytest.fixture
def s3_client():
    yield s3
