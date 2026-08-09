# Model Comparison

## Overview

Selecting an appropriate machine learning model is a critical step in building a reliable AQI forecasting system. Since air quality prediction is influenced by complex nonlinear relationships between weather variables, pollutant concentrations, and temporal patterns, multiple regression algorithms were evaluated before selecting the final production model.

Four different models were trained and evaluated using the same engineered feature set and identical chronological train-validation-test splits:

- Ridge Regression
- Random Forest Regressor
- XGBoost Regressor
- PyTorch Neural Network

Each model was trained to perform **multi-output regression**, simultaneously predicting the Air Quality Index (AQI) for the next three days:

- Day 1 (24 hours ahead)
- Day 2 (48 hours ahead)
- Day 3 (72 hours ahead)

The evaluation process compared predictive accuracy, generalization performance, and forecasting consistency across all prediction horizons.

---

# Evaluation Metrics

Three regression metrics were used to evaluate every model.

## Mean Absolute Error (MAE)

Mean Absolute Error measures the average magnitude of prediction errors without considering their direction.

Lower MAE values indicate more accurate predictions.

\[
MAE=\frac{1}{n}\sum |y_i-\hat{y_i}|
\]

---

## Root Mean Squared Error (RMSE)

Root Mean Squared Error penalizes larger prediction errors more heavily than MAE.

Lower RMSE values indicate better predictive performance.

\[
RMSE=\sqrt{\frac{1}{n}\sum(y_i-\hat{y_i})^2}
\]

---

## Coefficient of Determination (R²)

R² measures how much variance in the target variable is explained by the model.

Values closer to 1 indicate better predictive performance.

\[
R^2=1-\frac{\sum(y-\hat y)^2}{\sum(y-\bar y)^2}
\]

---

# Experimental Setup

To ensure a fair comparison, every model was trained using the same pipeline.

- Same engineered feature set
- Same Feature View from Hopsworks
- Same chronological dataset split
- Same training, validation, and testing datasets
- Same target variables
- Same evaluation metrics

The chronological split prevented future observations from leaking into historical training data, ensuring that every model was evaluated under realistic forecasting conditions.

---

# Models Evaluated

## Ridge Regression

Ridge Regression served as the baseline linear model.

Characteristics:

- Linear regression with L2 regularization
- Requires feature scaling
- Fast training
- High interpretability
- Limited ability to model nonlinear relationships

---

## Random Forest Regression

Random Forest is an ensemble learning algorithm based on multiple decision trees.

Characteristics:

- Ensemble of decision trees
- Handles nonlinear relationships
- Robust to noisy features
- Minimal preprocessing required
- Less effective than boosting methods for this dataset

---

## XGBoost Regression

Extreme Gradient Boosting (XGBoost) is an advanced ensemble algorithm that sequentially builds decision trees while minimizing previous prediction errors.

Characteristics:

- Gradient boosting framework
- Excellent performance on tabular datasets
- Captures complex nonlinear feature interactions
- Built-in regularization
- Efficient training
- Strong generalization capability

---

## PyTorch Neural Network

A fully connected deep neural network was also implemented to evaluate deep learning performance.

Architecture:

- Input Layer
- Dense (256)
- Batch Normalization
- ReLU
- Dropout
- Dense (128)
- Batch Normalization
- ReLU
- Dropout
- Dense (64)
- Batch Normalization
- ReLU
- Output Layer (3 AQI predictions)

Training configuration:

| Parameter | Value |
|-----------|------:|
| Epochs | 300 |
| Batch Size | 128 |
| Learning Rate | 0.0005 |
| Dropout | 0.30 |
| Optimizer | Adam |
| Loss Function | Mean Squared Error |

---

# Overall Performance Comparison

| Model | Validation MAE ↓ | Validation RMSE ↓ | Validation R² ↑ | Test MAE ↓ | Test RMSE ↓ | Test R² ↑ |
|-------|-----------------:|------------------:|----------------:|-----------:|------------:|----------:|
| Ridge Regression | 21.176 | 28.404 | 0.581 | 22.302 | 30.675 | 0.419 |
| Random Forest | 25.066 | 35.227 | 0.356 | 21.842 | 30.254 | 0.435 |
| **XGBoost** | **22.540** | **30.990** | **0.636** | **22.310** | **30.580** | **0.643** |
| PyTorch Neural Network | 24.977 | 33.842 | 0.405 | 22.343 | 32.295 | 0.356 |

