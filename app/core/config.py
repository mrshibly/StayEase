from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    """
    app_name: str = "StayEase AI Agent"
    database_url: str
    groq_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()
