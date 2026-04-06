from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    app_name: str = "My FastAPI Application"
    API_V1_STR: str = "/api/v1"
      # Versão corrigida com 127.0.0.1 e @ escapado
    DATABASE_URL: str = "postgresql+asyncpg://root:Danu%401985@127.0.0.1:5432/faculdade"

    class Config:
      case_sensitive = True

settings: Settings = Settings()