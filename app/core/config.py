from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AgentForge"
    app_version: str = "0.1.0"
    debug: bool = False
    secret_key: str = "your-secret-key"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()