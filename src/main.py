# src/main.py
import os
import math
import numpy as np
from config import (
    DATA_FILE,
    OUTPUT_REPORT,
    OUTPUT_REPORT_HTML,
    OUTPUT_ANOMALIES,
    NUMERICAL_FEATURES,
    SEPSIS_LABEL_COLUMN,
    Z_SCORE_THRESHOLD,
    CHART_SAMPLE_SIZE,
)
from data_loader import load_csv, get_unique_patients, column_to_numpy
from data_quality import check_invalid_values, check_missing_data, check_duplicates
from feature_statistics import analyze_all_features
from anomaly_detection import find_anomalies
from correlation import correlation_analysis
from report import write_anomalies_csv, generate_report
from html_report import generate_dataset_report, generate_patient_report
from patient_input import collect_patient_data, assess_patient, print_assessment_summary


# ─────────────────────────────────────────────
# Shared: load & analyse the dataset
# ─────────────────────────────────────────────

def load_and_analyse():
    """
    Load the full dataset, run all statistical analyses, and return results.
    This is shared between both modes (Mode 2 uses it for population context).
    """
    print("\n[1/7] Loading dataset...")
    patients = load_csv(DATA_FILE)
    print(f"      Loaded {len(patients):,} observations.")

    print("\n[2/7] Finding unique patients...")
    unique_patients = get_unique_patients(patients)
    print(f"      Unique patients: {len(unique_patients):,}")

    print("\n[3/7] Converting features to NumPy arrays...")
    data = {}
    for feature in NUMERICAL_FEATURES:
        data[feature] = column_to_numpy(patients, feature)
        valid_count = int(np.sum(~np.isnan(data[feature])))
        print(f"      {feature}: {valid_count:,} valid observations")

    print("\n[4/7] Checking data quality...")
    duplicates     = check_duplicates(patients)
    invalid_values = check_invalid_values(patients, NUMERICAL_FEATURES)
    missing_data   = check_missing_data(patients, NUMERICAL_FEATURES)
    print(f"      Duplicate rows:  {duplicates:,}")
    print(f"      Invalid values:  {len(invalid_values):,}")
    total_missing = sum(missing_data.values())
    print(f"      Total missing:   {total_missing:,}")

    print("\n[5/7] Calculating statistics...")
    statistics = analyze_all_features(data)
    for feature in NUMERICAL_FEATURES:
        mean_val = statistics.get(feature, {}).get("mean", float("nan"))
        if not math.isnan(mean_val):
            print(f"      {feature}: mean={mean_val:.2f}")
        else:
            print(f"      {feature}: mean=N/A")

    print("\n[6/7] Detecting statistical anomalies (z-score threshold = {Z_SCORE_THRESHOLD})...")
    anomalies = find_anomalies(patients, data, threshold=Z_SCORE_THRESHOLD)
    print(f"      Detected {len(anomalies):,} anomalies.")

    print("\n[7/7] Calculating correlations...")
    correlations = correlation_analysis(data)
    for relationship, value in correlations.items():
        if not math.isnan(value):
            print(f"      {relationship}: {value:.3f}")
        else:
            print(f"      {relationship}: N/A")

    # Load sepsis labels for group comparison charts
    sepsis_labels = None
    try:
        raw_labels = [
            p.get(SEPSIS_LABEL_COLUMN, "").strip() for p in patients
        ]
        arr = []
        for v in raw_labels:
            try:
                arr.append(float(v))
            except (ValueError, TypeError):
                arr.append(float("nan"))
        sepsis_labels = np.array(arr, dtype=float)
    except Exception:
        pass

    return (
        patients, unique_patients, statistics,
        missing_data, duplicates, invalid_values,
        anomalies, correlations, data, sepsis_labels,
    )


# ─────────────────────────────────────────────
# Mode 1: Full Dataset Analysis
# ─────────────────────────────────────────────

