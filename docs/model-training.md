# Model Training

## Overview

Model training is the stage of the machine learning pipeline in which engineered features are used to learn predictive relationships between historical environmental conditions and future Air Quality Index (AQI) values. The objective of this stage is to train regression models capable of forecasting AQI for the next three days using the engineered dataset stored within the Hopsworks Feature Store.

Unlike traditional machine learning workflows that rely on locally stored datasets, this project retrieves engineered features directly from the Hopsworks Feature View. This ensures that every training run uses a consistent, version-controlled feature set and promotes reproducibility across experiments.

To identify the most suitable forecasting model, multiple machine learning algorithms were trained and evaluated. The project includes implementations of Ridge Regression, Random Forest Regression, XGBoost Regression, and a custom deep neural network developed using PyTorch. Each model was trained using the same engineered features, chronological data split, and evaluation metrics to enable a fair comparison of their predictive performance.

After training, each model is evaluated on both validation and testing datasets before being exported as a complete model artifact. Relevant metadata, evaluation metrics, feature information, and preprocessing objects are stored alongside the trained model to facilitate reproducibility and deployment. Finally, every trained model is registered within the Hopsworks Model Registry, enabling centralized version management and experiment tracking.

---

# Training Pipeline Architecture

The training stage follows a modular pipeline in which engineered features are retrieved from the Feature Store, preprocessed, used for model training, evaluated, and finally registered for deployment.

```text
Hopsworks Feature View
          │
          ▼
Load Training Dataset
          │
          ▼
Chronological Data Split
          │
          ▼
Feature Scaling (if required)
          │
          ▼
Model Training
          │
          ▼
Validation Evaluation
          │
          ▼
Test Evaluation
          │
          ▼
Model Export
          │
          ▼
Model Registry
```

Each stage is implemented as an independent module, allowing individual components of the training pipeline to be reused, tested, and maintained separately.

---

# Loading the Training Dataset

## Overview

The training pipeline begins by loading the engineered dataset from the Hopsworks Feature Store. Rather than reading the locally generated `features.csv` file, the project retrieves data directly from the Feature View, ensuring that model training always uses the latest engineered features available within the centralized Feature Store.

This approach establishes a single source of truth for machine learning features and eliminates inconsistencies that can arise from maintaining multiple local copies of the dataset.

---

## Loading Data from the Feature View

By default, the training pipeline retrieves the most recent engineered features directly from the Feature View.

The Feature View combines all engineered features together with the corresponding prediction targets, allowing the training pipeline to obtain a complete machine learning dataset using a single interface.

Loading data directly from the Feature View ensures that every training execution uses the latest version of the engineered features without requiring manual dataset management.

---

## Loading a Materialized Training Dataset

In addition to loading data directly from the Feature View, the pipeline also supports loading previously materialized training datasets stored within Hopsworks.

Materialized training datasets represent versioned snapshots of the Feature View at a specific point in time. These snapshots are particularly useful for reproducing previous experiments or comparing model performance across different dataset versions.

When a training dataset version is provided, the pipeline loads that specific version instead of retrieving the latest Feature View data.

---

## Training Dataset Structure

After loading the data, the Feature View returns two separate components:

- Feature columns containing the engineered predictors.
- Target columns representing AQI values for the next three forecast horizons.

 # Chronological Dataset Splitting

## Overview

Once the engineered dataset has been retrieved from the Hopsworks Feature View, it is divided into training, validation, and testing subsets before model training begins.

Since AQI forecasting is a time-series regression problem, maintaining the chronological order of observations is essential. Unlike conventional machine learning tasks where data can be randomly shuffled, time-series forecasting requires that models learn only from historical observations and are evaluated on future data.

To prevent information leakage, the project implements a chronological data splitting strategy that preserves the temporal sequence of the dataset throughout the training process.

---

## Training, Validation, and Testing Split

The dataset is divided using the following proportions:

| Dataset | Ratio | Purpose |
|---------|------:|---------|
| Training Set | 80% | Model learning |
| Validation Set | 10% | Hyperparameter tuning and model selection |
| Test Set | 10% | Final performance evaluation |

Rather than randomly sampling observations, the dataset is split sequentially according to time.

The earliest observations are assigned to the training set, followed by the validation set, while the most recent observations are reserved for testing. This methodology closely resembles real-world forecasting scenarios, where future observations are unavailable during model development.

