"""
This module provides functionalities to load data from the database
or a CSV file.

It includes a function to extract data from a DuckDB database
or load it from a CSV file, returning a pandas DataFrame. This
module is part of the data collection process in the ML pipeline.
"""

from loguru import logger
import pandas as pd

from config import db_settings
from db.duckdb_data import query_data


def load_data():
    data_path = db_settings.data_file_name
    try:
        logger.info(f"Loading data from {data_path}")
        return pd.read_csv(data_path)
    except Exception as e:
        print(f"Error loading data: {e}")  # noqa: WPS421
        return None


def load_data_from_db() -> pd.DataFrame:
    """
    Loads data from a DuckDB database and returns it as a pandas DataFrame.
    """
    logger.info("Loading data from DuckDB database")
    return query_data()
