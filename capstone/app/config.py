from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "sqlite+aiosqlite:///./learning_hub.db"
    jwt_secret_key: str = "local-development-only-change-before-deploy"
    access_token_minutes: int = 30
