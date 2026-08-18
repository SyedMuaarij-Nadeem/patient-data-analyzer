# src/data_quality.py

def check_invalid_values(patients, features):
    """
    Check for non-numeric and out-of-range values in the specified features.
    """
    invalid = []
    for patient in patients:
        for feature in features:
            value = patient.get(feature, "")
            if value is None:
                value = ""
            value = str(value).strip()
            
            if value == "":
                continue

            try:
                number = float(value)
            except ValueError:
                invalid.append({
                    "patient_id": patient.get("Patient_ID"),
                    "hour": patient.get("Hour"),
                    "feature": feature,
                    "value": value,
                    "reason": "Non-numeric value"
                })
                continue

            # Basic impossible-value checks
            if feature == "Age" and number < 0:
                invalid.append({
                    "patient_id": patient.get("Patient_ID"),
                    "hour": patient.get("Hour"),
                    "feature": feature,
                    "value": number,
                    "reason": "Negative age"
                })

            elif feature == "O2Sat" and (number < 0 or number > 100):
                invalid.append({
                    "patient_id": patient.get("Patient_ID"),
                    "hour": patient.get("Hour"),
                    "feature": feature,
                    "value": number,
                    "reason": "Outside 0-100 range"
                })

            elif feature in [
                "HR",
                "SBP",
                "MAP",
                "DBP",
                "Resp",
                "Glucose"
            ] and number < 0:
                invalid.append({
                    "patient_id": patient.get("Patient_ID"),
                    "hour": patient.get("Hour"),
                    "feature": feature,
                    "value": number,
                    "reason": "Negative value"
                })

    return invalid

def check_missing_data(patients, features):
    """
    Count missing values for each feature.
    """
    missing_counts = {feature: 0 for feature in features}
    for patient in patients:
        for feature in features:
            value = patient.get(feature, "")
            if value is None or str(value).strip() == "":
                missing_counts[feature] += 1
    return missing_counts

def check_duplicates(patients):
    """
    Check for duplicate patient-hour combinations.
    """
    seen = set()
    duplicates = 0
    for patient in patients:
        pid = patient.get("Patient_ID", "").strip()
        hour = patient.get("Hour", "").strip()
        key = (pid, hour)
        if key in seen:
            duplicates += 1
        else:
            seen.add(key)
    return duplicates
