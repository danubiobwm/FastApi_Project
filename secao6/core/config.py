from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
    )

    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "postgresql+asyncpg://root:Danu%401985@127.0.0.1:5432/faculdade"
    JWT_SECRET: str = "Danu%401985"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7


settings: Settings = Settings()

