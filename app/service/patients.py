from fastapi import HTTPException, status
from pydantic.types import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.patients import CreatePatient, GetPatientResponse, PatientCondition
from db.models.patients import Patient
from db.models.patients_history import PatientsHistory


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
    patients = await db_session.execute(
        select(Patient).limit(limit)
    )
    patients = patients.scalars().all()
    if not patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return [patient for patient in patients]


async def filter_patients_service():
    # TODO
    return


async def get_patient_by_id_service(
        patient_id: UUID,
        db_session: AsyncSession
):
    patient = await db_session.execute(
        select(Patient).filter(Patient.id == patient_id)
    )
    patient = patient.first()[0]
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    patients_history = await db_session.execute(
        select(PatientsHistory).filter(PatientsHistory.patient_id == patient_id)
    )

    patients_history = patients_history.scalars().all()

    patient_conditions = [PatientsHistory(patient_id=record.patient_id,
                                          condition_title=record.condition_title,
                                          condition_details=record.condition_details,
                                          created_at=record.created_at)
                          for record in patients_history
                          ]

    result = GetPatientResponse(
        id=patient.id,
        first_name=patient.first_name,
        last_name=patient.last_name,
        birthdate=patient.birthdate,
        patient_condition=patient_conditions
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


async def delete_patient_by_id_service(
        patient_id: UUID,
        db_session: AsyncSession
):
    patient = await db_session.execute(select(Patient).filter(Patient.id == patient_id))
    patient = patient.scalar()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    patients_history = await db_session.execute(
        select(PatientsHistory).filter(PatientsHistory.patient_id == patient_id)
    )
    patients_history = patients_history.all()
    for item in patients_history:
        await db_session.delete(item[0])
    await db_session.commit()
    await db_session.delete(patient)
    await db_session.commit()
    return


async def upload_patient_data_service():
    # TODO
    return
