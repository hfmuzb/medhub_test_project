"""add dummy doctor record

Revision ID: 5776c94449bd
Revises: 6048ae2a7bcb
Create Date: 2023-05-03 13:26:27.391843

"""
import uuid

from alembic import op
import sqlalchemy as sa

from config import config

# revision identifiers, used by Alembic.
revision = '5776c94449bd'
down_revision = '6048ae2a7bcb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    doctor_id = uuid.uuid4()

    op.execute(
        f"INSERT INTO DOCTORS_DATA "
        f"VALUES ('{doctor_id}', '{config.DOCTOR_LOGIN}', '{config.DOCTOR_PASSWORD}');"
    )


def downgrade() -> None:
    pass
