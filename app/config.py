from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory by looking for pyproject.toml"""
    
    current_path = Path(__file__).resolve()
    
    for parent in [current_path] + list(current_path.parents):
        if (parent / "pyproject.toml").exists():
            return parent
    
    return current_path.parent


def get_data_dir() -> Path:
    """Get the data directory and ensure it exists"""
    
    data_dir = get_project_root() / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


class Settings(BaseSettings):
    """Application settings for SupportAgent API."""
    
    openai_api_key: str = 'your-default-api-key'
    openai_model: str = 'gpt-3.5-turbo'
    openai_embedding_model_name: str = 'text-embedding-3-small'
    
    # PostgreSQL configuration
    postgres_host: str = 'localhost'
    postgres_port: int = 5432
    postgres_user: str = 'supportagent'
    postgres_password: str = 'password'
    postgres_db: str = 'supportagent'
    
    @property
    def database_url(self) -> str:
        """Construct the database URL for PostgreSQL with pgvector support."""
        
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()