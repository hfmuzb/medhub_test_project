import uuid

from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from db.models.base_model import Base


class PatientsHistory(Base):
    __tablename__ = 'patients_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'))
    condition_title = Column(String)
    condition_details = Column(String)
    created_at = Column(DateTime(), nullable=False, server_default=func.now())