---

## Chronological Splitting Strategy

If the dataset contains a `datetime` column, the observations are first sorted in ascending chronological order before splitting.

After sorting:

- The first 80% of observations form the training dataset.
- The next 10% form the validation dataset.
- The remaining 10% form the testing dataset.

This strategy prevents future observations from influencing the training process and produces a more realistic estimate of model performance.

---

## Feature and Target Separation

Following dataset splitting, the training pipeline separates the engineered features from the prediction targets.

The following columns are excluded from the feature matrix:

- `datetime`
- `target_day1`
- `target_day2`
- `target_day3`

The remaining columns constitute the input feature matrix used during model training.

The prediction labels are stored separately and supplied to the learning algorithms during training and evaluation.

---

# Multi-Day Prediction Targets

The objective of the project is to forecast AQI values for three future days simultaneously.

To support this objective, the feature engineering pipeline generates three target variables:

| Target | Forecast Horizon |
|---------|------------------|
| `target_day1` | AQI after 24 hours |
| `target_day2` | AQI after 48 hours |
| `target_day3` | AQI after 72 hours |

These targets are produced by shifting the historical AQI values by one, two, and three days respectively during the feature engineering stage.

The training pipeline supports both single-output and multi-output regression. For the final implementation, all three target variables are trained together as a multi-output regression problem, allowing each model to predict AQI values for the next three days within a single inference.

---

# Feature Scaling

## Overview

Many machine learning algorithms are sensitive to differences in feature magnitude. Variables measured on larger numerical scales can dominate the optimization process, resulting in slower convergence or reduced predictive performance.

To address this issue, the training pipeline includes an optional feature scaling stage that standardizes numerical features before model training.

Unlike conventional workflows where every model receives scaled data, this project automatically determines whether feature scaling is required based on the selected learning algorithm.

---

## Conditional Scaling

Each training function specifies whether feature scaling is required.

Models that depend on feature magnitude automatically receive standardized input features, while tree-based algorithms are trained using the original engineered feature values.

This design allows every algorithm to use the preprocessing strategy that best suits its underlying learning mechanism without requiring manual configuration.

---

## Models Requiring Feature Scaling

Feature scaling is applied when training the following models:

- Ridge Regression
- PyTorch Neural Network

These algorithms optimize numerical parameters using gradient-based optimization techniques or regularized linear regression, both of which benefit from standardized feature distributions.

Scaling improves optimization stability, accelerates convergence, and prevents features with larger numerical ranges from dominating the learning process.

---

## Models Not Requiring Feature Scaling

Tree-based algorithms perform recursive feature partitioning rather than distance-based optimization.

Consequently, the following models are trained using the original engineered feature values:

- Random Forest Regression
- XGBoost Regression

Since decision trees are insensitive to monotonic transformations of the input variables, applying feature scaling provides little or no improvement in predictive performance while introducing unnecessary preprocessing overhead.

---

## Saving the Feature Scaler

Whenever feature scaling is applied, the fitted scaler is exported alongside the trained model.

Storing the scaler ensures that future inference data undergoes the same preprocessing transformations used during training, maintaining consistency between model development and deployment.

During prediction, incoming feature values are transformed using the saved scaler before being passed to the trained model, ensuring reliable and reproducible predictions.

# Machine Learning Models

## Overview

To identify the most suitable algorithm for multi-day AQI forecasting, the project implements and evaluates four different regression models. These models were selected to represent a diverse range of machine learning approaches, including linear models, ensemble tree-based methods, gradient boosting techniques, and deep neural networks.

Each model is trained using the same engineered feature set, chronological dataset split, and evaluation methodology, ensuring a fair comparison of predictive performance.

The models implemented in this project are:

- Ridge Regression
- Random Forest Regression
- XGBoost Regression
- PyTorch Neural Network

---

# Ridge Regression

## Overview

Ridge Regression serves as the baseline model for the forecasting system.

It is a linear regression algorithm that incorporates L2 regularization to reduce overfitting by penalizing excessively large model coefficients. This regularization improves generalization while maintaining a relatively simple and interpretable model.

Because Ridge Regression relies on gradient-based optimization and coefficient estimation, standardized feature values are used during training.

---

## Training Procedure

