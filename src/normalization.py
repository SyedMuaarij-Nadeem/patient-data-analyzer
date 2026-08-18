# src/normalization.py
import numpy as np

def min_max_normalize(values):
    normalized = np.full(values.shape, np.nan)
    valid_mask = ~np.isnan(values)
    valid_values = values[valid_mask]
    
    if len(valid_values) == 0:
        return normalized

    minimum = np.min(valid_values)
    maximum = np.max(valid_values)

    if maximum == minimum:
        normalized[valid_mask] = 0
        return normalized

    normalized[valid_mask] = (
        (valid_values - minimum)
        / (maximum - minimum)
    )
    return normalized
