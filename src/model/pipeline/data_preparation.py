"""
This module provides functionality for preparing a dataset for ML model.

It consists of functions to load data from a database,
encode categorical columns, and parse specific columns for further processing.
"""

import re

import pandas as pd
from loguru import logger

from model.pipeline.data_collection import load_data


def prepare_data():
    """
    Prepares the dataset for analysis and modeling.

    This involves loading the data, encoding cartegorical columns,
    and parsing the 'garden' column.

    Returns:
        df (pandas.DataFrame): The preprocessed DataFrame ready for modeling.
    """
    logger.info("Starting up preprocessing pipeline")
    dataframe = load_data()
    data_encoded = _encode_cat_cols(dataframe)
    return _parse_garden_cols(data_encoded)


def _encode_cat_cols(dataframe: pd.DataFrame):
    """
    Encodes categorical columns into dummy variaables.

    Args:
        data (pd.DataFrame): The original dataset.
    """
    cols = ["balcony", "parking", "furnished", "garage", "storage"]
    logger.info(f"Encoding categorical columns: {cols}")
    return pd.get_dummies(
        dataframe,
        columns=cols,
        drop_first=True,
    )


def _parse_garden_cols(dataframe: pd.DataFrame):
    """ "
    Parses the 'garden' column in the dataset.

    Args:
        data (pd.DataFrame): The dataset with the 'garden' column to be parsed.

    Returns:
        pd.DataFrame: The dataset with the parsed 'garden' column.
    """
    logger.info("Parsing garden column")
    dataframe["garden"] = dataframe["garden"].apply(
        lambda x: 0 if x == "Not present" else int(re.findall(r"\d+", x)[0]),
    )
    return dataframe
