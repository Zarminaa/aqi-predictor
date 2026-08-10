# Dashboard

## Overview

The dashboard serves as the primary user interface for the AQI Prediction System, providing real-time monitoring of environmental conditions and machine learning-based forecasts for the next three days in **Lahore Cantonment**. It combines live air quality measurements, weather observations, predictive analytics, historical trends, model explainability, and evaluation metrics into a single interactive application.

The dashboard is developed using **Streamlit**, while all prediction and data processing tasks are handled by a **FastAPI** backend. This architecture separates the user interface from the inference logic, making the application modular, scalable, and easier to maintain. The backend retrieves the latest environmental observations, performs feature engineering, generates predictions using the trained XGBoost model, computes explainability scores, and serves all required information through REST API endpoints. :contentReference[oaicite:0]{index=0}

---

# Dashboard Architecture

```text
                    Supabase Database
                           │
                           ▼
                 FastAPI Prediction API
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
      ▼                    ▼                    ▼
Feature Engineering   XGBoost Prediction   SHAP Explainability
      │                    │                    │
      └────────────────────┼────────────────────┘
                           │
                           ▼
                 Streamlit Dashboard
                           │
                           ▼
            Interactive Visualizations
```

---

# Why XGBoost?

Multiple machine learning models were evaluated during the development of the AQI forecasting system to determine the most suitable algorithm for multi-day air quality prediction. The evaluated models included:

- Ridge Regression
- Random Forest Regressor
- XGBoost Regressor

Among these models, **XGBoost** consistently demonstrated the best predictive performance across both validation and testing datasets. The final deployment therefore uses an **XGBoost Multi-Output Regression model** capable of predicting AQI values for the next three days simultaneously.

XGBoost was selected because it:

- Achieved the highest R² scores during evaluation.
- Produced lower Mean Absolute Error (MAE).
- Produced lower Root Mean Squared Error (RMSE).
- Generalized better on unseen data.
- Captured complex nonlinear relationships between meteorological variables and atmospheric pollutants.
- Maintained stable performance across multiple forecasting horizons.

These characteristics made XGBoost the most reliable model for deployment in the production inference pipeline.

---

# Backend API

The Streamlit dashboard communicates with a FastAPI backend through several REST endpoints. Each endpoint is responsible for serving a specific component of the dashboard.

| Endpoint | Description |
|----------|-------------|
| `/predict` | Generates AQI predictions for the next three days and returns the latest environmental observations. |
| `/history` | Retrieves historical AQI observations from the merged dataset stored in Supabase. |
| `/metrics` | Returns validation and testing metrics of the deployed XGBoost model. |
| `/shap` | Computes and returns SHAP feature importance values for model explainability. |

When the FastAPI server starts, it performs the following initialization steps:

1. Downloads the latest trained model from the Hopsworks Model Registry.
2. Loads the trained XGBoost model.
3. Loads the stored evaluation metrics.
4. Loads the feature column definitions.
5. Initializes SHAP explainers.

Since these components are loaded only once during application startup, prediction requests remain efficient with minimal latency.

---

# Model Loading

Instead of storing trained models locally, the application retrieves the latest production model directly from the **Hopsworks Model Registry**.

During initialization, the backend:

- Authenticates with Hopsworks.
- Downloads the latest registered model version.
- Loads the serialized model using Joblib.
- Loads evaluation metrics from `metrics.json`.
- Loads the feature column configuration used during training.

This approach ensures that the dashboard always uses the latest deployed model without requiring manual updates to the application.

---

# Feature Engineering During Inference

Predictions are not generated directly from raw environmental observations. Before inference, the backend reconstructs the complete feature vector using the same feature engineering pipeline employed during model training.

The inference pipeline performs the following operations:

1. Retrieves the most recent merged environmental observations from Supabase.
2. Applies the complete feature engineering pipeline.
3. Generates temporal features.
4. Generates cyclical time features.
5. Generates lag features.
6. Generates rolling statistics.
7. Generates trend-based features.
8. Generates interaction features.
9. Selects only the feature columns used during model training.
10. Passes the engineered feature vector to the XGBoost model.

Using an identical preprocessing pipeline during both training and inference ensures feature consistency and prevents training-serving skew.

---

# Current Air Quality Monitoring

The dashboard displays the latest environmental observations retrieved from the merged dataset.

The current air quality panel includes:

- Current US AQI
- PM2.5
- PM10
- Ozone (O₃)
- Nitrogen Dioxide (NO₂)
- Sulphur Dioxide (SO₂)
- Carbon Monoxide (CO)

Alongside pollutant concentrations, the dashboard also displays the latest weather measurements, including:

- Temperature
- Relative Humidity
- Wind Speed
- Surface Pressure
- Dew Point
- Cloud Cover

