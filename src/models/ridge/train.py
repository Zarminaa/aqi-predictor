from sklearn.linear_model import Ridge


def train_ridge(
    X_train,
    y_train,
    alpha=1.0,
    random_state=42,
):
    """
    Train a Ridge Regression model.
    """

    model = Ridge(
        alpha=alpha,
        random_state=random_state,
    )

    model.fit(
        X_train,
        y_train,
    )

    return model


train_ridge.requires_scaling = True