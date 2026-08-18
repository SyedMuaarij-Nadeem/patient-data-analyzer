# src/time_analysis.py
import numpy as np

def get_patient_observations(patients, patient_id):
    observations = []
    for patient in patients:
        if patient.get("Patient_ID") == patient_id:
            observations.append(patient)
    return observations

def calculate_patient_changes(patients, patient_id, feature):
    observations = get_patient_observations(
        patients,
        patient_id
    )
    values = []
    for patient in observations:
        value = patient.get(feature, "")
        if value is None:
            value = ""
        value = str(value).strip()
        
        if value == "":
            continue
        try:
            values.append(
                (
                    int(float(patient["Hour"])),
                    float(value)
                )
            )
        except (ValueError, TypeError):
            continue

    values.sort()
    if len(values) < 2:
        return None

    first_hour, first_value = values[0]
    last_hour, last_value = values[-1]

    return {
        "patient_id": patient_id,
        "feature": feature,
        "first_hour": first_hour,
        "first_value": first_value,
        "last_hour": last_hour,
        "last_value": last_value,
        "change": last_value - first_value
    }
