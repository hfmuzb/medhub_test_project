import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID, DATE

from db.models.base_model import Base


class Patients(Base):
    __tablename__ = 'patients'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    birthdate = Column(DATE)
