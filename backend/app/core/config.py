from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "development"
    database_url: str = ""
    redis_url: str = "redis://localhost:6379"
    clerk_secret_key: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()