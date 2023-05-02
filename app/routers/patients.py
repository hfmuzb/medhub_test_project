from typing import List, Optional

from fastapi import APIRouter, Request, Response, status, Depends, UploadFile, File
from pydantic.types import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.patients import CreatePatient, CreatePatientResponse, GetPatientResponse, PatientCondition
from dependencies.basic_auth import basic_auth
from dependencies.get_db import get_session

router = APIRouter()


@router.post("/patient/add", status_code=status.HTTP_200_OK, response_model=CreatePatientResponse)
async def create_new_patient(
        request: Request,
        response: Response,
        patient: CreatePatient,
        doctor: str = Depends(basic_auth),
        db_session: AsyncSession = Depends(get_session)
):

    return patient


@router.get("/patient", status_code=status.HTTP_200_OK, response_model=List[GetPatientResponse])
async def filter_patients(
        request: Request,
        response: Response,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        condition_title: Optional[str] = None,
        doctor: str = Depends(basic_auth),
        db_session: AsyncSession = Depends(get_session)
):
    """
    Get patients data based on given filters.
    """

    return


@router.get("/patient-by-id", status_code=status.HTTP_200_OK, response_model=GetPatientResponse)
async def get_patient_by_id(
        request: Request,
        response: Response,
        patient_id: UUID,
        doctor: str = Depends(basic_auth),
        db_session: AsyncSession = Depends(get_session)
):
    return


@router.put("/patient-history-update")
async def update_patient_history_by_id(
        request: Request,
        response: Response,
        patient_id: UUID,
        data: PatientCondition,
        doctor: str = Depends(basic_auth),
        db_session: AsyncSession = Depends(get_session)
):
    return


@router.delete("/patient/{patient_id}")
async def delete_patient_by_id(
        request: Request,
        response: Response,
        patient_id: UUID,
        doctor: str = Depends(basic_auth),
        db_session: AsyncSession = Depends(get_session)
):
    return


@router.post("/patient/data/{patient_id}")
async def upload_patient_data(
        request: Request,
        response: Response,
        patient_id: UUID,
        file: UploadFile = File(...),
        doctor: str = Depends(basic_auth),
        db_session: AsyncSession = Depends(get_session)
):
    return
