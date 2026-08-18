# Hospital Patient Data Analyzer

A Python-based data analysis pipeline designed to process, validate, and analyze large-scale hospital patient datasets.

## Overview

The Hospital Patient Data Analyzer takes raw clinical data (such as vital signs, lab results, and patient demographics) and runs a comprehensive automated analysis pipeline. It evaluates data quality, calculates summary statistics, identifies statistical anomalies (using Z-scores), and computes correlations between key medical features.

## Features

- **Data Loading & Preprocessing:** Efficiently loads CSV data and converts features to numerical arrays using NumPy.
- **Data Quality Checks:** Automatically detects duplicate records, missing data points, and invalid values.
- **Statistical Analysis:** Calculates mean, standard deviation, and other statistics for numerical features (Age, HR, O2Sat, Temp, SBP, MAP, DBP, Resp, Glucose).
- **Anomaly Detection:** Flags extreme outlier observations across features using configurable Z-score thresholds.
- **Correlation Analysis:** Computes Pearson correlation coefficients to discover relationships between physiological variables.
- **Automated Reporting:** Generates a detailed text-based summary report and exports a CSV file of all detected anomalies.

## Project Structure

```
hospital-patient-analyzer/
│
├── data/               # Directory for input CSV datasets
├── output/             # Directory where generated reports and anomalies are saved
├── src/                # Source code directory
│   ├── main.py                 # Main execution script
│   ├── config.py               # Configuration constants (thresholds, file paths)
│   ├── data_loader.py          # Data ingestion and formatting
│   ├── data_quality.py         # Missing value, duplicate, and validation checks
│   ├── feature_statistics.py   # Statistical computation logic
│   ├── anomaly_detection.py    # Outlier detection algorithms
│   ├── correlation.py          # Statistical correlation calculations
│   └── report.py               # Output generation (CSV and txt reports)
│
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Setup and Installation

1. Ensure you have **Python 3** installed on your system.
2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your input dataset in the appropriate location (configured in `src/config.py`, usually `data/`).
2. Run the main analysis script from the root directory of the project:
   ```bash
   python src/main.py
   ```
3. The script will output its progress to the console. Once complete, check the `output/` folder for:
   - `analysis_report.txt`: A human-readable summary of the dataset.
   - `anomalies.csv`: A spreadsheet containing all flagged anomalous observations.

## Requirements

- Python 3.x
- NumPy (see `requirements.txt`)
