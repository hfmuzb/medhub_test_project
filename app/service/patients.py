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


async def filter_patients_service():
    return


async def get_patient_by_id_service(
        patient_id: UUID,
        db_session: AsyncSession
):
    patient = await db_session.execute(
        select(Patient).filter(Patient.id == patient_id).first()
    )
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
        patient_condition=patient_conditions,
        **patient.dict()
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
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    patient_history = await db_session.execute(select(PatientsHistory).filter(PatientsHistory.patient_id == patient_id))
    await db_session.delete(patient_history)
    await db_session.delete(patient)
    await db_session.flush()
    return


async def upload_patient_data_service():
    return
