from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SunOps SaaS"
    debug: bool = False

    database_url: str = "postgresql+asyncpg://sunops:sunops123@localhost:5432/sunops"
    database_url_sync: str = "postgresql://sunops:sunops123@localhost:5432/sunops"

    redis_url: str = "redis://localhost:6379/0"

    secret_key: str = "dev-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    google_maps_api_key: str = ""

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