def run_dataset_mode():
    print("\n" + "=" * 52)
    print("  MODE 1: FULL DATASET ANALYSIS")
    print("=" * 52)

    (patients, unique_patients, statistics,
     missing_data, duplicates, invalid_values,
     anomalies, correlations, data, sepsis_labels) = load_and_analyse()

    os.makedirs("output", exist_ok=True)

    # Legacy .txt report (kept as fallback)
    write_anomalies_csv(anomalies, OUTPUT_ANOMALIES)
    generate_report(
        OUTPUT_REPORT, patients, unique_patients,
        statistics, missing_data, duplicates,
        invalid_values, anomalies, correlations,
    )

    # HTML report (new)
    print("\n  Generating HTML report with charts...")
    generate_dataset_report(
        output_path     = OUTPUT_REPORT_HTML,
        patients        = patients,
        unique_patients = unique_patients,
        statistics      = statistics,
        missing_data    = missing_data,
        duplicates      = duplicates,
        invalid_values  = invalid_values,
        anomalies       = anomalies,
        correlations    = correlations,
        data            = data,
        sepsis_labels   = sepsis_labels,
        chart_sample_size = CHART_SAMPLE_SIZE,
    )

    print("\n" + "=" * 52)
    print("  Analysis complete!")
    print("=" * 52)
    print(f"\n  HTML Report : {OUTPUT_REPORT_HTML}")
    print(f"  Text Report : {OUTPUT_REPORT}")
    print(f"  Anomalies   : {OUTPUT_ANOMALIES}")
    print("\n  Open the HTML report in your browser for the full visualisation.")


# ─────────────────────────────────────────────
# Mode 2: Patient Input Assessment
# ─────────────────────────────────────────────

def run_patient_mode():
    print("\n" + "=" * 52)
    print("  MODE 2: PATIENT VITAL SIGN ASSESSMENT")
    print("=" * 52)
    print("""
  This mode lets you enter a patient's vital signs
  and receive a personalised assessment report.

  Reference ranges are based on WHO/AHA/NIH guidelines.
  Population context charts are drawn from the Kaggle
  sepsis dataset (40,336 ICU patients).
""")

    # Collect patient data from user
    patient    = collect_patient_data()
    assessments = assess_patient(patient)
    print_assessment_summary(patient, assessments)

    # Load dataset for population context in charts
    print("\n  Loading dataset for population comparison charts...")
    print("  (This may take a moment — vitals are compared against 1.5M observations)\n")

    (patients, _, statistics, _, _, _, _, _, data, _) = load_and_analyse()

    os.makedirs("output", exist_ok=True)

    # Build safe filename from patient name
    safe_name = "".join(
        c if c.isalnum() else "_"
        for c in patient.get("name", "patient")
    ).strip("_").lower()
    output_path = f"output/patient_report_{safe_name}.html"

    print("\n  Generating patient HTML report...")
    generate_patient_report(
        output_path   = output_path,
        patient       = patient,
        assessments   = assessments,
        statistics    = statistics,
        data          = data,
        chart_sample_size = CHART_SAMPLE_SIZE,
    )

    print("\n" + "=" * 52)
    print("  Assessment complete!")
    print("=" * 52)
    print(f"\n  Patient Report : {output_path}")
    print("\n  Open the HTML report in your browser to view the full assessment.")


# ─────────────────────────────────────────────
# Entry point — CLI menu
# ─────────────────────────────────────────────

def main():
    print("=" * 52)
    print("      HOSPITAL PATIENT ANALYZER  v2")
    print("=" * 52)
    print("""
  Select a mode:

    [1]  Analyze Dataset
         Full statistical analysis of the Kaggle sepsis dataset.
         Generates an interactive HTML report with charts.

    [2]  Patient Assessment
         Enter a patient's vital signs and receive a
         personalised traffic-light assessment report.

    [0]  Exit
""")

    while True:
        choice = input("  Enter your choice [0/1/2]: ").strip()
        if choice == "1":
            run_dataset_mode()
            break
        elif choice == "2":
            run_patient_mode()
            break
        elif choice == "0":
            print("\n  Exiting. Goodbye!")
            break
        else:
            print("  Invalid choice. Please enter 0, 1, or 2.")


if __name__ == "__main__":
    main()