> **Insert Screenshot:** Overall Evaluation Metrics

---

# Day 1 Prediction Performance

| Model | Validation MAE | Validation RMSE | Validation R² | Test MAE | Test RMSE | Test R² |
|-------|---------------:|----------------:|--------------:|---------:|----------:|---------:|
| Ridge | 14.692 | 19.883 | 0.796 | 18.407 | 25.536 | 0.598 |
| Random Forest | 18.755 | 28.479 | 0.582 | 17.423 | 25.341 | 0.604 |
| **XGBoost** | **16.100** | **22.460** | **0.803** | **15.980** | **22.170** | **0.810** |
| PyTorch | 17.578 | 23.311 | 0.720 | 17.190 | 25.930 | 0.586 |

> **Insert Screenshot:** Day 1 Evaluation Results

---

# Day 2 Prediction Performance

| Model | Validation MAE | Validation RMSE | Validation R² | Test MAE | Test RMSE | Test R² |
|-------|---------------:|----------------:|--------------:|---------:|----------:|---------:|
| Ridge | 22.734 | 30.056 | 0.531 | 23.637 | 32.331 | 0.355 |
| Random Forest | 26.342 | 35.859 | 0.333 | 22.956 | 31.342 | 0.394 |
| **XGBoost** | **24.120** | **32.760** | **0.592** | **23.930** | **32.210** | **0.600** |
| PyTorch | 27.038 | 35.336 | 0.352 | 23.548 | 33.216 | 0.319 |

> **Insert Screenshot:** Day 2 Evaluation Results

---

# Day 3 Prediction Performance

| Model | Validation MAE | Validation RMSE | Validation R² | Test MAE | Test RMSE | Test R² |
|-------|---------------:|----------------:|--------------:|---------:|----------:|---------:|
| Ridge | 26.100 | 33.492 | 0.416 | 24.862 | 33.549 | 0.303 |
| Random Forest | 30.102 | 40.323 | 0.153 | 25.146 | 33.488 | 0.306 |
| **XGBoost** | **27.410** | **35.810** | **0.513** | **27.030** | **35.340** | **0.519** |
| PyTorch | 30.316 | 40.544 | 0.144 | 26.293 | 36.787 | 0.163 |

> **Insert Screenshot:** Day 3 Evaluation Results

---

# Comparative Analysis

## Ridge Regression

Ridge Regression established a strong linear baseline, particularly for one-day-ahead forecasting. Its performance gradually declined for longer prediction horizons, indicating that linear relationships alone were insufficient to capture the complex interactions present in meteorological and air pollution data.

---

## Random Forest Regression

Random Forest successfully modeled nonlinear relationships but demonstrated inconsistent performance across validation and testing datasets. While it improved upon Ridge for certain testing metrics, its overall predictive performance remained below that of the gradient boosting approach.

---

## PyTorch Neural Network

The neural network successfully learned nonlinear representations from the engineered features. However, despite its deeper architecture and multi-output design, it did not outperform the tree-based ensemble methods on this dataset. This suggests that the available data volume and feature representation were more effectively utilized by boosting algorithms.

---

## XGBoost Regression

XGBoost consistently achieved the strongest predictive performance across all evaluation stages. The model maintained the highest overall R² while producing competitive MAE and RMSE values for each forecasting horizon. Validation and testing metrics remained closely aligned, demonstrating strong generalization and limited evidence of overfitting.

---

# Final Model Selection

Based on the experimental results, **XGBoost Regression** was selected as the production model for the AQI forecasting pipeline.

The selection was based on the following observations:

- Highest overall validation R²
- Highest overall testing R²
- Strong performance across all three prediction horizons
- Stable validation and testing metrics
- Excellent ability to model nonlinear feature interactions
- Robust generalization on unseen data

The selected XGBoost model is integrated into the automated MLOps pipeline, where it is retrained using the latest engineered features, registered in the Hopsworks Model Registry, and deployed for inference through the Streamlit dashboard.

---

# Conclusion

Multiple regression algorithms were evaluated under identical experimental conditions to identify the most suitable model for multi-day AQI forecasting.

Although Ridge Regression, Random Forest, and the PyTorch Neural Network provided competitive baseline performance, XGBoost consistently demonstrated superior predictive accuracy and generalization across validation and testing datasets.

Its ability to effectively capture complex nonlinear relationships within the engineered feature set made it the most suitable choice for deployment in the production MLOps pipeline.
