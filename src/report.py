# src/report.py
import csv
import math

def write_anomalies_csv(anomalies, output_path):
    if not anomalies:
        return
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["patient_id", "hour", "feature", "value", "z_score"])
        writer.writeheader()
        for anomaly in anomalies:
            writer.writerow(anomaly)

def generate_report(
    output_path,
    patients,
    unique_patients,
    statistics,
    missing_data,
    duplicates,
    invalid_values,
    anomalies,
    correlations
):
    with open(output_path, "w", encoding="utf-8") as report:
        # Header
        report.write("========================================\n")
        report.write("DATASET SUMMARY\n")
        report.write("----------------------------------------\n")
        report.write(f"Total observations: {len(patients)}\n")
        report.write(f"Unique patients: {len(unique_patients)}\n\n")

        # Data Quality
        report.write("DATA QUALITY\n")
        report.write("----------------------------------------\n")
        total_missing = sum(missing_data.values()) if missing_data else 0
        report.write(f"Total missing values: {total_missing}\n")
        report.write(f"Duplicate observations: {duplicates}\n")
        report.write(f"Invalid values: {len(invalid_values)}\n\n")

        report.write("Missing values by feature:\n")
        for feature, count in missing_data.items():
            report.write(f"{feature:<15} {count}\n")
        report.write("\n")

        # Statistics
        report.write("FEATURE STATISTICS\n")
        report.write("----------------------------------------\n\n")
        for feature, stats in statistics.items():
            report.write(f"{feature}\n")
            report.write(f"  Count:    {stats['count']}\n")
            
            if stats['count'] > 0:
                report.write(f"  Mean:     {stats['mean']:.4f}\n")
                report.write(f"  Median:   {stats['median']:.4f}\n")
                report.write(f"  Minimum:  {stats['minimum']:.4f}\n")
                report.write(f"  Maximum:  {stats['maximum']:.4f}\n")
                report.write(f"  Std Dev:  {stats['std']:.4f}\n\n")
            else:
                report.write("  No valid data\n\n")

        if "Glucose" in statistics and statistics["Glucose"]["count"] > 0:
            stats = statistics["Glucose"]
            report.write("GLUCOSE ANALYSIS\n")
            report.write("----------------------------------------\n")
            report.write(f"Measurements: {stats['count']}\n")
            report.write(f"Mean:         {stats['mean']:.2f}\n")
            report.write(f"Median:       {stats['median']:.2f}\n")
            report.write(f"Minimum:      {stats['minimum']:.2f}\n")
            report.write(f"Maximum:      {stats['maximum']:.2f}\n")
            report.write(f"Std Dev:      {stats['std']:.2f}\n")
            report.write("\nNote: Glucose values are analyzed statistically. No medical diagnosis is made.\n\n")

        # Anomalies
        report.write("STATISTICAL ANOMALIES\n")
        report.write("----------------------------------------\n")
        report.write(f"Total anomalies: {len(anomalies)}\n\n")
        
        # Write up to 20 anomalies so we don't blow up the report
        for anomaly in anomalies[:20]:
            report.write(
                f"Patient {anomaly['patient_id']} | "
                f"Hour {anomaly['hour']} | "
                f"{anomaly['feature']} | "
                f"Value: {anomaly['value']:.2f} | "
                f"Z-score: {anomaly['z_score']:.2f}\n"
            )
        if len(anomalies) > 20:
            report.write(f"... and {len(anomalies) - 20} more anomalies.\n")
        report.write("\n")

        # Correlations
        report.write("CORRELATION ANALYSIS\n")
        report.write("----------------------------------------\n")
        for relationship, correlation in correlations.items():
            if math.isnan(correlation):
                report.write(f"{relationship}: N/A\n")
            else:
                report.write(f"{relationship}: {correlation:.3f}\n")

        report.write("\n\n")
        report.write("IMPORTANT:\n")
        report.write("A statistical anomaly means that a measurement is unusual relative to this dataset. ")
        report.write("It does not indicate a disease or diagnosis.\n")