The Ridge Regression model is trained using the engineered feature matrix together with the three AQI prediction targets.

Prior to training, all numerical features are standardized using the project's feature scaling pipeline. The fitted scaler is preserved and exported alongside the trained model to ensure identical preprocessing during inference.

The implementation uses Scikit-learn's `Ridge` estimator with a fixed random seed to improve reproducibility across training runs.

---

# Random Forest Regression

## Overview

Random Forest Regression is an ensemble learning algorithm that combines the predictions of multiple decision trees.

Rather than relying on a single tree, the model constructs numerous independent decision trees using randomly sampled subsets of both the observations and feature space. The final prediction is obtained by averaging the predictions of all individual trees.

This ensemble strategy generally produces better predictive performance and greater robustness than a single decision tree.

---

## Training Procedure

The Random Forest model is trained directly on the engineered features without feature scaling.

Since decision trees perform recursive feature partitioning instead of numerical optimization, scaling the input variables does not significantly influence model performance.

The implementation utilizes the Scikit-learn `RandomForestRegressor`, allowing multiple trees to be trained in parallel for improved computational efficiency.

---

# XGBoost Regression

## Overview

Extreme Gradient Boosting (XGBoost) is an advanced ensemble learning algorithm based on gradient boosted decision trees.

Unlike Random Forest, which trains trees independently, XGBoost builds trees sequentially. Each successive tree focuses on correcting the prediction errors made by the previous trees, gradually improving overall model performance.

Its ability to model highly nonlinear relationships while incorporating regularization makes XGBoost particularly well suited for structured environmental datasets such as weather observations and air quality measurements.

---

## Training Procedure

The XGBoost model is trained using the same engineered features generated during the feature engineering stage.

As a tree-based learning algorithm, it operates directly on the original feature values without requiring feature scaling.

Throughout experimentation, XGBoost consistently demonstrated strong predictive performance and served as one of the primary candidate models for the final forecasting system.

---

# PyTorch Neural Network

## Overview

In addition to conventional machine learning algorithms, the project implements a custom deep neural network using the PyTorch framework.

The neural network is designed to learn complex nonlinear relationships between meteorological variables, historical pollution measurements, engineered temporal features, and future AQI values.

Unlike traditional regression models, the neural network simultaneously predicts AQI values for all three forecast horizons using a multi-output regression architecture.

---

## Network Architecture

The neural network consists of four fully connected layers arranged in a feed-forward architecture.

The architecture follows the sequence:

```text
Input Features
      │
      ▼
Linear Layer (256)
      │
Batch Normalization
      │
ReLU Activation
      │
Dropout
      │
      ▼
Linear Layer (128)
      │
Batch Normalization
      │
ReLU Activation
      │
Dropout
      │
      ▼
Linear Layer (64)
      │
Batch Normalization
      │
ReLU Activation
      │
      ▼
Output Layer
```

Batch normalization layers improve training stability by reducing internal covariate shift, while ReLU activation functions introduce nonlinearity into the model.

Dropout layers are included within the network to reduce overfitting by randomly disabling neurons during training.

---

# Training Configuration

The PyTorch implementation uses a fixed set of training hyperparameters throughout experimentation.

| Hyperparameter | Value |
|---------------|------:|
| Batch Size | 128 |
| Learning Rate | 0.0005 |
| Number of Epochs | 300 |
| Dropout Rate | 0.30 |
| Random Seed | 42 |

These values were selected to provide stable optimization while balancing convergence speed and model generalization.

---

## Optimization Strategy

The neural network is trained using the Adam optimization algorithm together with Mean Squared Error (MSE) as the loss function.

During training:

- The model processes data in mini-batches.
- Predictions are generated for each batch.
- The Mean Squared Error loss is computed.
- Gradients are calculated using backpropagation.
- Adam updates the network parameters.
- The process repeats for every epoch.

Validation performance is evaluated after every ten training epochs.

Rather than simply saving the model from the final epoch, the training pipeline continuously monitors validation performance and preserves the model achieving the highest validation coefficient of determination (R²). This best-performing model is restored after training has completed and is subsequently used for final testing, export, and registration.

# Model Evaluation

## Overview

After each model has completed training, its predictive performance is assessed using both validation and testing datasets.

The validation dataset is used during model development to compare candidate models and monitor learning performance, while the testing dataset remains completely unseen throughout training and provides an unbiased estimate of the model's generalization capability.

