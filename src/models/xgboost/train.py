from xgboost import XGBRegressor


def train_xgboost(
    X_train,
    y_train,
):
    """
    Train an XGBoost regressor.
    """

    model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        objective="reg:squarederror",
        n_jobs=-1,
    )

    model.fit(
        X_train,
        y_train,
    )

    return model

train_xgboost.requires_scaling = False