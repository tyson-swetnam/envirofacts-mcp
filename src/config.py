"""Configuration for EPA Envirofacts MCP tool."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    epa_api_base_url: str = "https://data.epa.gov/efservice"
    epa_request_timeout: int = 30
    epa_max_retries: int = 3
    epa_cache_ttl: int = 3600
    log_level: str = "INFO"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
