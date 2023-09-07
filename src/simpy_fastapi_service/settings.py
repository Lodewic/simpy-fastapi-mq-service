from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings

# class Psycopg3Dsn(PostgresDsn):
#     """Subclass of PostgresDsn that also allows 'postgreql+psycopg' urls."""
#     allowed_schemes = {"postgresql+psycopg", *PostgresDsn.allowed_schemes}

class Settings(BaseSettings):
    TOKEN_SECRET_KEY: str = ""
    TOKEN_ALGORITHM: str = "HS256"
    TOKEN_EXPIRY_DAYS: int = 90
    PROJECT_NAME: str = "simpy_fastapi_service"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
