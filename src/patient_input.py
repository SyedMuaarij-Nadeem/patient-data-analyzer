# src/patient_input.py
# Patient Input Mode — collects vital sign values from the user via the CLI,
# validates each entry, and returns an assessment dict with traffic-light status.

from reference_ranges import REFERENCE_RANGES, get_vital_status

VITAL_FIELDS = [
    {"key": "HR",      "optional": False},
    {"key": "O2Sat",   "optional": False},
    {"key": "Temp",    "optional": False},
    {"key": "SBP",     "optional": False},
    {"key": "DBP",     "optional": False},
    {"key": "MAP",     "optional": True},
    {"key": "Resp",    "optional": False},
    {"key": "Glucose", "optional": True},
]


def _prompt_str(label, hint):
    while True:
        val = input(f"  {label} ({hint}): ").strip()
        if val:
            return val
        print("    [!] This field cannot be empty. Please try again.")


def _prompt_choice(label, choices):
    choices_display = " / ".join(choices)
    while True:
        val = input(f"  {label} [{choices_display}]: ").strip()
        for c in choices:
            if val.lower() == c.lower():
                return c
        print(f"    [!] Please enter one of: {choices_display}")


def _prompt_float(label, unit, hint, min_val=None, max_val=None, optional=False):
    unit_str = f" {unit}" if unit else ""
    opt_str  = " (press Enter to skip)" if optional else ""
    while True:
        raw = input(f"  {label}{unit_str}{opt_str}: ").strip()
        if raw == "" and optional:
            return None
        if raw == "" and not optional:
            print("    [!] This field is required. Please enter a value.")
            continue
        try:
            val = float(raw)
        except ValueError:
            print("    [!] Please enter a number (e.g. 75.5)")
            continue
        if min_val is not None and val < min_val:
            print(f"    [!] Value must be at least {min_val}.")
            continue
        if max_val is not None and val > max_val:
            print(f"    [!] Value must be at most {max_val}.")
            continue
        return val


def collect_patient_data():
    print()
    print("  +----------------------------------------------+")
    print("  |         PATIENT VITAL SIGN ASSESSMENT        |")
    print("  +----------------------------------------------+")
    print()
    print("  Fill in the patient details below.")
    print("  For optional fields, press Enter to skip.")
    print()

    patient = {}

    print("  --- Patient Demographics ---")
    patient["name"]   = _prompt_str("Patient Name", "Full name for report header")
    patient["age"]    = _prompt_float("Age", "years", "e.g. 45", min_val=0, max_val=130)
    patient["gender"] = _prompt_choice("Gender", ["M", "F", "Other"])

    print()
    print("  --- Vital Signs ---")
    print("  (Normal ranges shown in parentheses for reference)")
    print()

    for vf in VITAL_FIELDS:
        feature  = vf["key"]
        optional = vf["optional"]
        ref      = REFERENCE_RANGES.get(feature, {})
        name     = ref.get("name", feature)
        unit     = ref.get("unit", "")
        min_n    = ref.get("min_normal", "")
        max_n    = ref.get("max_normal", "")
        hint_str = f"normal: {min_n}-{max_n} {unit}" if min_n != "" else ""

        value = _prompt_float(
            label    = name,
            unit     = unit,
            hint     = hint_str,
            optional = optional,
        )
        patient[feature] = value

    # Derive MAP if missing but SBP/DBP are available
    if patient.get("MAP") is None:
        sbp = patient.get("SBP")
        dbp = patient.get("DBP")
        if sbp is not None and dbp is not None:
            patient["MAP"] = round(dbp + (sbp - dbp) / 3, 1)
            print(f"  [i] MAP derived from SBP/DBP: {patient['MAP']} mmHg")

    return patient


def assess_patient(patient):
    assessments = []
    vital_keys  = [vf["key"] for vf in VITAL_FIELDS]
    for feature in vital_keys:
        value = patient.get(feature)
        ref   = REFERENCE_RANGES.get(feature, {})
        if value is None:
            assessments.append({
                "feature":     feature,
                "value":       None,
                "ref":         ref,
                "status_info": {
                    "status":  "skipped",
                    "label":   "Not Provided",
                    "color":   "#8b949e",
                    "emoji":   "\u26aa",
                    "message": "This measurement was not provided.",
                },
            })
        else:
            assessments.append({
                "feature":     feature,
                "value":       value,
                "ref":         ref,
                "status_info": get_vital_status(feature, value),
            })
    return assessments


def print_assessment_summary(patient, assessments):
    print()
    print("  ==============================================")
    print(f"  Assessment Summary for: {patient['name']}")
    print("  ==============================================")
    for a in assessments:
        ref  = a["ref"]
        name = ref.get("name", a["feature"])
        unit = ref.get("unit", "")
        si   = a["status_info"]
        if a["value"] is None:
            print(f"  {si['emoji']}  {name:<35}  SKIPPED")
        else:
            print(f"  {si['emoji']}  {name:<35}  {a['value']} {unit}  [{si['label']}]")
    print()
