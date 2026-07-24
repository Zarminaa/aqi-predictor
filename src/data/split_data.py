TARGET_COLUMNS = [
    "target_day1",
    "target_day2",
    "target_day3",
]


def split_data(
    df,
    target="target_day1",
    train_ratio=0.8,
    val_ratio=0.1,
):
    """
    Split a time-series dataset into
    train, validation and test sets.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset.

    target : str or list[str]
        Target column(s) to predict.

    train_ratio : float
        Fraction of data used for training.

    val_ratio : float
        Fraction of data used for validation.
    """

    # ----------------------------------------------------
    # Validate split ratios
    # ----------------------------------------------------
    if not (0 < train_ratio < 1):
        raise ValueError(
            "train_ratio must be between 0 and 1."
        )

    if not (0 <= val_ratio < 1):
        raise ValueError(
            "val_ratio must be between 0 and 1."
        )

    if train_ratio + val_ratio >= 1:
        raise ValueError(
            "train_ratio + val_ratio must be less than 1."
        )

    # ----------------------------------------------------
    # Validate target(s)
    # ----------------------------------------------------
    if isinstance(target, str):

        if target not in TARGET_COLUMNS:
            raise ValueError(
                f"Invalid target: {target}"
            )

    elif isinstance(target, list):

        invalid_targets = [
            t
            for t in target
            if t not in TARGET_COLUMNS
        ]

        if invalid_targets:
            raise ValueError(
                f"Invalid targets: {invalid_targets}"
            )

    else:
        raise TypeError(
            "target must be a string or a list of strings."
        )

    # ----------------------------------------------------
    # Ensure chronological order
    # ----------------------------------------------------
    if "datetime" in df.columns:

        df = (
            df.sort_values("datetime")
            .reset_index(drop=True)
        )

    # ----------------------------------------------------
    # Split dataset
    # ----------------------------------------------------
    n = len(df)

    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    train_df = df.iloc[:train_end]
    val_df = df.iloc[train_end:val_end]
    test_df = df.iloc[val_end:]

    # ----------------------------------------------------
    # Validate split sizes
    # ----------------------------------------------------
    if (
        train_df.empty
        or val_df.empty
        or test_df.empty
    ):
        raise ValueError(
            "One or more dataset splits are empty. "
            "Adjust the split ratios."
        )

    # ----------------------------------------------------
    # Feature columns
    # ----------------------------------------------------
    excluded_columns = set(TARGET_COLUMNS)

    if "datetime" in df.columns:
        excluded_columns.add("datetime")

    feature_columns = [
        column
        for column in df.columns
        if column not in excluded_columns
    ]

    # ----------------------------------------------------
    # Features
    # ----------------------------------------------------
    X_train = train_df[feature_columns]
    X_val = val_df[feature_columns]
    X_test = test_df[feature_columns]

    # ----------------------------------------------------
    # Targets
    # ----------------------------------------------------
    y_train = train_df[target]
    y_val = val_df[target]
    y_test = test_df[target]

    return (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
    )