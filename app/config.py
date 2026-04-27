from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    """
    app_name: str = "StayEase AI Agent"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/stayease"
    groq_api_key: str = "your_groq_api_key_here" # Placeholder

    class Config:
        env_file = ".env"

settings = Settings()