The current AQI is visualized using an interactive gauge chart and classified according to standard AQI categories, allowing users to quickly interpret the current air quality conditions. :contentReference[oaicite:1]{index=1}

---

# Three-Day AQI Forecast

The primary objective of the dashboard is to provide short-term AQI forecasts.

The deployed XGBoost model predicts:

- Day 1 AQI
- Day 2 AQI
- Day 3 AQI

Each prediction is displayed using an individual forecast card showing:

- Predicted AQI value
- Air quality category
- Color-coded severity indicator

A line chart visualizes the predicted AQI trajectory over the next three days, enabling users to easily observe expected changes in air quality over time. :contentReference[oaicite:2]{index=2}

---

# Health Advisory

The dashboard automatically generates health advisory messages based on the predicted AQI for the following day.

Depending on the predicted pollution level, the dashboard displays alerts such as:

- Favorable Air Quality
- Elevated Pollution Advisory
- Hazardous Atmosphere Forecasted

These notifications provide users with quick guidance regarding outdoor activities based on the forecasted air quality. :contentReference[oaicite:3]{index=3}

---

# Historical AQI Trends

Historical observations are retrieved from the Supabase database and visualized using an interactive Plotly area chart.

The historical visualization enables users to:

- Explore recent AQI patterns.
- Observe pollution fluctuations over time.
- Compare current air quality with historical measurements.
- Identify short-term pollution episodes.

Providing historical context helps users better understand current environmental conditions alongside future predictions. :contentReference[oaicite:4]{index=4}

---

# Model Explainability

Machine learning models often function as black boxes, making it difficult to understand why a particular prediction was generated.

To improve transparency, the dashboard integrates **SHAP (SHapley Additive exPlanations)**.

During API initialization, SHAP TreeExplainers are created for the trained XGBoost estimators. When explainability is requested, SHAP values are computed for the latest feature vector and aggregated into overall feature importance scores.

The dashboard presents these importance scores as an interactive horizontal bar chart, allowing users to identify the variables that contributed most significantly to the current prediction.

Providing explainability improves trust in the model by allowing users to understand the factors influencing AQI predictions rather than viewing them as unexplained outputs. :contentReference[oaicite:5]{index=5}

---

# Model Performance

To provide transparency regarding predictive accuracy, the dashboard displays evaluation metrics generated during model training.

Performance is reported separately for:

- Validation Dataset
- Test Dataset

For each forecasting horizon (Day 1, Day 2, and Day 3), the dashboard presents:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- Coefficient of Determination (R²)

These metrics allow users to evaluate the expected accuracy of the deployed model across different prediction horizons.

Additionally, the dashboard includes a performance visualization illustrating how prediction error changes as the forecasting horizon increases. Since forecasting uncertainty generally increases over time, this visualization provides valuable insight into the behavior of the deployed model. :contentReference[oaicite:6]{index=6}

---

# Interactive Visualizations

The dashboard makes extensive use of Plotly visualizations to improve user interaction and data interpretation.

The available visualizations include:

- AQI Gauge Chart
- Three-Day Forecast Cards
- AQI Forecast Line Chart
- Historical AQI Area Chart
- SHAP Feature Importance Bar Chart
- Model Performance Comparison Charts

These visualizations enable users to quickly interpret current conditions, forecast trends, and model behavior through an intuitive graphical interface.

---

# User Interface Design

The dashboard adopts a modern monitoring-style interface optimized for readability and user experience.

Key design features include:

- Dark-themed interface
- Responsive layout
- Live system status indicator
- Interactive Plotly visualizations
- Color-coded AQI categories
- Glassmorphism-inspired information cards
- Responsive pollutant and weather panels
- Automatic data caching to improve responsiveness

This design provides a clean and intuitive interface suitable for continuous environmental monitoring. :contentReference[oaicite:7]{index=7}

---

# Dashboard Workflow

```text
          Supabase Database
                  │
                  ▼
      Retrieve Latest Environmental Data
                  │
                  ▼
        Feature Engineering Pipeline
                  │
                  ▼
     XGBoost Multi-Output Regression
                  │
      ┌───────────┼────────────┐
      │           │            │
      ▼           ▼            ▼
  Predictions   SHAP       Model Metrics
      │           │            │
      └───────────┼────────────┘
                  │
                  ▼
          FastAPI REST API
                  │
                  ▼
        Streamlit Dashboard
                  │
                  ▼
      Interactive AQI Monitoring
```

---

# Summary

The dashboard provides an end-to-end interface for monitoring and forecasting air quality in Lahore Cantonment. By integrating real-time environmental observations, engineered features, an XGBoost-based forecasting model, SHAP explainability, historical trend analysis, and comprehensive evaluation metrics, it offers users a transparent and interactive platform for understanding both current and future air quality conditions. The separation of the Streamlit frontend from the FastAPI inference backend further ensures modularity, scalability, and ease of deployment within the overall MLOps pipeline.
