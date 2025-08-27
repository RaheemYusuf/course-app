"""
This module provides functionality for managing a ML model.

It contains the ModelService class, which handles loading and using
a pre-trained ML model. The class offers methods to load a model
from a file, building it if doesn't exit, and to make predictions
using the loaded model.
"""

import pickle as pk
from pathlib import Path

import pandas as pd
from loguru import logger

from config import model_settings
from model.pipeline.model import build_model


class ModelService:
    """
    A service class for managing the ML model.

    This class provides functionalities to load a ML model from
    a specified path, build it if it doesn't exist, and make
    predictions using the loaded model.

    Attributes:
        model: ML model managed by this service. Initially set to None.

    Methods:
        __init__(): Constructor that initializes the ModelService.
        load_model(): Loads the model from file or builds it if doesn't exist.
        predict(): Makes a prediction using the loaded model.
    """

    def __init__(self):
        """Initializes the ModelService with no model loaded."""
        self.model = None

    def load_model(self):
        """
        Loads the model from a specified path,
        or builds it if it doen't exist.
        """
        logger.info(
            f'checking the existence of the model config file at '
            f'{model_settings.model_path}/{model_settings.model_name}',
        )

        model_path = Path(
            f'{model_settings.model_path}/{model_settings.model_name}',
        )

        if not model_path.exists():
            logger.warning(
                f'model at {model_path} was not found -> '
                f'building {model_settings.model_name} model',
            )
            build_model()

        logger.info(
            f'model {model_settings.model_name} exists! --> '
            'loading model config file',
        )

        with open(model_path, 'rb') as model_file:
            self.model = pk.load(model_file)

    def predict(self, input_parameters: list):
        """
        Makes a prediction using the loaded model.

        Takes input parameters and passes it to the model, which
        was loaded using a pickle file.

        Args:
            input_parameters (list): The input data for making a prediction.

        Returns:
            list: The prediction result from the model.
        """
        logger.info('making prediction!')
        return self.model.predict(pd.DataFrame([input_parameters]))
