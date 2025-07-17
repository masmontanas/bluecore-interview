from pydantic_settings import BaseSettings
from functools import lru_cache
import yaml
import os
from pathlib import Path


class Settings(BaseSettings):
    """
    All application settings are defined here.
    """
    redis_url: str
    redis_max_connections: int = 10
    log_level: str = "INFO"
    redis_failure_threshold: int = 3
    redis_recovery_time: int = 5

@lru_cache()
def get_settings(
        config_env_key: str = "APP_ENV",
        config_env: str = "default",
        config_file_name: str = "config.yaml"
) -> Settings:
    """
    config.yaml is used to define the configuration for each environment.
    The key for each configuration block in the yaml file denotes the environment,
    and the APP_ENV environment variable is used to select the correct environment at runtime.
    """
    env = os.getenv(config_env_key, config_env)
    file_name = config_file_name
    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / file_name

    with open(config_path) as f:
        data = yaml.safe_load(f)

    if env not in data:
        raise ValueError(f"Environment '{env}' not found in config.yaml")

    return Settings(**data[env])
