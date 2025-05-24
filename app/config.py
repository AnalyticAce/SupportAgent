from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    
    openai_api_key: str = 'your-default-api-key'
    openai_model: str = 'gpt-3.5-turbo'
    database_url: str = f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'support.db')}"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()