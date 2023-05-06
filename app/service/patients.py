from typing import Optional

import aiofiles
from fastapi import HTTPException, status, UploadFile
from pydantic.types import UUID
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.patients import CreatePatient, GetPatientResponse, PatientCondition
from db.models.patients import Patient
from db.models.patients_history import PatientsHistory
from db.models.patients_data import PatientsData
from db.models.doctors import Doctors
from service.storage import s3


async def create_new_patient_service(
        patient: CreatePatient,
        doctor: str,
        db_session: AsyncSession
):
    new_patient = Patient(
        first_name=patient.first_name,
        last_name=patient.last_name,
        birthdate=patient.birthdate
    )
    db_session.add(new_patient)
    await db_session.commit()
    await db_session.refresh(new_patient)
    return new_patient


async def get_all_patients_service(
        limit,
        db_session: AsyncSession
):
    patients = (
        await db_session.execute(
            select(Patient).limit(limit)
        )
    ).scalars().all()
    if not patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return [patient for patient in patients]


async def filter_patients_service(
        db_session: AsyncSession,
        name: Optional[str] = None,
        condition_title: Optional[str] = None
):
    # if neither name and condition is not provided, raise HTTPException
    if not (name or condition_title):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Please provide either name or condition title")
    patients_ids = []
    patients = (
        await db_session.execute(
            select(Patient).filter(
                Patient.first_name.like(name) | Patient.last_name.like(name)
            )
        )
    ).scalars()
    if not patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    for patient in patients.all():
        patients_ids.append(patient.id)

    return patients_ids


async def get_patient_by_id_service(
        patient_id: UUID,
        db_session: AsyncSession
):
    patient = (
        await db_session.execute(
            select(Patient).filter(Patient.id == patient_id)
        )
    ).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    patient = patient[0]

    patients_history = (
        await db_session.execute(
            select(PatientsHistory).filter(PatientsHistory.patient_id == patient_id)
        )
    ).scalars().all()

    patient_conditions = [PatientsHistory(id=record.id,
                                          patient_id=record.patient_id,
                                          condition_title=record.condition_title,
                                          condition_details=record.condition_details,
                                          created_at=record.created_at)
                          for record in patients_history
                          ]
    patient_files = (
        await db_session.execute(
            select(PatientsData).filter(PatientsData.patient_id == patient_id)
        )
    ).scalars().all()

    patient_files = [
        PatientsData(
            id=file.id,
            patient_id=file.patient_id,
            uploaded_by_doctor=file.uploaded_by_doctor,
            data_type=file.data_type,
            tags=file.tags,
            data_url=file.data_url,
            uploaded_at=file.uploaded_at
        )
        for file in patient_files
    ]

    result = GetPatientResponse(
        id=patient.id,
        first_name=patient.first_name,
        last_name=patient.last_name,
        birthdate=patient.birthdate,
        patient_condition=patient_conditions,
        patient_files=patient_files
    )
    return result


async def add_item_to_patient_history_service(
        patient_id: UUID,
        data: PatientCondition,
        doctor: str,
        db_session: AsyncSession
):
    new_item = PatientsHistory(
        patient_id=patient_id,
        condition_title=data.condition_title,
        condition_details=data.condition_details
    )
    db_session.add(new_item)
    await db_session.commit()
    await db_session.refresh(new_item)
    return new_item


async def delete_history_item_by_id_service(
        item_id: UUID,
        db_session: AsyncSession
):
    await db_session.execute(delete(PatientsHistory).filter(PatientsHistory.id == item_id))
    await db_session.commit()


async def delete_patient_by_id_service(
        patient_id: UUID,
        db_session: AsyncSession
):
    patient = (
        await db_session.execute(select(Patient).filter(Patient.id == patient_id))
    ).scalar()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    patients_history = (
        await db_session.execute(
            select(PatientsHistory).filter(PatientsHistory.patient_id == patient_id)
        )
    ).scalars().all()

    patients_files = (
        await db_session.execute(
            select(PatientsData).filter(PatientsData.patient_id == patient_id)
        )
    ).scalars().all()

    for item in patients_history:
        await db_session.delete(item)

    s3_links_to_delete = []
    for file_record in patients_files:
        s3_links_to_delete.append(file_record.data_url)
        await db_session.delete(file_record)

    await db_session.commit()
    await db_session.delete(patient)
    await db_session.commit()
    for link in s3_links_to_delete:
        await s3.remove_object(link)
    return


async def upload_patient_data_service(
        patient_id: UUID,
        doctor: str,
        data_type: str,
        tags: list,
        file: UploadFile,
        db_session: AsyncSession,
) -> str:
    doctor_id = (
        await db_session.execute(
            select(Doctors).filter(Doctors.login == doctor)
        )
    ).first()[0].id
    file_bytes = await file.read()
    async with aiofiles.tempfile.NamedTemporaryFile('wb') as f:
        await f.write(file_bytes)
        s3_link = await s3.upload(
            input_filepath=f.name,
            filename=file.filename,
            patient_id=patient_id
        )
    patient_data_item = PatientsData(
        patient_id=patient_id,
        uploaded_by_doctor=doctor_id,
        data_type=data_type,
        tags=tags,
        data_url=s3_link
    )
    db_session.add(patient_data_item)
    await db_session.commit()
    return s3_link
