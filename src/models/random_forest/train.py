from sklearn.ensemble import RandomForestRegressor


def train_random_forest(
    X_train,
    y_train,
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
):
    """
    Train a Random Forest Regressor.
    """

    model = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=n_jobs,
    )

    model.fit(X_train, y_train)

    return model


train_random_forest.requires_scaling = False