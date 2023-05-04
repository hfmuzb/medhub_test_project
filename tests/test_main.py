import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(ac: AsyncClient) -> None:
    response = await ac.get(
        "/",
    )
    assert 200 == response.status_code


@pytest.mark.asyncio
async def test_unathorized_request(ac: AsyncClient) -> None:
    response = await ac.get(
        "/patients/all"
    )
    assert response.status_code == 401
