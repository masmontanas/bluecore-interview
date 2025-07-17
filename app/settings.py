from pydantic_settings import BaseSettings
from functools import lru_cache
import yaml
import os
from pathlib import Path


class Settings(BaseSettings):
    """
    All application settings are defined here.
    Environment variables can override values in config.yaml.
    """
    redis_url: str
    redis_max_connections: int = 10
    log_level: str = "INFO"
    redis_failure_threshold: int = 3
    redis_recovery_time: int = 5

    class Config:
        env_prefix = ""  # No prefix needed; keys match env var names
        case_sensitive = False


@lru_cache()
def get_settings(
    config_env_key: str = "APP_ENV",
    config_env: str = "default",
    config_file_name: str = "config.yaml"
) -> Settings:
    """
    Loads settings from config.yaml for the specified environment (APP_ENV).
    Environment variables take precedence over config file values so that k8s secrets
    can be exposed as environment variables at runtime for sensitive values.
    """
    env = os.getenv(config_env_key, config_env)
    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / config_file_name

    with open(config_path) as f:
        data = yaml.safe_load(f)

    if env not in data:
        raise ValueError(f"Environment '{env}' not found in {config_file_name}")

    return Settings(**data[env])
