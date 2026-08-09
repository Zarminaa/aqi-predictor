# Feature Engineering

## Overview

Raw weather and air quality observations are often insufficient for training accurate forecasting models because they do not explicitly capture temporal patterns, historical dependencies, seasonal behavior, or relationships between environmental variables. Feature engineering transforms these raw observations into informative representations that improve a machine learning model's ability to learn complex patterns within the data.

In this project, the merged hourly weather and pollution dataset is processed through a dedicated feature engineering pipeline that generates multiple categories of features, including temporal features, cyclical encodings, lagged observations, rolling statistics, trend indicators, interaction variables, and multi-day prediction targets.

The resulting engineered dataset serves as the foundation for the complete MLOps pipeline. It is stored both locally and within the Hopsworks Feature Store, enabling reproducible model training, centralized feature management, and consistent feature reuse throughout the project.

---

## Feature Engineering Pipeline

The complete feature engineering workflow is illustrated below.

```text
Merged Dataset (lahore_merged.csv)
                │
                ▼
      Time Feature Extraction
                │
                ▼
     Cyclical Feature Encoding
                │
                ▼
        Lag Feature Generation
                │
                ▼
      Rolling Window Statistics
                │
                ▼
        Trend Feature Creation
                │
                ▼
    Interaction Feature Creation
                │
                ▼
     Multi-Day Target Generation
                │
                ▼
 Remove Temporary Columns & NaNs
                │
                ▼
      Engineered Feature Dataset
          (features.csv)
                │
                ▼
     Hopsworks Feature Group
                │
                ▼
         Hopsworks Feature View
                │
                ▼
     Training Dataset Creation
                │
                ▼
        Model Training Pipeline
```

---

## Input Dataset

The feature engineering pipeline begins with the merged dataset generated during the data processing stage.

**Input File**

```text
data/interim/lahore_merged.csv
```

This dataset combines hourly weather observations and air quality measurements collected from the Open-Meteo Weather API and Open-Meteo Air Quality API into a single chronological dataset.

Each record represents one hourly observation and contains variables such as:

- Air Quality Index (US AQI)
- PM₂.₅ concentration
- PM₁₀ concentration
- Carbon Monoxide (CO)
- Nitrogen Dioxide (NO₂)
- Sulphur Dioxide (SO₂)
- Ozone (O₃)
- Temperature
- Relative Humidity
- Surface Pressure
- Wind Speed
- Wind Direction
- Cloud Cover
- Timestamp (`datetime`)

At this stage, the dataset consists solely of raw measurements and does not yet contain engineered features suitable for machine learning.

---

## Feature Engineering Pipeline

Feature generation is performed through a modular pipeline, where each transformation is implemented as an independent component. This modular design improves maintainability, testing, and future extensibility of the feature engineering process.

The transformations are applied sequentially in the following order:

1. Time Features
2. Cyclical Features
3. Lag Features
4. Rolling Window Features
5. Trend Features
6. Interaction Features
7. Target Features

After all feature transformations are completed, unnecessary intermediate columns are removed, rows containing missing values introduced by lagging and rolling operations are discarded, and the dataset index is reset before saving the final engineered dataset.

This produces a machine learning-ready dataset that is later uploaded into the Hopsworks Feature Store.

## Time Features

Time-based features provide the model with contextual information about when an observation occurred. Air quality exhibits strong temporal patterns influenced by daily human activities, traffic density, industrial operations, and seasonal weather conditions. By explicitly representing temporal information, the model can learn these recurring patterns more effectively.

The following temporal features are extracted directly from the `datetime` column.

| Feature | Description | Purpose |
|---------|-------------|---------|
| `hour` | Hour of the day (0–23) | Captures daily pollution cycles such as rush hours and nighttime conditions. |
| `day` | Day of the month | Represents monthly progression and short-term calendar effects. |
| `day_of_week` | Day of the week (Monday–Sunday) | Enables the model to distinguish weekday and weekend pollution patterns. |
| `month` | Month of the year | Captures seasonal variations in weather and pollution. |
| `day_of_year` | Sequential day within the year | Represents long-term seasonal progression. |
| `is_weekend` | Binary indicator (0 or 1) | Distinguishes weekends from weekdays, where traffic and industrial activity often differ. |

These features provide the model with temporal context while remaining computationally inexpensive to generate.

---

## Cyclical Features

Although variables such as hour, month, day of the week, and wind direction are numerical, they are inherently cyclical. For example, hour **23** and hour **0** are adjacent in time, yet their numerical values suggest they are far apart. Similarly, December and January represent consecutive months despite being encoded as 12 and 1.

