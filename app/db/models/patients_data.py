import uuid

from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from db.models.base_model import Base


class PatientsData(Base):
    __tablename__ = 'patients_data'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey('patients.id'))
    uploaded_by_doctor = Column(UUID(as_uuid=True), ForeignKey('doctors_data.id'))
    data_type = Column(String)
    tags = Column(ARRAY(String))
    data_url = Column(String)
    uploaded_at = Column(DateTime(), nullable=False, server_default=func.now())
