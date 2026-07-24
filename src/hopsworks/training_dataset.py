# src/hopsworks/training_dataset.py

import pandas as pd

from src.hopsworks.feature_view import get_feature_view



def load_training_data(
    description="AQI 3-Day Forecasting Dataset",
):
    """
    Load training data directly from Feature View.

    This creates an in-memory dataset.
    It does NOT create a versioned training dataset.

    Returns
    -------
    pandas.DataFrame
        Features and labels combined.
    """


    feature_view = get_feature_view()


    feature_df, label_df = feature_view.training_data(
        description=description,
    )


    if label_df is not None:

        df = pd.concat(
            [
                feature_df,
                label_df,
            ],
            axis=1,
        )

    else:

        df = feature_df


    print("=" * 50)
    print("Training Data Loaded")
    print("=" * 50)
    print(
        f"Shape : {df.shape}"
    )


    return df




def create_training_dataset(
    description="AQI 3-Day Forecasting Dataset",
    data_format="parquet",
    wait_for_job=True,
):
    """
    Create a materialized versioned training dataset.

    Parameters
    ----------
    description : str
        Dataset description.

    data_format : str
        Storage format.
        parquet recommended for ML datasets.

    wait_for_job : bool
        Wait until materialization finishes.

    Returns
    -------
    int
        Training dataset version.
    """


    feature_view = get_feature_view()


    version, job = feature_view.create_training_data(
        description=description,
        data_format=data_format,
        write_options={
            "wait_for_job": wait_for_job,
        },
    )


    print("=" * 50)
    print("Training Dataset Created")
    print("=" * 50)
    print(
        f"Version : {version}"
    )


    # Hopsworks 5.x may return bytes here,
    # not a Job object.
    if job is not None:

        print(
            f"Materialization job returned: {job}"
        )


    return version




def get_training_dataset(
    version,
):
    """
    Load a previously materialized training dataset.

    Parameters
    ----------
    version : int
        Training dataset version.

    Returns
    -------
    pandas.DataFrame
        Features and labels combined.
    """


    feature_view = get_feature_view()


    feature_df, label_df = feature_view.get_training_data(
        training_dataset_version=version,
    )


    if label_df is not None:

        df = pd.concat(
            [
                feature_df,
                label_df,
            ],
            axis=1,
        )

    else:

        df = feature_df


    print("=" * 50)
    print("Training Dataset Loaded")
    print("=" * 50)
    print(
        f"Version : {version}"
    )
    print(
        f"Shape   : {df.shape}"
    )


    return df




def get_training_dataset_splits(
    version,
):
    """
    Retrieve Hopsworks generated train/validation/test splits.

    NOTE:
    For your AQI time-series project we currently use our own
    chronological split_data.py, so this function is kept for
    future experimentation.

    Returns
    -------
    tuple
        Train/validation/test splits.
    """


    feature_view = get_feature_view()


    return feature_view.get_train_validation_test_split(
        training_dataset_version=version,
    )