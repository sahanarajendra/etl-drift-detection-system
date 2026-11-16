# Data ETL Pipeline and Drift Detection System

A Python-based ETL pipeline that automates data extraction, cleaning, transformation, data quality analysis, and statistical drift detection. The project also provides an interactive Streamlit dashboard to visualize data quality, identify changes in datasets, and generate automated recommendations.

## Project Overview

This project helps identify changes in incoming data by comparing it with a reference dataset. It supports both Pandas and PySpark processing engines and uses statistical techniques to detect data drift.

## Key Features

- **Data Extraction:** Loads datasets from CSV files.
- **Data Cleaning:** Handles missing values, duplicate records, and inconsistent data.
- **Data Transformation:** Applies numerical scaling and categorical encoding.
- **Data Quality Analysis:** Evaluates missing values, duplicates, unique values, and quality scores.
- **Drift Detection:** Uses statistical methods to identify changes between reference and current datasets.
- **Automated Recommendations:** Generates suggestions based on detected data quality and drift issues.
- **Data Visualization:** Displays drift analysis through charts.
- **Interactive Dashboard:** Provides a Streamlit interface for uploading and analyzing datasets.
- **Dual Processing Engines:** Supports Pandas and PySpark.
- **Performance Measurement:** Measures ETL processing time for the selected engine.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data manipulation and cleaning |
| PySpark | Distributed data processing |
| NumPy | Numerical operations |
| SciPy | Statistical tests |
| Scikit-learn | Data preprocessing |
| Streamlit | Interactive dashboard |
| Matplotlib & Seaborn | Data visualization |

## Drift Detection Techniques

- Kolmogorov-Smirnov (KS) Test
- Population Stability Index (PSI)
- Wasserstein Distance
- Chi-Square Test

## Project Structure

```text
etl-drift-detection-system/
│
├── app.py
├── prepare_data.py
├── generate_drift_data.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   ├── reference/
│   └── processed/
│
├── src/
│   ├── extraction.py
│   ├── cleaning.py
│   ├── transformation.py
│   ├── data_quality.py
│   ├── drift_detection.py
│   ├── recommendations.py
│   ├── visualization.py
│   └── spark_processing.py
│
├── tests/
└── utils/
```

## Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/sahanarajendra/etl-drift-detection-system.git
```

### 2. Navigate to the project directory

```bash
cd etl-drift-detection-system
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Streamlit application

```bash
python -m streamlit run app.py
```

The dashboard will open in your browser.

## Dataset

The project uses the Bank Marketing dataset for ETL processing and drift analysis. It includes reference, current, and artificially drifted datasets for testing.

The original `bank-full.csv` dataset is excluded from this repository. Obtain it from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/222/bank+marketing) and place it in `data/raw/` if required by the preparation script.

## Testing

Run the project tests using:

```bash
python -m unittest discover -s tests
```

Individual test modules can also be executed separately.

## Project Outcomes

- Automated data processing using Pandas and PySpark.
- Identification of data quality issues.
- Statistical detection of data drift.
- Automated recommendations for detected issues.
- Interactive visualization and dataset analysis through Streamlit.

## Author

**Sahana Rajendra Naik**

GitHub: [sahanarajendra](https://github.com/sahanarajendra)

## License

This project is available for educational and learning purposes.
