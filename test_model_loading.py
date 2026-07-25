from src.hopsworks.feature_view import get_feature_view
from app.dashboard.model_loader import load_xgboost_model
from app.dashboard.predictor import (
    get_latest_features,
    predict_aqi
)


fv = get_feature_view()

model = load_xgboost_model()


X = get_latest_features(
    fv,
    "models/aqi_xgboost_3day_/feature_columns.json"
)


print(X)


result = predict_aqi(
    model,
    X
)


print(result)