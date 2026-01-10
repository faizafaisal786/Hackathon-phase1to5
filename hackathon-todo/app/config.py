"""
Application configuration using Pydantic settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str

    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Application
    app_name: str = "Hackathon Todo API"
    debug: bool = False

    # OpenAI (Optional - for AI chat feature)
    openai_api_key: Optional[str] = "demo"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"  # Allow extra fields from .env


settings = Settings()
