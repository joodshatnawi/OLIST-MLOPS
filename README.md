# OLIST MLOps

An end-to-end MLOps project built as part of the **Qafza Tech MLOps Training**.

The project takes an Olist Brazilian E-Commerce dataset and builds a production-oriented machine learning pipeline for predicting whether an order will be delivered late.

## Project Overview

The project covers the complete workflow from data preparation and exploratory analysis to model training, validation, experiment tracking, model registration, API serving, testing, and containerization.

### Main ML Task

**Binary classification:** predict whether an order will be delivered late.

The final model is a **Logistic Regression** model with preprocessing and feature engineering.

## Project Structure

```text
olist-mlops/
│
├── app/
│   └── main.py                  # FastAPI application
│
├── config/
│   └── config.json              # Runtime configuration
│
├── data/                        # Dataset managed by DVC
│
├── artifacts/
│   ├── eda/                     # EDA outputs
│   ├── eda_plots/              # EDA visualizations
│   ├── final_model.joblib.dvc  # DVC metadata for final model
│   ├── final_test_results.csv  # Final evaluation metrics
│   ├── feature_config.json
│   └── model_config.json
│
├── notebooks/
│   ├── 01_read_join.ipynb
│   ├── 02_create_labels.ipynb
│   ├── 03_split_data.ipynb
│   ├── 04_eda.ipynb
│   ├── 05_feature_engineering.ipynb
│   └── 06_final_evaluation.ipynb
│
├── src/
│   ├── features.py             # Feature engineering
│   ├── validation.py           # Great Expectations validation
│   ├── predict.py              # Model loading and prediction
│   ├── logging_config.py       # Application logging
│   └── mlflow_tracking.py      # MLflow experiment/model tracking
│
├── tests/
│   ├── test_api.py
│   ├── test_features.py
│   └── test_predict.py
│
├── Dockerfile
├── Dockerfile.mlflow
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── data.dvc
├── pytest.ini
└── .github/workflows/ci.yml
```

## Technologies

* Python 3.10
* Pandas
* Scikit-learn
* FastAPI
* Uvicorn
* MLflow
* Great Expectations
* DVC
* PostgreSQL
* Docker / Docker Compose
* Pytest
* GitHub Actions

## Model

The final model is a Logistic Regression classifier.

### Features

The model uses engineered order-level features including:

* Estimated delivery time
* Number of items
* Total item price
* Total freight value
* Number of unique products
* Number of unique sellers
* Payment information
* Customer location
* Purchase date and time features

The final model includes the preprocessing pipeline and is managed as an ML artifact through MLflow and DVC.

## MLOps Pipeline

The project follows this workflow:

```text
Raw Data
   ↓
Data Preparation
   ↓
Data Validation
   ↓
Feature Engineering
   ↓
Model Training
   ↓
Model Evaluation
   ↓
MLflow Tracking
   ↓
Model Registry
   ↓
FastAPI
   ↓
Docker
```

### Data Versioning

The dataset and final model artifact are versioned using DVC.

Large data files and model binaries are intentionally not stored directly in Git. Git stores the DVC metadata files, while the actual data and model files are managed by DVC.

The current development setup uses a local DVC remote configured outside the repository.

Useful commands:

```bash
dvc status
dvc add data
dvc add artifacts/final_model.joblib

The DVC remote used during development is configured locally and is not committed as a machine-specific path.

### Data Validation

Incoming prediction data is validated before inference using **Great Expectations**.

The validation checks include:

* Required columns
* Missing values
* Numeric data types
* Non-negative values
* Date and timestamp validity

Invalid input is rejected before reaching the model.

### MLflow

MLflow is used for:

* Experiment tracking
* Parameter logging
* Metric logging
* Artifact logging
* Model registration

The registered model is:

```text
OlistLateDeliveryModel
```

The API loads the model through the MLflow Model Registry using the configured alias.

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/joodshatnawi/OLIST-MLOPS.git
cd OLIST-MLOPS
```

### 2. Create the Python environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements-dev.txt
```

## Run Tests

Run the complete test suite with:

```bash
pytest -q
```

The current test suite covers:

* Feature engineering
* Prediction logic
* FastAPI endpoints

## Run with Docker Compose

The recommended way to run the production-style services is:

```bash
docker compose up -d --build
```

This starts:

| Service    | Port | Purpose                                |
| ---------- | ---: | -------------------------------------- |
| FastAPI    | 8000 | Prediction API                         |
| MLflow     | 5000 | Experiment tracking and model registry |
| PostgreSQL | 5432 | MLflow backend database                |

Check running containers:

```bash
docker compose ps
```

## API

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "model_version": "1.0.0"
}
```

### Model Information

```http
GET /model
```

### Single Prediction

```http
POST /predict
```

The API validates the input, generates the required features, loads the registered model, and returns the prediction probability and predicted class.

Example response:

```json
{
  "late_probability": 0.6173,
  "predicted_late": 0,
  "model_version": "1.0.0"
}
```

### Batch Prediction

```http
POST /predict/batch
```

Multiple orders can be submitted in a single request.

## API Documentation

When the FastAPI service is running, interactive API documentation is available at:

```text
http://localhost:8000/docs
```

## CI

GitHub Actions runs the test suite automatically on:

* Pushes
* Pull requests

The workflow installs the project dependencies and runs:

```bash
pytest -q
```

A failing test causes the CI workflow to fail.

## Logging

The application uses Python's logging framework.

Logs include information such as:

* Prediction input
* Prediction output
* Request latency
* Model version
* Batch prediction information

Logs are written to both the console and a local log file.

## Final Evaluation

The final Logistic Regression model was evaluated on a held-out test set.

The evaluation metrics are stored in:

```text
artifacts/final_test_results.csv
```

The final model configuration and prediction threshold are stored separately in:

```text
artifacts/model_config.json
config/config.json
```

## Task 1 – Data & Database

Earlier project work included loading the Olist Brazilian E-Commerce dataset into PostgreSQL and exploring relationships between the dataset tables using SQL queries and JOINs.

## Dataset

**Brazilian E-Commerce Public Dataset by Olist**

The dataset contains information about Brazilian e-commerce orders, customers, products, sellers, payments, reviews, and related entities.

## Author

**Jood Al-Shatnawi**

Built as part of the **Qafza Tech MLOps Training**.
