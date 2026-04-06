from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from typing import ClassVar
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    # Versão corrigida com 127.0.0.1 e @ escapado
    DB_URL: str = "postgresql+asyncpg://root:Danu%401985@127.0.0.1:5432/faculdade"

    DBBaseModel: ClassVar = declarative_base()

    class Config:
        case_sensitive = True

settings = Settings()