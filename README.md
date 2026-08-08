<div align="center">

# AQI Predictor

### End-to-End MLOps Pipeline for Multi-Day Air Quality Index Forecasting

<p align="center">
An industry-inspired Machine Learning Operations (MLOps) project that automates the complete lifecycle of Air Quality Index prediction—from data collection and feature engineering to model training, experiment tracking, automated retraining, and interactive visualization.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge)
![Hopsworks](https://img.shields.io/badge/Hopsworks-Feature%20Store-orange?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</p>

</div>

---

# Project Overview

Air pollution is one of the world's leading environmental and public health concerns. Reliable short-term Air Quality Index (AQI) forecasting enables individuals, healthcare organizations, and policymakers to make informed decisions regarding outdoor activities and pollution mitigation.

AQI Predictor is an end-to-end MLOps project designed to forecast the Air Quality Index (AQI) for the **next three days in Lahore Cantonment, Pakistan**. The project automates the complete machine learning lifecycle—from data ingestion and validation to feature engineering, model training, experiment tracking, and interactive visualization.


The pipeline continuously collects historical weather and air pollution data from Open-Meteo APIs, validates incoming data, engineers predictive features, trains multiple machine learning models, tracks experiments using MLflow, stores reusable features in Hopsworks Feature Store, and presents predictions through an interactive Streamlit dashboard.

Unlike traditional machine learning notebooks, this project emphasizes reproducibility, modularity, automation, and scalable engineering practices.

---

#  Objectives

The primary objectives of this project are to:

- Build an automated data ingestion pipeline
- Perform comprehensive feature engineering
- Train and compare multiple models
- Track experiments using MLflow
- Store reusable features in Hopsworks Feature Store
- Automate daily model retraining
- Provide explainable predictions using SHAP
- Visualize results through an interactive Streamlit dashboard
- Demonstrate production-level MLOps workflows

---

#  Features

##  Automated Data Ingestion

- Weather data collection from Open-Meteo Weather API
- Air Quality data collection from Open-Meteo Air Quality API
- Historical hourly observations
- Automated dataset merging

---

##  Data Validation

- Missing value detection
- Duplicate checking
- Schema validation
- Data consistency verification
- Validation reports

---

##  Feature Engineering

- Time-based features
- Cyclical encoding
- Lag features
- Rolling statistics
- Trend features
- Interaction features
- Multi-day prediction targets

---

##  Machine Learning

Multiple regression models are trained and compared including:

- Ridge Regression
- Random Forest Regressor
- XGBoost Regressor
- Neural Network

The best-performing model is selected based on evaluation metrics.

---

## Experiment Tracking

Every experiment is automatically logged using MLflow, including:

- Parameters
- Metrics
- Artifacts
- Feature importance
- Model versions

---

##  Feature Store

The project integrates with **Hopsworks Feature Store** for:

- Centralized feature management
- Feature versioning
- Offline feature retrieval
- Reproducible training datasets

---

##  Automation

GitHub Actions automatically:

- Fetch latest data
- Execute training pipeline
- Retrain models
- Generate updated artifacts

---

##  Dashboard

Interactive Streamlit dashboard featuring:

- AQI Predictions
- Historical AQI Trends
- Weather Insights
- Model Performance
- SHAP Explainability
- Feature Importance

---

# System Architecture



```
                        Open-Meteo APIs
                     (Weather + Air Quality)
                               │
                               ▼
                     Data Ingestion Pipeline
                               │
                               ▼
                      Data Validation Layer
                               │
                               ▼
                     Feature Engineering
                               │
                               ▼
                  Hopsworks Feature Store
                               │
                               ▼
                     Model Training Pipeline
                               │
                               ▼
                       MLflow Tracking
                               │
                               ▼
                    Model Evaluation & Selection
                               │
                               ▼
                    Streamlit Dashboard
```

---

# End-to-End Workflow

```
Weather API
      │
      ▼
Pollution API
      │
      ▼
Data Ingestion
      │
      ▼
Data Validation
      │
      ▼
Feature Engineering
      │
      ▼
Feature Store
      │
      ▼
Model Training
      │
      ▼
Model Evaluation
      │
      ▼
MLflow Tracking
      │
      ▼
Best Model
      │
      ▼
Streamlit Dashboard
```

---

# 🛠️ Technology Stack

| Category | Technologies |
|-----------|-------------|
| Programming Language | Python 3.12  |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly, Matplotlib |
| Machine Learning | Scikit-Learn,Pytorch |
| Experiment Tracking | MLflow |
| Feature Store | Hopsworks |
| Dashboard | Streamlit |
| Automation | GitHub Actions |
| Database | Supabase |
| APIs | Open-Meteo Weather API, Open-Meteo Air Quality API |

---

# 📸 Dashboard Preview

<img width="957" height="387" alt="image" src="https://github.com/user-attachments/assets/b01d485b-a36a-4221-aad5-b36f80324229" />
<img width="956" height="311" alt="image" src="https://github.com/user-attachments/assets/02533ff0-5033-42b6-9eff-ad636d4839a9" />
<img width="952" height="275" alt="image" src="https://github.com/user-attachments/assets/c7d17c1e-f69c-452e-8188-461ef04d287d" />
<img width="959" height="311" alt="image" src="https://github.com/user-attachments/assets/83eb2d0f-226e-4670-a53a-2e4402b1794b" />
<img width="921" height="359" alt="image" src="https://github.com/user-attachments/assets/a7c1fc4e-e1b7-4cdd-a0f3-d54b1d244a3b" />
<img width="938" height="278" alt="image" src="https://github.com/user-attachments/assets/e0fb03d8-ea7f-46a1-bc5a-7ac1607e4ff5" />
<img width="924" height="208" alt="image" src="https://github.com/user-attachments/assets/1adb6f6d-8217-44de-adf3-236c715e0862" />
<img width="905" height="286" alt="image" src="https://github.com/user-attachments/assets/b5069a3e-cec0-47f8-b032-878927235f78" />

> **Note:** The dashboard serves predictions generated by the **XGBoost Regressor**, which was selected as the final deployment model after comparing multiple regression algorithms using validation and test performance metrics.

# 📂 Repository Structure

```text
aqi-predictor/

├── .devcontainer/
├── .github/
│   └── workflows/
│
├── app/
│
├── docs/
│
├── notebooks/
│
├── reports/
│   └── figures/
│
├── src/
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── requirements-render.txt
└── README.md
```
# Getting Started

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.12 or later
- Git
- MLflow
- Hopsworks Account
- Supabase Project
- Open-Meteo APIs (No API key required)

---

## Clone the Repository

```bash
git clone https://github.com/Zarminaa/aqi-predictor.git

cd aqi-predictor
```

---

## Create a Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

Using pip:

```bash
pip install -r requirements.txt
```

or

```bash
pip install -e .
```

---

# ⚙️ Configuration

The project uses environment variables for configuring external services.

Create a `.env` file in the project root using the provided template:

```bash
cp .env.example .env
```

Configure the required credentials:

```env
SUPABASE_URL=
SUPABASE_KEY=

HOPSWORKS_API_KEY=

```

# 🔄 Pipeline Overview

The project follows a modular MLOps workflow where every stage is isolated into reusable components.

```
Weather API
        │
        ▼
Pollution API
        │
        ▼
Raw Dataset
        │
        ▼
Validation
        │
        ▼
Feature Engineering
        │
        ▼
Feature Store
        │
        ▼
Training
        │
        ▼
Evaluation
        │
        ▼
Experiment Tracking
        │
        ▼
Dashboard
```

---

#  Data Ingestion

Historical weather and air quality observations are automatically collected from Open-Meteo APIs.

The ingestion pipeline is responsible for:

- Downloading hourly weather observations
- Downloading hourly pollution observations
- Merging datasets
- Saving raw datasets
- Preparing data for downstream pipelines

---

# 🔍 Data Validation

Before model training, the datasets are validated to ensure high data quality.

Validation includes:

- Missing value analysis
- Duplicate detection
- Schema validation
- Data type verification
- Summary report generation

---

# ⚙️ Feature Engineering

The project creates a comprehensive set of predictive features, including:

### Temporal Features

- Hour
- Day
- Month
- Weekday

### Cyclical Features

- Hour (sin/cos)
- Month (sin/cos)
- Day of week (sin/cos)

### Lag Features

Historical AQI values from previous hours.

### Rolling Statistics

- Rolling Mean
- Rolling Standard Deviation
- Rolling Maximum
- Rolling Minimum

### Trend Features

Rolling trend indicators capturing AQI movement over time.

### Interaction Features

Combined weather and pollution relationships for richer model learning.

---

#  Model Training

Multiple regression algorithms are trained and evaluated.

Current models include:

- Ridge Regression
- Random Forest Regressor
- XGBoost Regressor
- 

Each model is trained using identical datasets for fair comparison.

Evaluation metrics are automatically calculated and logged.

---

# Experiment Tracking (MLflow)

Every experiment is tracked automatically.

Logged information includes:

- Hyperparameters
- Evaluation Metrics
- Feature Importance
- SHAP Visualizations
- Trained Models
- Artifacts

This enables experiment reproducibility and model comparison.

---

#  Feature Store (Hopsworks)

Engineered features are stored in Hopsworks Feature Store to support reproducible machine learning workflows.

Benefits include:

- Centralized feature management
- Version-controlled datasets
- Offline feature retrieval
- Consistent training pipelines
- Scalable feature reuse

---

# Automated Training

GitHub Actions is used to automate model retraining.

The scheduled workflow performs:

- Repository checkout
- Dependency installation
- Data updates
- Feature engineering
- Model training
- Evaluation
- Artifact generation

This enables continuous model updates without manual intervention.

---

# Streamlit Dashboard

The dashboard provides an interactive interface for exploring predictions and model insights.

Features include:

- AQI Prediction
- Historical Trends
- Weather Conditions
- Feature Importance
- SHAP Explainability
- Model Evaluation Metrics

Launch locally:

```bash
streamlit run app/streamlit_app.py
```


#  Project Organization

The repository follows a modular architecture to promote maintainability and scalability.

Each component of the pipeline is isolated into dedicated modules, making it easier to extend or replace individual stages without affecting the rest of the workflow.

This structure supports reproducibility, collaborative development, and production-oriented machine learning practices.


# Model Performance

The trained models are evaluated using standard regression metrics to measure prediction accuracy and generalization performance.

## Evaluation Metrics

- **MAE (Mean Absolute Error)** – Measures the average prediction error.
- **RMSE (Root Mean Squared Error)** – Penalizes larger prediction errors.
- **R² Score (Coefficient of Determination)** – Indicates how well the model explains the variance in AQI values.


---

# 🤝 Contributing

Contributions are welcome!

If you'd like to improve this project:

1. Fork the repository.
2. Create a new feature branch.

```bash
git checkout -b feature/your-feature-name
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push your branch.

```bash
git push origin feature/your-feature-name
```

5. Open a Pull Request.

Please ensure that your code follows the project's style guidelines and includes appropriate documentation where necessary.

---

#  Project Status

Current development includes:

- Automated data ingestion
- Data validation
- Feature engineering
- Feature Store integration
- MLflow experiment tracking
- Multiple regression models
- SHAP explainability
- Streamlit dashboard
- GitHub Actions automation

---

# 📄 License

This project is licensed under the MIT License.

See the `LICENSE` file for more information.

---

# 🙋 Author

<div align="center">

## Zarmina Amjad

AI • Machine Learning • Data Science • MLOps

GitHub: https://github.com/Zarminaa

LinkedIn: https://www.linkedin.com/in/zarmina-a-0403b2319/
</div>

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future development.

---

<div align="center">

### Thank you for visiting this repository! ❤️

</div>
