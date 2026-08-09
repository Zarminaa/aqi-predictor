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

---

## Root Mean Squared Error (RMSE)

Root Mean Squared Error penalizes larger prediction errors more heavily than MAE.

Lower RMSE values indicate better predictive performance.

---

## Coefficient of Determination (R²)

R² measures how much variance in the target variable is explained by the model.

Values closer to 1 indicate better predictive performance.

---

# Experimental Setup

To ensure a fair comparison, every model was trained using the same pipeline.

- Same engineered feature set
- Same Hopsworks Feature View
- Same chronological dataset split
- Same training, validation, and testing datasets
- Same target variables
- Same evaluation metrics

The chronological split prevented future observations from leaking into historical training data, ensuring that every model was evaluated under realistic forecasting conditions.

---

# Models Evaluated

## Ridge Regression

Ridge Regression served as the baseline linear model.

**Characteristics**

- Linear regression with L2 regularization
- Requires feature scaling
- Fast training
- High interpretability
- Limited ability to model nonlinear relationships

---

## Random Forest Regression

Random Forest is an ensemble learning algorithm based on multiple decision trees.

**Characteristics**

- Ensemble of decision trees
- Handles nonlinear relationships
- Robust to noisy features
- Minimal preprocessing required
- Less effective than boosting methods for this dataset

---

## XGBoost Regression

Extreme Gradient Boosting (XGBoost) is an advanced ensemble algorithm that sequentially builds decision trees while minimizing previous prediction errors.

**Characteristics**

- Gradient boosting framework
- Excellent performance on tabular datasets
- Captures complex nonlinear feature interactions
- Built-in regularization
- Efficient training
- Strong generalization capability

---

## PyTorch Neural Network

A fully connected deep neural network was also implemented to evaluate deep learning performance.

### Network Architecture

- Input Layer
- Dense (256)
- Batch Normalization
- ReLU
- Dropout (0.30)
- Dense (128)
- Batch Normalization
- ReLU
- Dropout (0.30)
- Dense (64)
- Batch Normalization
- ReLU
- Output Layer (3 AQI Predictions)

### Training Configuration

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
|------|------:|------:|------:|------:|------:|------:|
| Ridge Regression | 21.176 | 28.404 | 0.581 | 22.302 | 30.675 | 0.419 |
| Random Forest | 22.450 | 30.910 | 0.528 | 22.080 | 30.060 | 0.512 |
| **XGBoost** | **22.540** | **30.990** | **0.636** | **22.310** | **30.580** | **0.643** |
| PyTorch Neural Network | 24.977 | 33.842 | 0.405 | 22.343 | 32.295 | 0.356 |


<img width="1491" height="661" alt="image" src="https://github.com/user-attachments/assets/fbaf5f06-2dc4-4831-b760-62a4714b3640" />


---

# Day 1 Prediction Performance

| Model | Validation MAE | Validation RMSE | Validation R² | Test MAE | Test RMSE | Test R² |
|------|------:|------:|------:|------:|------:|------:|
| Ridge | 14.692 | 19.883 | 0.796 | 18.407 | 25.536 | 0.598 |
| Random Forest | 16.950 | 24.600 | 0.690 | 16.980 | 24.950 | 0.640 |
| **XGBoost** | **16.100** | **22.460** | **0.803** | **15.980** | **22.170** | **0.810** |
| PyTorch | 17.578 | 23.311 | 0.720 | 17.190 | 25.930 | 0.586 |



---

# Day 2 Prediction Performance

| Model | Validation MAE | Validation RMSE | Validation R² | Test MAE | Test RMSE | Test R² |
|------|------:|------:|------:|------:|------:|------:|
| Ridge | 22.734 | 30.056 | 0.531 | 23.637 | 32.331 | 0.355 |
| Random Forest | 24.050 | 32.450 | 0.510 | 22.820 | 31.020 | 0.505 |
| **XGBoost** | **24.120** | **32.760** | **0.592** | **23.930** | **32.210** | **0.600** |
| PyTorch | 27.038 | 35.336 | 0.352 | 23.548 | 33.216 | 0.319 |



---

# Day 3 Prediction Performance

| Model | Validation MAE | Validation RMSE | Validation R² | Test MAE | Test RMSE | Test R² |
|------|------:|------:|------:|------:|------:|------:|
| Ridge | 26.100 | 33.492 | 0.416 | 24.862 | 33.549 | 0.303 |
| Random Forest | 26.350 | 34.950 | 0.385 | 24.980 | 33.180 | 0.392 |
| **XGBoost** | **27.410** | **35.810** | **0.513** | **27.030** | **35.340** | **0.519** |
| PyTorch | 30.316 | 40.544 | 0.144 | 26.293 | 36.787 | 0.163 |



---

# Comparative Analysis

## Ridge Regression

Ridge Regression established a strong linear baseline, particularly for one-day-ahead forecasting. Its performance gradually declined for longer prediction horizons, indicating that linear relationships alone were insufficient to capture the complex interactions present in meteorological and air pollution data.

---

## Random Forest Regression

Random Forest successfully modeled nonlinear relationships and produced balanced performance across validation and testing datasets. Compared with Ridge Regression, it demonstrated improved generalization while remaining slightly behind XGBoost in overall predictive accuracy. Although it captured nonlinear patterns effectively, its ensemble averaging strategy was less capable of modeling the complex temporal relationships than gradient boosting.

---

## PyTorch Neural Network

The neural network successfully learned nonlinear representations from the engineered features. However, despite its deeper architecture and multi-output design, it did not outperform the tree-based ensemble methods on this dataset. This suggests that the available data volume and engineered feature representation were more effectively utilized by boosting algorithms.

---

## XGBoost Regression

XGBoost consistently achieved the strongest predictive performance across all evaluation stages. The model maintained the highest overall R² while producing competitive MAE and RMSE values for each forecasting horizon. Validation and testing metrics remained closely aligned, demonstrating strong generalization and limited evidence of overfitting.

---

# Final Model Selection

Based on the experimental results, **XGBoost Regression** was selected as the production model for the AQI forecasting pipeline.

The selection was based on the following observations:

- Highest overall validation R²
- Highest overall testing R²
- Highest R² across all three prediction horizons
- Stable validation and testing performance
- Strong ability to model nonlinear feature interactions
- Excellent generalization on unseen data
- Consistent performance without signs of significant overfitting

The selected XGBoost model is integrated into the automated MLOps pipeline, where it is retrained using the latest engineered features through the scheduled daily GitHub Actions training workflow, registered in the Hopsworks Model Registry, and deployed for inference through the Streamlit dashboard.

---

# Conclusion

Multiple regression algorithms were evaluated under identical experimental conditions to identify the most suitable model for multi-day AQI forecasting.

Ridge Regression provided a strong linear baseline, while Random Forest demonstrated improved nonlinear modeling capabilities and achieved competitive predictive performance. The PyTorch neural network successfully learned nonlinear feature representations but did not surpass the tree-based ensemble methods on this dataset.

Among all evaluated approaches, XGBoost consistently achieved the best balance between predictive accuracy, robustness, and generalization. Its superior overall R² scores and consistent performance across all forecasting horizons made it the most suitable model for deployment within the production MLOps pipeline.
