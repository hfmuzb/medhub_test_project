import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from db.models.base_model import Base


class Doctors(Base):
    __tablename__ = 'doctors_data'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String)
    password = Column(String)