To ensure consistency across all algorithms, every model is evaluated using the same regression metrics and identical chronological dataset splits.

---

## Evaluation Metrics

The project evaluates regression performance using three complementary metrics:

| Metric | Purpose |
|---------|---------|
| Mean Absolute Error (MAE) | Measures the average absolute prediction error. |
| Root Mean Squared Error (RMSE) | Penalizes larger prediction errors more heavily than MAE. |
| Coefficient of Determination (R²) | Measures how well the model explains the variance in AQI values. |

These metrics provide a comprehensive assessment of prediction accuracy, robustness, and explanatory power.

---

## Multi-Output Evaluation

Since the forecasting system predicts AQI for three future days simultaneously, evaluation is performed separately for each prediction horizon.

Performance metrics are calculated independently for:

- Day 1 Forecast
- Day 2 Forecast
- Day 3 Forecast

In addition to individual day metrics, overall multi-output performance is computed by averaging prediction performance across all target variables.

This approach provides both detailed insight into individual forecast horizons and an overall measure of model quality.

---

## Validation Evaluation

Following model training, predictions are generated for the validation dataset.

The validation metrics are used to compare competing algorithms and, in the case of the PyTorch neural network, monitor performance during training.

For the neural network implementation, validation evaluation is performed after every ten training epochs. The validation R² score is continuously monitored, and whenever a higher score is achieved, the corresponding model parameters are preserved as the current best-performing model.

This strategy ensures that the final exported neural network corresponds to the highest observed validation performance rather than simply the final training epoch.

---

## Test Evaluation

After model selection has been completed, the chosen model is evaluated using the independent testing dataset.

Unlike the validation dataset, the testing data is never used during model optimization or model selection. Consequently, the reported testing metrics provide an unbiased estimate of how the forecasting system is expected to perform on future unseen observations.

The same evaluation metrics—MAE, RMSE, and R²—are computed for each prediction horizon together with the overall multi-output regression performance.

---

# Model Artifact Export

## Overview

After successful evaluation, every trained model is exported as a complete model artifact.

Rather than saving only the trained model weights, the project packages all components required for future inference, reproducibility, and deployment into a dedicated model directory.

This approach allows the trained models to be deployed independently without requiring access to the original training environment.

---

## Exported Model Components

Each exported model directory contains the following files:

| File | Purpose |
|------|---------|
| `model.pkl` or `model.pt` | Trained machine learning model |
| `metadata.json` | Model metadata and training information |
| `metrics.json` | Validation and testing performance metrics |
| `feature_columns.json` | Ordered list of input features |
| `target_columns.json` | Prediction target names |
| `scaler.pkl` *(optional)* | Feature scaler used during training |

For PyTorch models, the trained neural network weights are stored as `model.pt`, while Scikit-learn models are serialized as `model.pkl`.

Whenever feature scaling is applied, the fitted scaler is exported alongside the trained model to ensure that future inference data undergoes identical preprocessing.

---

## Model Metadata

Each exported model includes a metadata file describing the complete training configuration.

The metadata records:

- Model name
- Machine learning framework
- Learning algorithm
- Feature View name and version
- Training dataset version
- Number of input features
- Number of prediction targets
- Ordered feature names
- Ordered target names
- Scaling requirement
- Model creation timestamp

Maintaining this information improves reproducibility and simplifies future deployment and experiment tracking.

---

# Prediction Export

In addition to saving trained models, the training pipeline exports prediction results generated on the testing dataset.

These prediction files contain the actual AQI values together with the corresponding model predictions, enabling detailed post-training analysis and comparison between different forecasting algorithms.

Exporting prediction results separately simplifies error analysis, visualization, and future benchmarking experiments without requiring models to be executed again.

# Hopsworks Model Registry

## Overview

After a model has been successfully trained, evaluated, and exported, it is registered within the Hopsworks Model Registry.

The Model Registry provides a centralized repository for storing trained machine learning models together with their associated metadata, evaluation metrics, and version information. Registering models enables reproducibility, simplifies deployment, and supports lifecycle management throughout the MLOps workflow.

Rather than maintaining trained models solely as local files, the registry acts as the project's single source of truth for production-ready models.

---

## Model Registration Process

Once the model artifact has been exported, the training pipeline performs the following steps:

