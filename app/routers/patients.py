from typing import List, Optional

from fastapi import APIRouter, Request, Response, Depends, UploadFile, File
from pydantic.types import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.patients import (
    CreatePatient, GetPatientResponse, PatientCondition, GetPatientsBasicData
)
from dependencies.basic_auth import basic_auth
from dependencies.get_db import get_session

from service.patients import (
    create_new_patient_service, get_patient_by_id_service, add_item_to_patient_history_service,
    delete_patient_by_id_service, get_all_patients_service, upload_patient_data_service, filter_patients_service,
    delete_history_item_by_id_service, delete_patient_file_service
)

router = APIRouter()


@router.post("/patient/add", response_model=GetPatientsBasicData)
async def create_new_patient(
        request: Request,
        response: Response,
        patient: CreatePatient,
        doctor: str = Depends(basic_auth),
        db_session: AsyncSession = Depends(get_session)
):
    new_patient = await create_new_patient_service(
        patient=patient,
        doctor=doctor,
        db_session=db_session
    )

    return new_patient


@router.get("/patients/all", response_model=List[GetPatientsBasicData])
async def get_all_patients(
        request: Request,
        response: Response,
        limit: Optional[int] = None,
        doctor: str = Depends(basic_auth),
        db_session: AsyncSession = Depends(get_session)
):
    res = await get_all_patients_service(
        limit=limit,
        db_session=db_session
    )
    return res


@router.get("/filter-patients", response_model=List[UUID])
async def filter_patients(
        request: Request,
        response: Response,
        name: Optional[str] = None,
        condition_title: Optional[str] = None,
        doctor: str = Depends(basic_auth),
        db_session: AsyncSession = Depends(get_session)
):
    """
    Get patients data based on given filters.
    """
    res = await filter_patients_service(
        name=name,
        condition_title=condition_title,
        db_session=db_session
    )
    return res


@router.get("/patient-by-id", response_model=GetPatientResponse)
async def get_patient_by_id(
        request: Request,
        response: Response,
        patient_id: UUID,
        doctor: str = Depends(basic_auth),
        db_session: AsyncSession = Depends(get_session)
):
    res = await get_patient_by_id_service(
        patient_id=patient_id,
        db_session=db_session
    )
    return res


@router.put("/patient-history-add-item")
async def add_item_to_patient_history(
        request: Request,
        response: Response,
        patient_id: UUID,
        data: PatientCondition,
        doctor: str = Depends(basic_auth),
        db_session: AsyncSession = Depends(get_session)
):
    item = await add_item_to_patient_history_service(
        patient_id=patient_id,
        data=data,
        doctor=doctor,
        db_session=db_session
    )
    return item


@router.delete("/patient-history")
async def delete_history_item_by_id(
        request: Request,
        response: Response,
        item_id: UUID,
        doctor: str = Depends(basic_auth),
        db_session: AsyncSession = Depends(get_session)
):
    await delete_history_item_by_id_service(
        item_id=item_id,
        db_session=db_session
    )
    return


@router.delete("/patient/{patient_id}")
async def delete_patient_by_id(
        request: Request,
        response: Response,
        patient_id: UUID,
        doctor: str = Depends(basic_auth),
        db_session: AsyncSession = Depends(get_session)
):
    await delete_patient_by_id_service(
        patient_id=patient_id,
        db_session=db_session
    )
    return


@router.post("/patient/files/{patient_id}")
async def upload_patient_data(
        request: Request,
        response: Response,
        patient_id: UUID,
        file: UploadFile = File(...),
        doctor: str = Depends(basic_auth),
        db_session: AsyncSession = Depends(get_session)
):
    res = await upload_patient_data_service(
        patient_id=patient_id,
        doctor=doctor,
        data_type='',
        tags=[],
        file=file,
        db_session=db_session
    )
    return res


@router.delete("/patient/files/delete")
async def delete_patient_file_by_id(
        request: Request,
        response: Response,
        item_id: UUID,
        doctor: str = Depends(basic_auth),
        db_session: AsyncSession = Depends(get_session)
):
    await delete_patient_file_service(
        item_id=item_id,
        db_session=db_session
    )
    return
