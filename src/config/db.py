"""
This module sets up the database configuration.

It utilizes Pydantic's BaseSettings for configuration management,
allowing settings to be read from environment variables and a .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    """
    Database configuration settings for the application.

    Attributes:
        model_config (SettingsConfigDict): Model config, loaded from .env file.
        data_file_name (str): Name of the preprocessed csv data file.
        database_path (str): Path to the database file.
    """

    model_config = SettingsConfigDict(
        env_file="config/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    data_file_name: str
    database_path: str


# Initializing settings and configure logging
db_settings = DbSettings()
