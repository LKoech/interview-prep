from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Singleton-pattern config — one instance shared across the app via DI."""

    app_name: str = "Interview Prep Coach"
    debug: bool = False
    redis_url: str = "redis://localhost:6379/0"

    model_config = {"env_file": ".env"}


# Singleton instance
settings = Settings()
