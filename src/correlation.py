# src/correlation.py
import numpy as np

def calculate_correlation(x, y):
    valid_mask = (
        ~np.isnan(x)
        & ~np.isnan(y)
    )
    x_valid = x[valid_mask]
    y_valid = y[valid_mask]

    if len(x_valid) < 2:
        return np.nan

    correlation_matrix = np.corrcoef(
        x_valid,
        y_valid
    )
    return correlation_matrix[0, 1]

def correlation_analysis(data):
    relationships = [
        ("Age", "Glucose"),
        ("Age", "SBP"),
        ("HR", "Temp"),
        ("Glucose", "SBP"),
        ("HR", "O2Sat")
    ]
    results = {}
    for feature_a, feature_b in relationships:
        if feature_a not in data or feature_b not in data:
            continue
        correlation = calculate_correlation(
            data[feature_a],
            data[feature_b]
        )
        results[
            f"{feature_a} vs {feature_b}"
        ] = correlation
    return results
