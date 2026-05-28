from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"
    database_url: str = ""
    redis_url: str = "redis://localhost:6379"
    clerk_secret_key: str = ""
    sleeper_api_base_url: str = "https://api.sleeper.app/v1"


settings = Settings()