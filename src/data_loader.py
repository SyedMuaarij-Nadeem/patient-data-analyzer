# src/data_loader.py

import csv
import numpy as np

def load_csv(file_path):
    """
    Load CSV file and return a list of dictionaries.

    Each dictionary represents one observation.
    """
    patients = []
    with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            patients.append(row)
    return patients

def get_columns(patients):
    """Return column names."""
    if not patients:
        return []
    return list(patients[0].keys())

def get_unique_patients(patients):
    """Return unique patient IDs."""
    patient_ids = set()
    for patient in patients:
        patient_id = patient.get("Patient_ID", "").strip()
        if patient_id:
            patient_ids.add(patient_id)
    return patient_ids

def column_to_numpy(patients, column):
    """
    Convert a CSV column into a NumPy array.

    Empty/non-numeric values become NaN.
    """
    values = []
    for patient in patients:
        value = patient.get(column, "").strip() if patient.get(column) is not None else ""
        if value == "":
            values.append(np.nan)
        else:
            try:
                values.append(float(value))
            except ValueError:
                values.append(np.nan)
    return np.array(values, dtype=float)