To preserve these circular relationships, cyclical variables are transformed using sine and cosine encoding.

For a cyclic variable \(x\) with period \(P\):

\[
\text{sin}(x)=\sin\left(\frac{2\pi x}{P}\right)
\]

\[
\text{cos}(x)=\cos\left(\frac{2\pi x}{P}\right)
\]

This transformation maps cyclical variables onto a unit circle, allowing machine learning models to correctly interpret periodic relationships.

The following cyclical features are generated.

| Feature | Original Variable | Purpose |
|---------|-------------------|---------|
| `hour_sin` | Hour | Encodes the daily cycle. |
| `hour_cos` | Hour | Complements the sine representation of the daily cycle. |
| `month_sin` | Month | Encodes annual seasonal variation. |
| `month_cos` | Month | Complements seasonal encoding. |
| `dow_sin` | Day of Week | Encodes weekly periodicity. |
| `dow_cos` | Day of Week | Complements weekly encoding. |
| `wind_dir_sin` | Wind Direction | Represents circular wind direction. |
| `wind_dir_cos` | Wind Direction | Complements wind direction encoding. |

These features enable the model to capture periodic environmental behavior without introducing artificial discontinuities in the feature space.

---

## Lag Features

Air quality is highly dependent on previous atmospheric conditions. Pollutant concentrations typically evolve gradually over time rather than changing abruptly, making historical observations valuable predictors of future AQI values.

Lag features are created by shifting previous observations forward in time, allowing the model to learn temporal dependencies from earlier measurements.

The project generates lag features for multiple pollution variables using different historical windows.

| Variable | Lag Hours |
|-----------|-----------|
| `us_aqi` | 1, 3, 6, 12, 24, 48 |
| `pm2_5` | 1, 6, 12, 24 |
| `pm10` | 1, 24 |
| `carbon_monoxide` | 1, 24 |
| `nitrogen_dioxide` | 1, 24 |
| `sulphur_dioxide` | 1, 24 |
| `ozone` | 1, 24 |

For example:

- `us_aqi_lag_1` represents the AQI measured one hour earlier.
- `us_aqi_lag_24` represents the AQI observed one day earlier.
- `pm2_5_lag_6` represents the PM₂.₅ concentration recorded six hours earlier.

Including both short-term and long-term lag intervals enables the model to learn immediate pollutant persistence as well as longer temporal trends.

---

## Rolling Window Features

While lag features capture individual historical observations, rolling window features summarize recent behavior over a specified period. These statistical aggregates help the model understand short-term trends, variability, and local fluctuations in air quality.

Rolling statistics are computed using multiple window sizes to represent both immediate and longer-term conditions.

### AQI Rolling Statistics

The following statistics are calculated for rolling windows of **6**, **12**, and **24** hours.

| Feature | Description |
|---------|-------------|
| `aqi_mean_*` | Mean AQI within the rolling window. |
| `aqi_std_*` | Standard deviation of AQI within the window. |
| `aqi_min_*` | Minimum AQI observed in the window. |
| `aqi_max_*` | Maximum AQI observed in the window. |

These statistics capture the recent average pollution level, variability, and local extremes.

### PM₂.₅ Rolling Statistics

PM₂.₅ is one of the primary pollutants affecting AQI. Additional rolling statistics are therefore generated specifically for PM₂.₅ using **6-hour** and **24-hour** windows.

| Feature | Description |
|---------|-------------|
| `pm25_mean_6` | Six-hour rolling average of PM₂.₅ concentration. |
| `pm25_std_6` | Six-hour rolling standard deviation. |
| `pm25_mean_24` | Twenty-four-hour rolling average of PM₂.₅ concentration. |
| `pm25_std_24` | Twenty-four-hour rolling standard deviation. |

These rolling statistics provide the model with a smoothed representation of recent pollution conditions, helping reduce sensitivity to short-term measurement noise while preserving meaningful environmental trends.
## Trend Features

In addition to historical observations and rolling statistics, the feature engineering pipeline captures the direction and magnitude of changes between consecutive observations. These trend-based features help the model recognize whether environmental conditions are improving, deteriorating, or remaining stable over time.

Trend features are generated by computing the first-order difference between consecutive hourly observations.

| Feature | Description | Purpose |
|---------|-------------|---------|
| `aqi_change` | Difference in AQI between consecutive hours | Captures short-term changes in overall air quality. |
| `pm25_change` | Difference in PM₂.₅ concentration | Identifies increasing or decreasing particulate pollution. |
| `temperature_change` | Hourly temperature difference | Represents rapid temperature fluctuations that may influence pollutant dispersion. |
| `pressure_change` | Hourly surface pressure difference | Captures atmospheric pressure changes that can affect air quality conditions. |

