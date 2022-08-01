import os

import loguru
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings

SQLALCHEMY_DATABASE_URL = get_settings().MAIN_DATABASE_URL

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, future=True
)


async def get_db() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

Base = declarative_base()
