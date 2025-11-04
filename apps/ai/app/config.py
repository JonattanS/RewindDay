from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Server
    port: int = 8000
    environment: str = "development"
    
    # OpenAI (opcional)
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        # Para Pydantic v2
        extra = "ignore"


# Instancia global de configuración
settings = Settings()
