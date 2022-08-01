import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    ALEMBIC_DATABASE_URL: str
    MAIN_DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()

@lru_cache()
def get_settings():
    os.environ["ALEMBIC_DATABASE_URL"] = settings.ALEMBIC_DATABASE_URL
    return Settings()
