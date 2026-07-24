import pandas as pd
from sklearn.preprocessing import StandardScaler


def scale_features(
    X_train,
    X_val,
    X_test,
):
    """
    Scale feature sets while preserving
    DataFrame structure and column names.
    """

    scaler = StandardScaler()

    train_columns = X_train.columns
    val_columns = X_val.columns
    test_columns = X_test.columns

    train_index = X_train.index
    val_index = X_val.index
    test_index = X_test.index

    X_train = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=train_columns,
        index=train_index,
    )

    X_val = pd.DataFrame(
        scaler.transform(X_val),
        columns=val_columns,
        index=val_index,
    )

    X_test = pd.DataFrame(
        scaler.transform(X_test),
        columns=test_columns,
        index=test_index,
    )

    return (
        X_train,
        X_val,
        X_test,
        scaler,
    )