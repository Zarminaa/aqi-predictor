from contextlib import asynccontextmanager
import logging

import pandas as pd
import shap

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from app.dashboard.model_loader import load_xgboost_model
from app.dashboard.predictor import (
    build_latest_features,
    predict_aqi,
    get_recent_merged_rows,
)

# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FEATURE_COLUMNS_PATH = (
    "models/aqi_xgboost_3day_/feature_columns.json"
)

# --------------------------------------------------
# Response Models
# --------------------------------------------------

class CurrentConditions(BaseModel):
    aqi: float

    pm2_5: float
    pm10: float
    ozone: float
    nitrogen_dioxide: float
    sulphur_dioxide: float
    carbon_monoxide: float

    temperature: float
    humidity: float
    wind_speed: float
    pressure: float
    dew_point: float
    cloud_cover: float


class Prediction(BaseModel):
    Day_1: float
    Day_2: float
    Day_3: float


class PredictionResponse(BaseModel):
    prediction: Prediction
    current: CurrentConditions
    last_updated: str | None


class HistoryResponse(BaseModel):
    datetime: list[str]
    aqi: list[float]


# --------------------------------------------------
# Lifespan
# --------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Loading XGBoost Model...")
    app.state.model = load_xgboost_model()

    logger.info("Building SHAP Explainers...")

    app.state.explainers = [
        shap.TreeExplainer(estimator)
        for estimator in app.state.model.estimators_
    ]

    logger.info("API Ready")

    yield

    logger.info("Shutting down API...")


# --------------------------------------------------
# FastAPI
# --------------------------------------------------

app = FastAPI(
    title="AQI Prediction API",
    description="Predict Lahore AQI for the next 3 days",
    version="1.0.0",
    lifespan=lifespan,
)


# --------------------------------------------------
# Root
# --------------------------------------------------

@app.get("/", tags=["Health"])
def root():

    return {
        "message": "AQI Prediction API is running"
    }


# --------------------------------------------------
# Prediction
# --------------------------------------------------

@app.get(
    "/predict",
    response_model=PredictionResponse,
    tags=["Prediction"],
)
def predict(request: Request):

    try:

        model = request.app.state.model

        X, latest = build_latest_features(
            FEATURE_COLUMNS_PATH,
        )

        prediction = predict_aqi(
            model,
            X,
        )

        return {
            "prediction": {
                "Day_1": prediction["Day 1"],
                "Day_2": prediction["Day 2"],
                "Day_3": prediction["Day 3"],
            },
            "current": {
                "aqi": float(latest["us_aqi"].iloc[0]),

                "pm2_5": float(latest["pm2_5"].iloc[0]),
                "pm10": float(latest["pm10"].iloc[0]),
                "ozone": float(latest["ozone"].iloc[0]),
                "nitrogen_dioxide": float(latest["nitrogen_dioxide"].iloc[0]),
                "sulphur_dioxide": float(latest["sulphur_dioxide"].iloc[0]),
                "carbon_monoxide": float(latest["carbon_monoxide"].iloc[0]),

                "temperature": float(latest["temperature_2m"].iloc[0]),
                "humidity": float(latest["relative_humidity_2m"].iloc[0]),
                "wind_speed": float(latest["wind_speed_10m"].iloc[0]),
                "pressure": float(latest["surface_pressure"].iloc[0]),

                "dew_point": float(latest["dew_point_2m"].iloc[0]),
                "cloud_cover": float(latest["cloud_cover"].iloc[0]),
            },
            "last_updated": str(latest["datetime"].iloc[0]),
        }

    except Exception as e:

        logger.exception("Prediction failed")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
# --------------------------------------------------
# Historical AQI
# --------------------------------------------------

@app.get(
    "/history",
    response_model=HistoryResponse,
    tags=["History"],
)
def history():

    try:

        df = get_recent_merged_rows(limit=5000)

        return {
            "datetime": (
                pd.to_datetime(df["datetime"])
                .astype(str)
                .tolist()
            ),
            "aqi": df["us_aqi"].astype(float).tolist(),
        }

    except Exception as e:

        logger.exception("History endpoint failed")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# --------------------------------------------------
# SHAP Feature Importance
# --------------------------------------------------

@app.get(
    "/shap",
    tags=["Explainability"],
)
def shap_values(request: Request):

    try:

        explainers = request.app.state.explainers

        X, latest = build_latest_features(
            FEATURE_COLUMNS_PATH,
        )

        total_importance = None

        for explainer in explainers:

            shap_values = explainer.shap_values(X)

            importance = abs(shap_values[0])

            if total_importance is None:
                total_importance = importance
            else:
                total_importance += importance

        total_importance /= len(explainers)

        importance_df = (
            pd.DataFrame(
                {
                    "feature": X.columns,
                    "importance": total_importance,
                }
            )
            .sort_values(
                "importance",
                ascending=False,
            )
        )

        return importance_df.to_dict("records")

    except Exception as e:

        logger.exception("SHAP endpoint failed")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )