# src/feature_statistics.py
import numpy as np

def calculate_statistics(values):
    valid_values = values[~np.isnan(values)]
    if len(valid_values) == 0:
        return {
            "count": 0,
            "mean": np.nan,
            "median": np.nan,
            "minimum": np.nan,
            "maximum": np.nan,
            "std": np.nan
        }
    return {
        "count": len(valid_values),
        "mean": float(np.mean(valid_values)),
        "median": float(np.median(valid_values)),
        "minimum": float(np.min(valid_values)),
        "maximum": float(np.max(valid_values)),
        "std": float(np.std(valid_values))
    }

def analyze_all_features(data):
    results = {}
    for feature, values in data.items():
        results[feature] = calculate_statistics(values)
    return results
