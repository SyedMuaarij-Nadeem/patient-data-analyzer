# src/config.py
import os
import kagglehub

print("Downloading dataset from Kaggle...")
dataset_path = kagglehub.dataset_download("salikhussaini49/prediction-of-sepsis")
csv_files = [f for f in os.listdir(dataset_path) if f.endswith('.csv')]
if not csv_files:
    raise FileNotFoundError("No CSV file found in the downloaded dataset.")
DATA_FILE = os.path.join(dataset_path, csv_files[0])
print(f"Dataset downloaded to: {DATA_FILE}")

# Output paths
OUTPUT_REPORT     = "output/analysis_report.txt"       # legacy .txt fallback
OUTPUT_REPORT_HTML = "output/analysis_report.html"     # v2 HTML report (dataset mode)
OUTPUT_ANOMALIES  = "output/anomalies.csv"

# Columns we want to analyze
NUMERICAL_FEATURES = [
    "Age",
    "HR",
    "O2Sat",
    "Temp",
    "SBP",
    "MAP",
    "DBP",
    "Resp",
    "Glucose"
]

CATEGORICAL_FEATURES = [
    "Gender"
]

IDENTIFIER_COLUMNS = [
    "Patient_ID",
    "Hour"
]

# Sepsis label column (present in dataset)
SEPSIS_LABEL_COLUMN = "SepsisLabel"

# Z-score threshold — |z| > 2 means statistically unusual
Z_SCORE_THRESHOLD = 2

# Number of rows randomly sampled for chart visualisation.
# Statistics (mean, std, etc.) still use the full dataset.
CHART_SAMPLE_SIZE = 30_000
