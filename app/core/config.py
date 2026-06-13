from functools import lru_cache
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    app_name: str = "PharmaTrainerAI"
    app_version: str = "0.1.0"
    app_description: str = (
        "AI-enhanced gamified training platform for smart pharmaceutical manufacturing"
    )

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()