Unlike lag features, which provide historical values, trend features describe how quickly environmental conditions are changing, enabling the model to learn dynamic temporal behavior.

---

## Interaction Features

Many environmental variables do not influence air quality independently. Instead, their combined effects often provide stronger predictive signals than individual measurements alone. Interaction features are created to capture these relationships by multiplying related variables together.

The following interaction features are generated.

| Feature | Formula | Purpose |
|---------|----------|---------|
| `temp_humidity` | Temperature × Relative Humidity | Represents combined atmospheric conditions that influence pollutant formation and dispersion. |
| `wind_pm25` | Wind Speed × PM₂.₅ | Models the relationship between wind conditions and fine particulate matter. |
| `wind_pm10` | Wind Speed × PM₁₀ | Represents the combined effect of wind and coarse particulate concentration. |

These interaction terms allow the machine learning model to learn nonlinear relationships between meteorological conditions and air pollutant concentrations that may not be captured by the original variables alone.

---

## Target Features

The objective of this project is to forecast Air Quality Index (AQI) for the next three days using historical weather and pollution observations. To enable supervised learning, future AQI values are converted into prediction targets by shifting the current AQI measurements forward in time.

Three target variables are generated.

| Target | Description |
|---------|-------------|
| `target_day1` | AQI 24 hours ahead |
| `target_day2` | AQI 48 hours ahead |
| `target_day3` | AQI 72 hours ahead |

The targets are created using forward shifts of the `us_aqi` column:

- **target_day1** = AQI at *t + 24 hours*
- **target_day2** = AQI at *t + 48 hours*
- **target_day3** = AQI at *t + 72 hours*

This formulation converts the original time-series forecasting problem into a supervised machine learning task, where the engineered features at time **t** are used to predict future AQI values.

---

## Feature Cleaning

After all engineered features have been generated, several preprocessing steps are performed to prepare the dataset for model training.

### Removal of Temporary Columns

Some intermediate variables are only required during feature generation and do not provide additional information once their engineered representations have been created. These columns are therefore removed from the final dataset.

The following columns are dropped:

| Column | Reason |
|---------|--------|
| `hour` | Replaced by cyclical hour encoding (`hour_sin`, `hour_cos`). |
| `month` | Replaced by cyclical month encoding (`month_sin`, `month_cos`). |
| `day_of_week` | Replaced by cyclical weekday encoding (`dow_sin`, `dow_cos`). |
| `wind_direction_10m` | Replaced by sine and cosine wind direction features. |

### Handling Missing Values

Feature generation introduces missing values at the beginning and end of the dataset:

- Lag features require previous observations.
- Rolling statistics require sufficient historical data.
- Target features require future observations.

Rows containing missing values are removed to ensure that every training sample contains a complete set of input features and target labels.

### Index Reset

Finally, the dataset index is reset after removing incomplete rows to maintain a continuous sequence of observations.

---

## Final Engineered Dataset

After feature engineering and preprocessing, the resulting dataset contains a comprehensive representation of historical air quality conditions, meteorological variables, temporal information, statistical summaries, interaction terms, and future prediction targets.

The engineered dataset includes:

- Original weather and pollution measurements
- Temporal features
- Cyclical encodings
- Historical lag features
- Rolling window statistics
- Trend indicators
- Interaction features
- Three prediction target columns

The processed dataset is saved locally as:

```text
data/processed/features.csv
```

This machine learning-ready dataset serves as the input to the Hopsworks Feature Store, where it becomes the centralized source of features for model training and future inference pipelines.

# Hopsworks Feature Store Integration

## Overview

After feature engineering is completed, the resulting dataset is integrated into the Hopsworks Feature Store. Rather than training models directly from local CSV files, the project uses Hopsworks as a centralized feature repository to ensure feature consistency, reproducibility, and efficient data management across the MLOps pipeline.

The engineered features are first generated locally and stored as `features.csv`. This dataset is then uploaded to a Feature Group, which acts as the authoritative source for all engineered features used throughout the project.

The initial engineered dataset contained **34,632 observations** with **72 columns**, including engineered features and prediction targets, before being uploaded to Hopsworks. :contentReference[oaicite:0]{index=0}

---

## Feature Group

The engineered dataset is stored inside a Hopsworks Feature Group named:

| Property | Value |
|----------|-------|
| Feature Group | `aqi_features_hudi` |
| Version | `1` |
| Primary Key | `datetime` |
| Storage Format | HUDI |

