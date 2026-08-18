# src/anomaly_detection.py
import numpy as np

def calculate_z_scores(values):
    z_scores = np.full(values.shape, np.nan)
    valid_mask = ~np.isnan(values)
    valid_values = values[valid_mask]
    
    if len(valid_values) == 0:
        return z_scores

    mean = np.mean(valid_values)
    std = np.std(valid_values)

    if std == 0:
        return z_scores

    z_scores[valid_mask] = (
        (valid_values - mean) / std
    )
    return z_scores

def find_anomalies(patients, data, threshold=2):
    anomalies = []
    for feature, values in data.items():
        z_scores = calculate_z_scores(values)
        for index, z_score in enumerate(z_scores):
            if np.isnan(z_score):
                continue
            if abs(z_score) > threshold:
                anomalies.append({
                    "patient_id": patients[index].get("Patient_ID"),
                    "hour": patients[index].get("Hour"),
                    "feature": feature,
                    "value": values[index],
                    "z_score": z_score
                })
    return anomalies
