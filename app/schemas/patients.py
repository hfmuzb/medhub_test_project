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


class CreatePatient(BasePatient):
    birthdate: date


class CreatePatientResponse(BasePatient):
    pass


class GetPatientResponse(BasePatient):
    id: UUID
    birthdate: date
    patient_condition: List[PatientCondition]
