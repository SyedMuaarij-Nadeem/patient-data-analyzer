# src/main.py
import os
import math
from config import (
    DATA_FILE,
    OUTPUT_REPORT,
    OUTPUT_ANOMALIES,
    NUMERICAL_FEATURES,
    Z_SCORE_THRESHOLD
)
from data_loader import load_csv, get_unique_patients, column_to_numpy
from data_quality import check_invalid_values, check_missing_data, check_duplicates
from feature_statistics import analyze_all_features
from anomaly_detection import find_anomalies
from correlation import correlation_analysis
from report import write_anomalies_csv, generate_report

def main():
    print("==================================================")
    print("      HOSPITAL PATIENT DATA ANALYZER")
    print("==================================================")

    # 1. Loading
    print("\n[1/7] Loading dataset...")
    patients = load_csv(DATA_FILE)
    print(f"Loaded {len(patients)} observations.")

    # 2. Unique patients
    print("\n[2/7] Finding unique patients...")
    unique_patients = get_unique_patients(patients)
    print(f"Unique patients: {len(unique_patients)}")

    # 3. Converting to NumPy
    print("\n[3/7] Converting features to NumPy...")
    data = {}
    for feature in NUMERICAL_FEATURES:
        data[feature] = column_to_numpy(patients, feature)
        # Count non-nan values
        import math
        valid_count = sum(1 for v in data[feature] if not math.isnan(v))
        print(f"{feature}: {valid_count} observations")

    # 4. Data quality
    print("\n[4/7] Checking data quality...")
    duplicates = check_duplicates(patients)
    invalid_values = check_invalid_values(patients, NUMERICAL_FEATURES)
    missing_data = check_missing_data(patients, NUMERICAL_FEATURES)
    print(f"Duplicate observations: {duplicates}")
    print(f"Invalid values: {len(invalid_values)}")

    # 5. Statistics
    print("\n[5/7] Calculating statistics...")
    statistics = analyze_all_features(data)
    for feature in NUMERICAL_FEATURES:
        mean_val = statistics.get(feature, {}).get("mean", float('nan'))
        if not math.isnan(mean_val):
            print(f"{feature}: mean={mean_val:.2f}")
        else:
            print(f"{feature}: mean=N/A")

    # 6. Anomalies
    print("\n[6/7] Detecting statistical anomalies...")
    anomalies = find_anomalies(patients, data, threshold=Z_SCORE_THRESHOLD)
    print(f"Detected {len(anomalies)} anomalies.")

    # 7. Correlation
    print("\n[7/7] Calculating correlations...")
    correlations = correlation_analysis(data)
    for relationship, value in correlations.items():
        if not math.isnan(value):
            print(f"{relationship}: {value:.3f}")
        else:
            print(f"{relationship}: N/A")

    # Output directory
    os.makedirs("output", exist_ok=True)

    # Write anomalies CSV
    write_anomalies_csv(anomalies, OUTPUT_ANOMALIES)

    # Generate final report
    generate_report(
        OUTPUT_REPORT,
        patients,
        unique_patients,
        statistics,
        missing_data,
        duplicates,
        invalid_values,
        anomalies,
        correlations
    )

    print("\n========================================")
    print("Analysis complete!")
    print("========================================")
    print(f"\nReport: {OUTPUT_REPORT}")
    print(f"Anomalies: {OUTPUT_ANOMALIES}")

if __name__ == "__main__":
    main()
