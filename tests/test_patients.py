import datetime
import uuid
import pytest
from httpx import AsyncClient

from config import config


@pytest.mark.asyncio
async def test_create_patient(ac: AsyncClient) -> None:
    data = {
        'first_name': uuid.uuid4().hex,
        'last_name': uuid.uuid4().hex,
        'birthdate': datetime.date.today().strftime("%Y-%m-%d")
    }

    response = await ac.post(
        "/patient/add",
        auth=(config.DOCTOR_LOGIN, config.DOCTOR_PASSWORD),
        json=data
    )
    assert response.status_code == 200
    for key in data:
        assert data[key] == response.json()[key]


@pytest.mark.asyncio
async def test_get_all_patients(ac: AsyncClient) -> None:
    # request all patients
    response = await ac.get(
        "/patients/all",
        auth=(config.DOCTOR_LOGIN, config.DOCTOR_PASSWORD)
    )

    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_get_patient_by_id(ac: AsyncClient) -> None:
    # prepare some data
    data = {
        'first_name': uuid.uuid4().hex,
        'last_name': uuid.uuid4().hex,
        'birthdate': datetime.date.today().strftime("%Y-%m-%d")
    }
    # create patient
    response = await ac.post(
        "/patient/add",
        auth=(config.DOCTOR_LOGIN, config.DOCTOR_PASSWORD),
        json=data
    )
    created_patient_id = response.json().get('id')
    assert created_patient_id

    # get patient by id
    response = await ac.get(
        f"/patient-by-id?patient_id={created_patient_id}",
        auth=(config.DOCTOR_LOGIN, config.DOCTOR_PASSWORD)
    )
    assert response.status_code == 200
    assert response.json()
    assert response.json().get('id') == created_patient_id
