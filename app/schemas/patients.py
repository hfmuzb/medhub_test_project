from typing import Optional, List
from datetime import date
from pydantic import BaseModel
from pydantic.schema import UUID


class BasePatient(BaseModel):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class PatientCondition(BaseModel):
    condition_title: Optional[str] = None
    condition_details: Optional[str] = None

    class Config:
        orm_mode = True


class PatientConditionResponse(PatientCondition):
    id: Optional[UUID] = None


class PatientFiles(BaseModel):
    id: Optional[UUID] = None
    uploaded_by_doctor: Optional[UUID] = None
    data_url: Optional[str] = None

    class Config:
        orm_mode = True


class CreatePatient(BasePatient):
    birthdate: date


class GetPatientResponse(BasePatient):
    id: UUID
    birthdate: date
    patient_condition: List[PatientConditionResponse]
    patient_files: List[PatientFiles]


class GetPatientsBasicData(BasePatient):
    id: UUID
    birthdate: date
