# AI Data Analyst

An AI-powered Data Analysis application built with Streamlit, Pandas, SQLite, and Groq LLMs.

The application supports:

* Automated Data Cleaning
* Automated EDA Summary Generation
* ML Readiness Assessment
* Natural Language SQL Querying
* Automatic Chart Generation
* Dataset Export After Cleaning


## Features

### 1. Data Cleaning Mode

The application automatically analyzes uploaded datasets and performs intelligent cleaning operations.

Supported cleaning operations:

* Missing value imputation

  * Mean
  * Median
  * Mode
* Outlier detection using IQR
* Outlier removal (when safe)
* High-missing-value column removal
* Identifier column detection and removal
* Data type conversion

After cleaning, the system generates:

* Cleaning Summary
* EDA Summary
* Strengths and Weaknesses
* ML Readiness Score
* Recommendations

The cleaned dataset can be downloaded as a CSV file.

---

### 2. Data Querying Mode

Users can ask questions in natural language.

Examples:

* What is the average salary?
* Show the top 5 customers by revenue.
* Which department has the highest sales?
* Show monthly sales trends.

The system:

1. Converts natural language into SQL.
2. Executes the query on SQLite.
3. Generates a concise answer.
4. Automatically selects a chart when useful.

Supported charts:

* Bar Charts
* Line Charts

---

## Tech Stack

### Frontend

* Streamlit

### Data Processing

* Pandas
* NumPy

### Database

* SQLite

### LLM

* Groq
* Llama 3.3 70B Versatile

### Visualization

* Matplotlib

---

## Project Structure

ai_data_analyst/

├── ai_data_analyst.py
├── cleaning.py
├── conversion.py
├── database.py
├── chart.py
├── requirements.txt
├── README.md
└── .gitignore

## Workflow

### Data Cleaning Workflow

Upload Dataset
      ↓
Basic Cleaning
      ↓
Data Type Conversion
      ↓
Dataset Profiling
      ↓
LLM Cleaning Recommendations
      ↓
Automatic Cleaning Execution
      ↓
EDA Summary
      ↓
ML Readiness Assessment
      ↓
Download Cleaned Dataset

### Data Query Workflow

Upload Dataset
      ↓
Store in SQLite
      ↓
Ask Question
      ↓
LLM SQL Generation
      ↓
Execute Query
      ↓
Generate Answer
      ↓
Generate Chart


## Example Use Cases

* Data Cleaning Automation
* Exploratory Data Analysis
* Dataset Quality Assessment
* Business Intelligence Reporting
* SQL Learning and Exploration
* Machine Learning Dataset Preparation


## Future Improvements

* LangGraph Integration
* MCP Integration
* Agentic Workflow Support
* PDF Report Export
* Advanced Visualizations
* Multi-table SQL Querying
* Resume and Job Analytics Modules


## Author

Ben Jigi

AI Engineer | Data Science | Generative AI

```
