# src/reference_ranges.py
# Medically established reference ranges for each vital sign feature.
# Sources: WHO, AHA, NIH clinical guidelines.

REFERENCE_RANGES = {
    "HR": {
        "name":           "Heart Rate",
        "unit":           "bpm",
        "description":    (
            "The number of times your heart beats per minute. It reflects how hard "
            "your heart is working to pump blood through your body."
        ),
        "min_normal":     60,
        "max_normal":     100,
        "low_threshold":  40,
        "high_threshold": 130,
        "normal_meaning": "Your heart is beating at a healthy pace - not too fast or too slow.",
        "abnormal_high":  (
            "A high heart rate (tachycardia) could mean the heart is under stress. "
            "This may happen due to fever, dehydration, pain, anxiety, or infection."
        ),
        "abnormal_low":   (
            "A low heart rate (bradycardia) can mean the heart is beating too slowly. "
            "In athletes this is often normal, but in hospital patients it may need attention."
        ),
        "tech_notes":     "Normal sinus rhythm: 60-100 bpm. Tachycardia >100 bpm; Bradycardia <60 bpm.",
    },
    "O2Sat": {
        "name":           "Oxygen Saturation (SpO2)",
        "unit":           "%",
        "description":    (
            "The percentage of your blood haemoglobin that is carrying oxygen. "
            "Think of it as how full the blood oxygen tanks are."
        ),
        "min_normal":     95,
        "max_normal":     100,
        "low_threshold":  88,
        "high_threshold": 100,
        "normal_meaning": "Your blood is carrying a healthy amount of oxygen to your organs.",
        "abnormal_high":  "Values above 100% are not physiologically possible - likely a sensor artifact.",
        "abnormal_low":   (
            "Low oxygen saturation (hypoxaemia) means organs may not be getting enough oxygen. "
            "This needs immediate medical review."
        ),
        "tech_notes":     "SpO2 >=95% normal. 88-94% mild hypoxaemia; <88% severe - supplemental O2 indicated.",
    },
    "Temp": {
        "name":           "Body Temperature",
        "unit":           "deg C",
        "description":    (
            "Your core body temperature. The body keeps it in a narrow range "
            "to allow enzymes and organs to work correctly."
        ),
        "min_normal":     36.1,
        "max_normal":     37.2,
        "low_threshold":  35.0,
        "high_threshold": 38.3,
        "normal_meaning": "Your body temperature is within the healthy range.",
        "abnormal_high":  (
            "A high temperature (fever) usually means the body is fighting an infection or inflammation. "
            "Temperatures above 38.3 C in a hospital setting are clinically significant."
        ),
        "abnormal_low":   (
            "A low body temperature (hypothermia) can occur due to cold exposure, severe infection "
            "(sepsis), or certain medical conditions. It requires prompt attention."
        ),
        "tech_notes":     "Normal: 36.1-37.2 C. Fever: >=38.3 C. Hypothermia: <=35.0 C. Hyperthermia (>=40 C) is a medical emergency.",
    },
    "SBP": {
        "name":           "Systolic Blood Pressure",
        "unit":           "mmHg",
        "description":    (
            "The pressure in your arteries when your heart beats and pushes blood out. "
            "It is the top number in a blood pressure reading like 120/80."
        ),
        "min_normal":     90,
        "max_normal":     120,
        "low_threshold":  70,
        "high_threshold": 140,
        "normal_meaning": "The pressure your heart generates when it pumps is within the healthy range.",
        "abnormal_high":  (
            "High systolic pressure (hypertension) over time can strain the heart and blood vessels. "
            "In acute settings, very high SBP may indicate hypertensive crisis."
        ),
        "abnormal_low":   (
            "Low systolic pressure (hypotension) can mean the body is not getting enough blood flow. "
            "This is a serious sign in hospitalised patients and may indicate shock."
        ),
        "tech_notes":     "Normal: 90-120 mmHg. Hypertension Stage 1: 130-139; Stage 2: >=140. Hypotension: <90 mmHg. Shock threshold typically <70 mmHg.",
    },
    "MAP": {
        "name":           "Mean Arterial Pressure",
        "unit":           "mmHg",
        "description":    (
            "An average blood pressure value that estimates how well blood is being "
            "delivered to organs throughout the entire cardiac cycle."
        ),
        "min_normal":     70,
        "max_normal":     100,
        "low_threshold":  60,
        "high_threshold": 110,
        "normal_meaning": "Blood is being delivered to your organs at a healthy pressure throughout each heartbeat.",
        "abnormal_high":  (
            "A persistently high MAP may signal uncontrolled hypertension, "
            "increasing risk of stroke or heart damage."
        ),
        "abnormal_low":   (
            "A MAP below 65 mmHg is a critical threshold in intensive care - it suggests "
            "organs (especially kidneys and brain) may not be receiving adequate blood flow."
        ),
        "tech_notes":     "MAP = DBP + 1/3*(SBP-DBP). Critical threshold: <65 mmHg (septic shock criterion). Target MAP >=65 mmHg in ICU patients.",
    },
    "DBP": {
        "name":           "Diastolic Blood Pressure",
        "unit":           "mmHg",
        "description":    (
            "The pressure in your arteries when your heart rests between beats. "
            "It is the bottom number in a blood pressure reading like 120/80."
        ),
        "min_normal":     60,
        "max_normal":     80,
        "low_threshold":  40,
        "high_threshold": 90,
        "normal_meaning": "The resting pressure in your arteries between heartbeats is within the healthy range.",
        "abnormal_high":  (
            "High diastolic pressure contributes to overall hypertension and can "
            "increase the workload on the heart over time."
        ),
        "abnormal_low":   (
            "Low diastolic pressure may mean the heart is not filling properly, "
            "which can reduce blood flow to the coronary arteries."
        ),
        "tech_notes":     "Normal: 60-80 mmHg. Hypertension: >=90 mmHg. Isolated diastolic hypotension (<60 mmHg) may indicate aortic regurgitation.",
    },
    "Resp": {
        "name":           "Respiratory Rate",
        "unit":           "breaths/min",
        "description":    (
            "How many times per minute a person breathes. It is one of the most sensitive "
            "early warning signs that a patient condition is worsening."
        ),
        "min_normal":     12,
        "max_normal":     20,
        "low_threshold":  8,
        "high_threshold": 25,
        "normal_meaning": "Your breathing rate is within the normal range for a resting adult.",
        "abnormal_high":  (
            "A high respiratory rate (tachypnoea) often means the body is working harder to get enough "
            "oxygen - it can be an early sign of infection, sepsis, or breathing problems."
        ),
        "abnormal_low":   (
            "A very low respiratory rate (bradypnoea) may indicate sedation, neurological problems, "
            "or severe metabolic disturbances. This needs prompt medical evaluation."
        ),
        "tech_notes":     "Normal adult: 12-20 br/min. Tachypnoea: >20 br/min. Bradypnoea: <12 br/min. SIRS criterion: RR >20. NEWS2 score uses RR as a key parameter.",
    },
    "Glucose": {
        "name":           "Blood Glucose",
        "unit":           "mg/dL",
        "description":    (
            "The amount of sugar (glucose) in the blood. "
            "Glucose is the main fuel for the brain and muscles."
        ),
        "min_normal":     70,
        "max_normal":     140,
        "low_threshold":  50,
        "high_threshold": 200,
        "normal_meaning": "Your blood sugar level is within the healthy range.",
        "abnormal_high":  (
            "High blood sugar (hyperglycaemia) can indicate diabetes or a stress response to illness. "
            "In critically ill patients, hyperglycaemia is associated with worse outcomes."
        ),
        "abnormal_low":   (
            "Low blood sugar (hypoglycaemia) is dangerous - the brain relies on glucose. "
            "Symptoms include confusion, shakiness, and loss of consciousness."
        ),
        "tech_notes":     "Fasting normal: 70-99 mg/dL. Post-meal: <140 mg/dL. Hyperglycaemia: >140 mg/dL. Hypoglycaemia: <70 mg/dL. ICU target: 140-180 mg/dL (ADA/AACE).",
    },
}

