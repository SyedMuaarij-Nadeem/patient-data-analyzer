# src/feature_statistics.py
import numpy as np

def calculate_statistics(values):
    valid_values = values[~np.isnan(values)]
    if len(valid_values) == 0:
        return {
            "count":   0,
            "mean":    np.nan,
            "median":  np.nan,
            "minimum": np.nan,
            "maximum": np.nan,
            "std":     np.nan,
            "p25":     np.nan,
            "p75":     np.nan,
        }
    return {
        "count":   len(valid_values),
        "mean":    float(np.mean(valid_values)),
        "median":  float(np.median(valid_values)),
        "minimum": float(np.min(valid_values)),
        "maximum": float(np.max(valid_values)),
        "std":     float(np.std(valid_values)),
        "p25":     float(np.percentile(valid_values, 25)),
        "p75":     float(np.percentile(valid_values, 75)),
    }

def analyze_all_features(data):
    results = {}
    for feature, values in data.items():
        results[feature] = calculate_statistics(values)
    return results

def compute_patient_percentile(patient_value: float, all_values: np.ndarray) -> float | None:
    """
    Return the percentile rank (0-100) of patient_value within all_values.
    Returns None if patient_value is None or array has no valid data.
    """
    if patient_value is None:
        return None
    valid = all_values[~np.isnan(all_values)]
    if len(valid) == 0:
        return None
    return float(np.mean(valid <= patient_value) * 100)