The Feature Group acts as the centralized storage layer for all engineered features generated by the pipeline.

Using a Feature Group provides several advantages:

- Centralized feature storage
- Consistent feature definitions across training and inference
- Version control for feature datasets
- Incremental data insertion
- Time-travel support through HUDI
- Scalable offline feature storage

The Feature Group was created using `datetime` as the primary key and configured with the HUDI storage format to support versioned and incremental feature management. :contentReference[oaicite:1]{index=1}

---

## Initial Feature Backfill

Once feature engineering was completed, the entire engineered dataset was uploaded to the Feature Group as an initial backfill.

The upload process consisted of the following steps:

1. Load the engineered dataset from `features.csv`.
2. Convert the `datetime` column to the appropriate timestamp format.
3. Insert the complete dataset into the Hopsworks Feature Group.
4. Trigger offline materialization.
5. Verify successful completion of the upload.

This one-time initialization populated the Feature Store with the complete historical feature dataset, providing the foundation for future model training and incremental updates.

The upload successfully inserted all **34,632 engineered records** into the Feature Group and completed offline materialization. :contentReference[oaicite:2]{index=2}

---

# Feature View

## Overview

While a Feature Group stores engineered features, machine learning workflows typically require a curated subset of features together with their prediction targets. Hopsworks provides this abstraction through a **Feature View**.

A Feature View defines a reusable logical representation of the features required for model training without duplicating the underlying data.

For this project, the Feature View is configured as follows:

| Property | Value |
|----------|-------|
| Feature View | `aqi_training_view` |
| Version | `1` |
| Source | `aqi_features_hudi` |
| Labels | `target_day1`, `target_day2`, `target_day3` |

The Feature View selects all engineered features from the Feature Group while explicitly designating the three future AQI targets as prediction labels.

Separating features from labels simplifies downstream machine learning workflows and ensures consistent feature retrieval for every training run.

---

## Benefits of Using a Feature View

Using a Feature View provides several important advantages within the MLOps pipeline:

- Centralized feature definitions
- Reusable training datasets
- Consistent feature selection
- Separation of input features and prediction targets
- Simplified model training
- Improved reproducibility
- Version-controlled feature retrieval

Because every model accesses features through the same Feature View, feature consistency is maintained across experiments and future deployments.

---

# Loading Training Data

The project retrieves training data directly from the Feature View instead of reading local CSV files.

During training, the Feature View automatically returns:

- Engineered input features
- Prediction target columns
- A combined training DataFrame ready for preprocessing

The returned features and labels are merged into a single dataset before being passed to the model training pipeline.

This approach ensures that every experiment is trained using the latest approved feature definitions stored in the Feature Store rather than relying on manually managed datasets.

---

# Materialized Training Dataset

In addition to loading data directly from the Feature View, the project also supports creating a **materialized training dataset**.

Materialization creates a versioned snapshot of the Feature View and stores it as a persistent dataset within Hopsworks.

Compared with loading data directly from the Feature View, a materialized training dataset offers several advantages:

- Reproducible experiments
- Dataset versioning
- Faster repeated access
- Stable training data across multiple experiments
- Simplified experiment tracking

Although the current training pipeline primarily loads data directly from the Feature View, support for materialized datasets has been implemented to enable future experimentation and long-term reproducibility.

---
# Incremental Feature Engineering Pipeline

## Overview

While the initial historical dataset is uploaded to the Hopsworks Feature Store as a one-time backfill, the project also implements an incremental feature engineering pipeline to continuously process newly collected weather and air quality data.

Instead of regenerating and uploading the entire feature dataset every time new observations become available, the incremental pipeline processes only newly collected records and inserts only unseen engineered features into the Feature Group.

This approach significantly reduces processing time, avoids duplicate feature generation, and keeps the Feature Store synchronized with the latest available data.

---

## Pipeline State Management

To support incremental processing, the pipeline maintains a processing checkpoint inside Supabase using a dedicated `pipeline_state` table.

For the feature engineering pipeline, this table stores the timestamp of the most recently processed observation.

During each pipeline execution:

1. The last processed timestamp is retrieved.
2. The latest merged dataset is loaded from Supabase.
3. Feature engineering is performed on the complete chronological dataset.
4. Only records newer than the stored checkpoint are selected.
5. Newly engineered features are uploaded to the Feature Store.
6. The checkpoint is updated with the latest processed timestamp.

By maintaining this checkpoint, the pipeline ensures that previously processed observations are never engineered or uploaded more than once.

---

## Feature Engineering for New Data

The incremental pipeline applies exactly the same feature engineering process used during the initial dataset creation.

