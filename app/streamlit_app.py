import streamlit as st
import pandas as pd
import datetime

from src.hopsworks.feature_view import get_feature_view
from app.dashboard.model_loader import load_xgboost_model
from app.dashboard.predictor import (
    get_latest_features,
    predict_aqi
)


def get_aqi_category(aqi):

    if aqi <= 50:
        return "Good 🟢"

    elif aqi <= 100:
        return "Moderate 🟡"

    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups 🟠"

    elif aqi <= 200:
        return "Unhealthy 🔴"

    elif aqi <= 300:
        return "Very Unhealthy 🟣"

    else:
        return "Hazardous ⚫"



st.set_page_config(
    page_title="Lahore AQI Predictor",
    layout="wide"
)


st.title("🌫️ Lahore AQI Predictor")

st.caption(
    f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)



@st.cache_resource
def load_resources():

    fv = get_feature_view()
    model = load_xgboost_model()

    return fv, model



feature_view, model = load_resources()



# -----------------------------
# Prediction
# -----------------------------

X = get_latest_features(
    feature_view,
    "models/aqi_xgboost_3day_/feature_columns.json"
)


prediction = predict_aqi(
    model,
    X
)



# -----------------------------
# 3 Day Forecast Cards
# -----------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Tomorrow AQI",
        prediction["Day 1"],
        get_aqi_category(prediction["Day 1"])
    )


with col2:

    st.metric(
        "Day 2 AQI",
        prediction["Day 2"],
        get_aqi_category(prediction["Day 2"])
    )


with col3:

    st.metric(
        "Day 3 AQI",
        prediction["Day 3"],
        get_aqi_category(prediction["Day 3"])
    )



# -----------------------------
# Current Air Quality
# -----------------------------

st.divider()

st.subheader("Current Air Quality")


current_aqi = X["us_aqi"].iloc[0]


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Current AQI",
        round(float(current_aqi), 2),
        get_aqi_category(current_aqi)
    )


with col2:

    st.metric(
        "PM2.5",
        round(float(X["pm2_5"].iloc[0]), 2)
    )


with col3:

    st.metric(
        "PM10",
        round(float(X["pm10"].iloc[0]), 2)
    )


with col4:

    st.metric(
        "Temperature",
        f"{float(X['temperature_2m'].iloc[0]):.1f} °C"
    )



# -----------------------------
# Forecast Chart
# -----------------------------

st.divider()

st.subheader("3-Day AQI Forecast")


forecast_df = pd.DataFrame({

    "Day": [
        "Tomorrow",
        "Day 2",
        "Day 3"
    ],

    "AQI": [
        prediction["Day 1"],
        prediction["Day 2"],
        prediction["Day 3"]
    ]

})


st.line_chart(
    forecast_df.set_index("Day")
)



# -----------------------------
# Health Alert
# -----------------------------

st.divider()

st.subheader("Health Alert")


tomorrow_aqi = prediction["Day 1"]


if tomorrow_aqi > 300:

    st.error(
        "⚫ Hazardous AQI expected tomorrow. "
        "Avoid outdoor activities."
    )


elif tomorrow_aqi > 200:

    st.error(
        "🟣 Very unhealthy air quality expected tomorrow. "
        "Sensitive groups should take precautions."
    )


elif tomorrow_aqi > 150:

    st.warning(
        "🔴 Unhealthy air quality expected tomorrow."
    )


else:

    st.success(
        "🟢 Air quality is expected to remain acceptable."
    )



# -----------------------------
# Weather Conditions
# -----------------------------

st.divider()

st.subheader("Weather Conditions")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Humidity",
        f"{float(X['relative_humidity_2m'].iloc[0]):.1f}%"
    )


with col2:

    st.metric(
        "Wind Speed",
        f"{float(X['wind_speed_10m'].iloc[0]):.1f} km/h"
    )


with col3:

    st.metric(
        "Pressure",
        f"{float(X['surface_pressure'].iloc[0]):.1f} hPa"
    )



# -----------------------------
# Historical AQI Trend
# -----------------------------

st.divider()

st.subheader("Historical AQI Trend")


history_df = feature_view.get_batch_data()


if "datetime" in history_df.columns:

    history_df = history_df.sort_values(
        "datetime"
    )

    st.line_chart(
        history_df.set_index("datetime")["us_aqi"]
    )

else:

    st.warning(
        "Timestamp column not available for historical chart."
    )