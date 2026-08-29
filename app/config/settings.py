'''
This file centralizes configuration and reads values from .env when we create it
'''
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-5-mini"
    openai_reasoning_effort: str = "minimal"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = 'ai_tutor_documents'
    documents_dir: str = "data/documents"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()