Each execution generates:

- Time features
- Cyclical features
- Lag features
- Rolling window statistics
- Trend features
- Interaction features
- Prediction targets

Using a single feature engineering pipeline guarantees that historical data and newly generated features follow identical transformation logic, ensuring consistency throughout the Feature Store.

---

## Data Type Validation

Before inserting newly engineered features into Hopsworks, the pipeline validates and standardizes the data types of every feature.

The validation process includes:

- Converting the `datetime` column into the required timestamp format.
- Converting integer-based features to `int64`.
- Converting continuous numerical features to `float64`.
- Handling invalid or missing numeric values before insertion.

Standardizing feature data types ensures compatibility with the predefined Feature Group schema and prevents schema mismatch errors during ingestion.

---

## Incremental Feature Insertion

Once validation is complete, only newly generated feature records are inserted into the existing Hopsworks Feature Group.

Because the Feature Group uses `datetime` as its primary key and stores data using the HUDI storage format, new observations can be appended without recreating the entire dataset.

This incremental ingestion strategy enables the Feature Store to remain continuously updated while preserving all previously stored historical records.

---

## Updating the Processing Checkpoint

After a successful insertion into the Feature Group, the pipeline determines the most recent timestamp among the newly processed records.

This timestamp is then written back to the `pipeline_state` table in Supabase.

Updating the checkpoint marks all processed observations as complete, ensuring that the next pipeline execution begins processing only from the first unseen observation.

---

# Chronological Dataset Splitting

## Overview

After loading the engineered features from the Hopsworks Feature View, the dataset is divided into training, validation, and testing subsets.

Since AQI forecasting is a time-series prediction problem, preserving the chronological order of observations is essential. Randomly shuffling records would introduce future information into the training set, resulting in data leakage and overly optimistic model performance.

To avoid this issue, the project implements a chronological splitting strategy.

---

## Split Ratios

The engineered dataset is divided using the following proportions:

| Dataset | Ratio |
|---------|------:|
| Training | 80% |
| Validation | 10% |
| Testing | 10% |

The data is split sequentially based on time, ensuring that earlier observations are used for training while later observations are reserved for validation and testing.

This approach more accurately reflects real-world forecasting, where future observations are unavailable during model training.

---

## Feature and Target Separation

Before training, the dataset is divided into input features (`X`) and prediction targets (`y`).

The following columns are excluded from the feature matrix:

- `datetime`
- `target_day1`
- `target_day2`
- `target_day3`

The remaining columns constitute the input feature set used by the machine learning models.

Depending on the forecasting objective, one of the target columns is selected as the prediction label.

Although the project currently trains separate models for each prediction horizon, the feature engineering pipeline supports all three target variables simultaneously.

---

## Why Not Use Hopsworks Train-Test Splits?

Hopsworks provides functionality for automatically generating train, validation, and test splits from a Feature View.

However, these generic splitting methods are primarily designed for conventional machine learning problems and do not explicitly preserve temporal ordering.

To prevent information leakage and maintain the integrity of time-series forecasting, this project instead uses a custom chronological splitting strategy implemented within the training pipeline.

Support for Hopsworks-generated dataset splits has nevertheless been retained within the codebase for future experimentation and comparison.

---

# Feature Engineering Workflow Summary

The complete feature engineering workflow implemented in this project is summarized below.

```text
Merged Dataset
       │
       ▼
Time Features
       │
       ▼
Cyclical Features
       │
       ▼
Lag Features
       │
       ▼
Rolling Statistics
       │
       ▼
Trend Features
       │
       ▼
Interaction Features
       │
       ▼
Target Generation
       │
       ▼
Feature Cleaning
       │
       ▼
features.csv
       │
       ▼
Hopsworks Feature Group
       │
       ▼
Feature View
       │
       ▼
Training Dataset
       │
       ▼
Chronological Train / Validation / Test Split
       │
       ▼
Machine Learning Models
```

---

# Conclusion

The feature engineering stage transforms raw weather and air quality observations into a comprehensive machine learning dataset suitable for multi-day AQI forecasting. Through the generation of temporal, cyclical, lag, rolling, trend, interaction, and target features, the pipeline captures both the historical behavior and environmental dynamics that influence future air quality.

By integrating the engineered dataset with the Hopsworks Feature Store, the project establishes a centralized and reproducible feature management system that supports versioning, incremental updates, reusable Feature Views, and consistent feature retrieval across training workflows. Combined with a custom chronological data splitting strategy, this feature engineering pipeline provides a robust foundation for accurate and reproducible AQI prediction within the end-to-end MLOps architecture.
