import pytest
from httpx import AsyncClient

from config import config


@pytest.mark.asyncio
async def test_create_patient(ac: AsyncClient, get_json_data) -> None:
    response = await ac.post(
        "/patient/add",
        auth=(config.DOCTOR_LOGIN, config.DOCTOR_PASSWORD),
        json=get_json_data
    )
    assert response.status_code == 200
    for key in get_json_data:
        assert get_json_data[key] == response.json()[key]


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
async def test_get_patient_by_id(ac: AsyncClient, get_json_data) -> None:
    # create patient
    response = await ac.post(
        "/patient/add",
        auth=(config.DOCTOR_LOGIN, config.DOCTOR_PASSWORD),
        json=get_json_data
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


@pytest.mark.asyncio
async def test_file_upload(
        ac: AsyncClient,
        get_json_data,
        get_random_file,
        s3_client
) -> None:
    # create a new patient
    response = await ac.post(
        '/patient/add',
        auth=(config.DOCTOR_LOGIN, config.DOCTOR_PASSWORD),
        json=get_json_data
    )

    patient_id = response.json().get('id')
    assert patient_id

    with open(get_random_file, 'rb') as f:
        # now upload file through API, to a newly created patient
        response = await ac.post(
            f'/patient/files/{patient_id}',
            auth=(config.DOCTOR_LOGIN, config.DOCTOR_PASSWORD),
            files=[('file', f)]
        )
    assert response.status_code == 200

    s3_link: str = response.json()
    s3_file_path = s3_link.split(sep='//')[1]
    s3_bucket, s3_key = s3_file_path.split(sep='/', maxsplit=1)

    assert await s3_client.object_exists(bucket=s3_bucket, s3_key=s3_key)