1. Connect to the Hopsworks Model Registry.
2. Create a new model entry.
3. Attach the exported model directory.
4. Store validation and testing metrics.
5. Store an input example for inference.
6. Register the model as a versioned artifact.

Each registered model receives its own version number, allowing multiple training runs to coexist without overwriting previous versions.

---

## Stored Model Information

During registration, the following information is recorded:

- Model name
- Model version
- Model description
- Validation metrics
- Testing metrics
- Input example
- Training dataset version (when available)

By preserving both the trained model and its associated metadata, the registry enables future experiments to be reproduced using the exact training configuration.

---

## Framework Support

The project supports registering models trained using multiple machine learning frameworks.

Separate registration implementations are provided for:

- Scikit-learn models
- PyTorch neural networks

Although the underlying serialization formats differ, both registration workflows store evaluation metrics, metadata, and model artifacts using the same version-controlled registry.

---

# Reproducibility

## Overview

Machine learning experiments should produce consistent and repeatable results whenever possible.

To improve reproducibility, the training pipeline explicitly initializes the random number generators used throughout the project before model training begins.

For the PyTorch implementation, reproducibility is achieved by fixing the random seeds for:

- Python's random module
- NumPy
- PyTorch
- CUDA (when GPU acceleration is available)

Additionally, deterministic execution is enabled within the PyTorch backend to reduce variability between training runs.

Using fixed random seeds ensures that data shuffling, weight initialization, and optimization behave consistently across repeated executions under the same computational environment.

---

# Automated Model Training Pipeline

## Overview

To support continuous model development, the project automates the complete training workflow using GitHub Actions.

Instead of manually executing the training pipeline whenever new features become available, model training is performed automatically according to a predefined schedule.

This automation ensures that newly engineered data can be incorporated into updated forecasting models with minimal manual intervention.

---

## Automated Workflow

Each execution of the automated training pipeline performs the following operations:

1. Retrieve the latest engineered dataset from the Hopsworks Feature Store.
2. Split the dataset into training, validation, and testing subsets.
3. Train the selected machine learning model.
4. Evaluate validation and testing performance.
5. Export the trained model artifact.
6. Register the model within the Hopsworks Model Registry.

This workflow enables continuous retraining while maintaining a complete history of model versions and evaluation results.

---

## GitHub Actions Integration

The automated training process is implemented using a GitHub Actions workflow.

The workflow prepares the execution environment, installs the required project dependencies, loads the necessary environment variables, and executes the model training pipeline.

Automating model training provides several important advantages:

- Eliminates manual retraining.
- Ensures models remain synchronized with newly engineered features.
- Enables scheduled retraining using the latest available data.
- Produces reproducible training runs.
- Automatically updates the Hopsworks Model Registry.

The workflow definition is located within the project repository:

```text
.github/workflows/training-pipeline.yml
```

This workflow can be executed automatically according to its schedule or triggered manually whenever retraining is required.

---

# Training Workflow Summary

The complete model training workflow implemented in this project is summarized below.

```text
Hopsworks Feature View
          │
          ▼
Load Training Dataset
          │
          ▼
Chronological Train / Validation / Test Split
          │
          ▼
Feature Scaling (when required)
          │
          ▼
Train Machine Learning Model
          │
          ▼
Validation Evaluation
          │
          ▼
Test Evaluation
          │
          ▼
Export Model Artifact
          │
          ▼
Register Model in Hopsworks
          │
          ▼
Production-Ready Model
```

---

# Conclusion

The model training stage transforms engineered environmental features into predictive machine learning models capable of forecasting Air Quality Index values for the next three days.

By integrating the Hopsworks Feature Store with multiple machine learning algorithms, standardized preprocessing, chronological dataset splitting, comprehensive evaluation, automated model export, and centralized model registration, the project establishes a reproducible and production-oriented training workflow.

Furthermore, the use of GitHub Actions for automated retraining enables the forecasting system to continuously incorporate newly engineered data while maintaining version-controlled model artifacts within the Hopsworks Model Registry. This design forms a key component of the end-to-end MLOps pipeline, ensuring that model development, evaluation, and deployment remain consistent, scalable, and reproducible.

These components are combined into a single DataFrame before the training process begins, providing a unified dataset for preprocessing, model training, and evaluation.
