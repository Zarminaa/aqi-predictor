# AQI Predictor Feature Dictionary

## Overview

This document describes all features used in the AQI forecasting pipeline.

Target:
Predict AQI for the next 3 days:
- target_day1
- target_day2
- target_day3

Forecast frequency:
Hourly

Location:
Lahore, Pakistan

Data sources:
- Open-Meteo Air Quality API
- Open-Meteo Weather API


---

# Feature Groups


## 1. Timestamp Feature

| Feature | Type | Description |
|---|---|---|
| datetime | datetime | Timestamp of the observation (hourly frequency) |

Source:
API timestamp

Purpose:
Used for temporal ordering and feature generation.


---

# 2. Current Air Quality Features

| Feature | Type | Description |
|---|---|---|
| us_aqi | float | Current US Air Quality Index |
| pm2_5 | float | PM2.5 concentration |
| pm10 | float | PM10 concentration |
| carbon_monoxide | float | Carbon monoxide concentration |
| nitrogen_dioxide | float | Nitrogen dioxide concentration |
| sulphur_dioxide | float | Sulphur dioxide concentration |
| ozone | float | Ozone concentration |

Source:
Air Quality API

Purpose:
Main pollution indicators used for AQI prediction.



---

# 3. Weather Features

| Feature | Type | Description |
|---|---|---|
| temperature_2m | float | Air temperature at 2 meters |
| relative_humidity_2m | float | Relative humidity percentage |
| dew_point_2m | float | Dew point temperature |
| surface_pressure | float | Atmospheric pressure |
| wind_speed_10m | float | Wind speed at 10 meters |
| precipitation | float | Precipitation amount |
| cloud_cover | float | Cloud coverage percentage |

Source:
Weather API

Purpose:
Capture meteorological effects on pollution dispersion.



---

# 4. Calendar Features

| Feature | Type | Description |
|---|---|---|
| day | integer | Day of month |
| day_of_year | integer | Day number within year |
| is_weekend | boolean | Whether observation occurs on weekend |

Purpose:
Capture human activity patterns.


---

# 5. Cyclic Time Encoding Features

## Hour Encoding

| Feature | Description |
|---|---|
| hour_sin | Sine transformation of hour |
| hour_cos | Cosine transformation of hour |

Purpose:
Capture daily pollution cycles.


## Month Encoding

| Feature | Description |
|---|---|
| month_sin | Sine transformation of month |
| month_cos | Cosine transformation of month |

Purpose:
Capture seasonal patterns.


## Day Of Week Encoding

| Feature | Description |
|---|---|
| dow_sin | Sine transformation of weekday |
| dow_cos | Cosine transformation of weekday |

Purpose:
Capture weekly patterns.


## Wind Direction Encoding

| Feature | Description |
|---|---|
| wind_dir_sin | Sine transformation of wind direction |
| wind_dir_cos | Cosine transformation of wind direction |

Purpose:
Avoid discontinuity in wind direction values.


---

# 6. Lag Features

Lag features represent previous observations.

Formula:

feature_lag_n = value n hours before current timestamp


## AQI Lag Features

| Feature | Description |
|---|---|
| us_aqi_lag_1 | AQI one hour ago |
| us_aqi_lag_3 | AQI three hours ago |
| us_aqi_lag_6 | AQI six hours ago |
| us_aqi_lag_12 | AQI twelve hours ago |
| us_aqi_lag_24 | AQI one day ago |
| us_aqi_lag_48 | AQI two days ago |


## Pollutant Lag Features

Includes:

- pm2_5
- pm10
- carbon_monoxide
- nitrogen_dioxide
- sulphur_dioxide
- ozone


Purpose:
Capture pollution persistence and temporal dependencies.



---

# 7. Rolling Statistics

Rolling statistics summarize recent pollution behavior.


## AQI Rolling Features

| Feature | Description |
|---|---|
| aqi_mean_6 | Average AQI over previous 6 hours |
| aqi_std_6 | AQI variation over previous 6 hours |
| aqi_min_6 | Minimum AQI over previous 6 hours |
| aqi_max_6 | Maximum AQI over previous 6 hours |

Same calculation applies for:
- 12 hour window
- 24 hour window


## PM2.5 Rolling Features

| Feature | Description |
|---|---|
| pm25_mean_6 | Average PM2.5 over previous 6 hours |
| pm25_std_6 | PM2.5 variation over previous 6 hours |
| pm25_mean_24 | Average PM2.5 over previous 24 hours |
| pm25_std_24 | PM2.5 variation over previous 24 hours |


Purpose:
Capture pollution trends.


---

# 8. Change Features

Difference between current and previous observations.


Formula:

current_value - previous_value


| Feature | Description |
|---|---|
| aqi_change | AQI increase/decrease from previous hour |
| pm25_change | PM2.5 increase/decrease |
| temperature_change | Temperature change |
| pressure_change | Pressure change |


Purpose:
Capture pollution movement direction.


---

# 9. Interaction Features

Combined features representing relationships between variables.


| Feature | Description |
|---|---|
| temp_humidity | Temperature × humidity interaction |
| wind_pm25 | Wind speed × PM2.5 interaction |
| wind_pm10 | Wind speed × PM10 interaction |


Purpose:
Capture meteorological influence on pollution.


---

# Target Variables

| Target | Description |
|---|---|
| target_day1 | AQI value 24 hours after observation |
| target_day2 | AQI value 48 hours after observation |
| target_day3 | AQI value 72 hours after observation |


Targets are excluded from feature store during inference.


---

# Feature Store Schema

Feature Group:

aqi_features

Primary Key:

datetime

Frequency:

Hourly


Feature Types:

- Numerical: float
- Categorical: boolean/integer
- Timestamp: datetime


---

# Future Features

Planned additions:

- season
- week_of_year
- AQI lag 72 hours
- AQI rolling mean 7 days
- PM2.5 rolling mean 7 days
- holiday indicators