AGE_META = {
    "name":        "Age",
    "unit":        "years",
    "description": "The patient's age in years.",
    "tech_notes":  "Age is a demographic variable, not a vital sign. It is used as a risk modifier.",
}


def get_vital_status(feature: str, value: float) -> dict:
    # Returns status dict: status, label, color, emoji, message
    if feature not in REFERENCE_RANGES:
        return {
            "status":  "unknown",
            "label":   "No reference range available",
            "color":   "#8b949e",
            "emoji":   "\u26aa",
            "message": "No clinical reference range is available for this measurement.",
        }
    ref   = REFERENCE_RANGES[feature]
    lo    = ref["low_threshold"]
    min_n = ref["min_normal"]
    max_n = ref["max_normal"]
    hi    = ref["high_threshold"]
    if value < lo:
        return {"status": "critical_low",  "label": "Critically Low",  "color": "#f85149", "emoji": "\U0001f534", "message": ref["abnormal_low"]}
    elif value < min_n:
        return {"status": "low",           "label": "Low",             "color": "#e3b341", "emoji": "\U0001f7e1", "message": ref["abnormal_low"]}
    elif value <= max_n:
        return {"status": "normal",        "label": "Normal",          "color": "#3fb950", "emoji": "\U0001f7e2", "message": ref["normal_meaning"]}
    elif value <= hi:
        return {"status": "high",          "label": "High",            "color": "#e3b341", "emoji": "\U0001f7e1", "message": ref["abnormal_high"]}
    else:
        return {"status": "critical_high", "label": "Critically High", "color": "#f85149", "emoji": "\U0001f534", "message": ref["abnormal_high"]}
