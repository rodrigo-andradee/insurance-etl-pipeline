# Insurance ETL Pipeline

## 🚀 Live Demo
👉 **[Try the Insurance Lookup Tool](https://insurance-lookup-tool.streamlit.app/)**

ETL pipeline built with PySpark and Databricks using the Medallion Architecture (Bronze → Silver → Gold), with automated orchestration via Databricks Jobs and an interactive internal lookup tool built with Streamlit.

## Project Overview
This project processes an insurance claims dataset, transforming raw data into a Star Schema ready for business analysis, with engineered fraud indicators and risk levels.

> **Note:** In a real-world scenario, a customer could hold multiple policies across different insurance types (life, health, home, auto). This dataset represents one transaction per customer, which is a common structure in claims datasets.

## Architecture
- **Bronze** → Raw CSV files ingested as-is
- **Silver** → Cleaned and validated data (nulls, duplicates, data types)
- **Gold** → Star Schema with Fact and Dimension tables (Delta Tables)

## Tech Stack
- Python / PySpark
- Databricks (Serverless)
- Delta Lake
- SQL
- Parquet
- Streamlit

## Notebooks
| Notebook | Description |
|---|---|
| 00_exploration | Data exploration and schema analysis |
| 01_extract | Load raw CSV files into Bronze layer |
| 02_silver | Data cleaning and validation |
| 03_gold | Star Schema creation + fraud indicators |
| 04_load | Save as Delta Tables in Unity Catalog |

## Star Schema
- **fact_claims** → Central fact table with claims data
- **dim_customers** → Customer information
- **dim_policies** → Policy and insurance type information
- **dim_agents** → Agent information
- **dim_vendors** → Vendor/expert information
- **dim_dates** → Date dimension extracted from transactions

## Fraud Indicators & Risk Levels
Fraud indicators were engineered using business rules based on the dataset's average claim amount of **$16,563.83**. A claim is flagged as suspicious if:
- The claim amount is more than 2x the average (~$33,127) with no police report available
- The incident severity is Total Loss with no injuries reported

Risk level is classified as:
- **High** → Claim amount above 2x the average
- **Medium** → Claim amount above the average
- **Low** → Claim amount below the average

## Orchestration
The pipeline is orchestrated using Databricks Workflows, scheduled to run daily at 6AM (Europe/Lisbon). See `job_config.json` for the full configuration.

## Streamlit App
An internal lookup tool built with Streamlit allows users to search for a customer by ID or name and view their claims history and fraud risk assessment.

## Dataset
[Insurance Claims Fraud Data — Kaggle](https://www.kaggle.com/datasets/mastmustu/insurance-claims-fraud-data)
