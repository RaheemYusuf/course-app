"""
This module creates the pipeline for building, training and saving ML model.

It includes the process of data preparation, model training using
RandomFForestRegressor, hyperparameter tunning with GridSearchCV,
model evaluation, and serialization of the trained model to a file.
"""

import pickle as pk

import pandas as pd
from loguru import logger
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestRegressor

from config import model_settings
from model.pipeline.data_preparation import prepare_data


def build_model():
    """
    Builds, trains, evaluates, and saves a RandomForestRegressor model.

    This function orchestrates the model building pipepline.
    It starts by preparing the data, followed by defining feature names
    and splitting the dataset into features and target variables.
    The dataset is then divided into training and testing sets.
    The model's performance is evaluated on the test set, and
    finally, the model is saved for future use.
    """
    logger.info("starting up model building pipeline")
    df = prepare_data()
    feature_names = [
        "area",
        "constraction_year",
        "bedrooms",
        "garden",
        "balcony_yes",
        "parking_yes",
        "furnished_yes",
        "garage_yes",
        "storage_yes",
    ]
    X, y = _get_x_y(
        df,
        col_x=feature_names,
    )
    X_train, X_test, y_train, y_test = _split_train_test(X, y)
    rf = _train_model(
        X_train,
        y_train,
    )
    _evaluate_model(
        rf,
        X_test,
        y_test,
    )
    _save_model(rf)


def _get_x_y(
    dataframe: pd.DataFrame,
    col_x: list[str],
    col_y: str = "rent",
):
    """
    Split the dataset into features and target variable.

    Args:
        dataframe (pd.DataFrame): The preprocessed dataset.
        col_x (list[str]): List of feature column names.
        col_y (str): Name of the target variable column. Default is 'rent'.

    Returns:
        tuple: A tuple containing the features (X) and target variable (y).
    """

    logger.info(f"defining X and Y variables. X vars: {col_x}; y var: {col_y}")
    return dataframe[col_x], dataframe[col_y]


def _split_train_test(
    features: pd.DataFrame,
    target: pd.Series,
):
    """
    Split the data into training and testing sets.

    Args:
        X (pd.DataFrame): The feature set.
        y (pd.Series): The target variable.

    Returns:
        tuple: Training and testing sets for features and target.
    """

    logger.info("splitting data into train and test sets")
    return train_test_split(
        features,
        target,
        test_size=0.2,  # noqa: WPS432
    )


def _train_model(X_train: pd.DataFrame, y_train: pd.Series):
    """
    Train the RandomForestRegressor model with hyperparameter tuning.

    Args:
        X_train (pd.DataFrame): The training feature set.
        y_train (pd.Series): The training target variable.

    Returns:
        RandomForestRegressor: The trained model with the best hyperparameters
        after GridSearchCV.
    """
    logger.info("training a model with hyperparameters")

    grid_space = {
        "n_estimators": [100, 200, 300],
        "max_depth": [3, 6, 9, 12],
    }

    logger.debug(f"grid_space = {grid_space}")
    grid = GridSearchCV(
        RandomForestRegressor(),
        param_grid=grid_space,
        cv=5,
        scoring="r2",
    )
    model_grid = grid.fit(
        X_train,
        y_train,
    )
    return model_grid.best_estimator_


def _evaluate_model(
    model: RandomForestRegressor,
    X_test: pd.DataFrame,
    y_test: pd.Series,
):
    """
    Evaluate the trained model's performance.

    Args:
        model (RandomForestRegressor): The trained model to be evaluated.
        X_test (pd.DataFrame): The testing feature set.
        y_test (pd.Series): The testing target variable.

    Returns:
        float: The R^2 score of the model on the test set.
    """
    model_score = model.score(
        X_test,
        y_test,
    )
    logger.info(f"evaluating model performance. SCORE={model_score}")
    return model_score


def _save_model(model):
    """
    Save the trained model to a specified directory.

    Args:
        model (RandomForestRegressor): The trained model to be saved.

    Returns:
        None
    """
    model_path = f"{model_settings.model_path}/{model_settings.model_name}"
    logger.info(f"saving a model to a directory: {model_path}")
    with open(model_path, "wb") as model_file:
        pk.dump(model, model_file)
