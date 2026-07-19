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
    """

    if target not in TARGET_COLUMNS:
        raise ValueError(f"Invalid target: {target}")

    n = len(df)

    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    train_df = df.iloc[:train_end]
    val_df = df.iloc[train_end:val_end]
    test_df = df.iloc[val_end:]

    feature_columns = [
        column
        for column in df.columns
        if column not in [
            "datetime",
            *TARGET_COLUMNS,
        ]
    ]

    X_train = train_df[feature_columns]
    y_train = train_df[target]

    X_val = val_df[feature_columns]
    y_val = val_df[target]

    X_test = test_df[feature_columns]
    y_test = test_df[target]

    return (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
    )