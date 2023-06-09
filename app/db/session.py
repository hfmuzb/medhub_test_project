from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import config

DB_STRING = config.DB_STRING

engine = create_async_engine(DB_STRING, echo=True, future=True)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
