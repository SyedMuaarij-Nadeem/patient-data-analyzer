# 🏥 Hospital Patient Data Analyzer

A powerful, interactive Python-based data analysis and assessment pipeline designed to process large-scale clinical patient datasets and evaluate individual vital signs against medical reference guidelines.

---

## 🌟 Key Features

The project operates in **two distinct modes** designed to cater to both clinical researchers and guardians/patients:

### 1. Dual-Mode Interface
*   **Mode 1: Full Dataset Analysis** — Ingests a dataset of **1.55 Million observations** across **40,336 unique ICU patients**. It evaluates data quality, calculates summary statistics (mean, median, standard deviation, and percentiles), detects statistical anomalies via Z-scores, and calculates Pearson correlation matrices.
*   **Mode 2: Patient Assessment** — Collects a patient's vital signs interactively. It classifies each vital into one of 5 zones (Normal, Low, High, Critically Low, Critically High) using clinical reference ranges.

### 2. Multi-Audience Reporting
Generates rich, self-contained **HTML dashboards** using a clean, dark-mode design with dedicated tabs:
*   **🩺 Technical Tab (Clinicians):** Zoomable/hoverable Plotly scatter charts, group comparison box plots (Sepsis vs. Non-Sepsis), a correlation matrix heatmap, data coverage indicators, and statistical summaries.
*   **👪 Plain English Tab (Guardians/Patients):** Translates medical jargon into plain English, presents vital status using a traffic-light indicator system (🟢/🟡/🔴), and maps the patient's individual vitals onto the broader population distribution curve.

### 3. Rigorous Clinical Reference Guidelines
Vitals are assessed against established guidelines sourced from **WHO, AHA, and NIH**:
*   **Heart Rate (HR):** Normal sinus rhythm (60–100 bpm)
*   **Oxygen Saturation (SpO₂):** Normal healthy range (95–100%)
*   **Body Temperature:** Typical core range (36.1–37.2 °C)
*   **Systolic Blood Pressure (SBP):** Typical range (90–120 mmHg)
*   **Diastolic Blood Pressure (DBP):** Typical range (60–80 mmHg)
*   **Mean Arterial Pressure (MAP):** Normal perfusion range (70–100 mmHg); flags critical perfusion risks below 65 mmHg.
*   **Respiratory Rate (Resp):** Normal adult range (12–20 breaths/min)
*   **Blood Glucose:** Fasting/normal range (70–140 mg/dL)

---

## 📁 Project Structure

```text
hospital-patient-analyzer/
│
├── output/                   # Directory for generated reports and data exports
│   ├── analysis_report.html  # Interactive v2 dataset dashboard (Mode 1)
│   ├── analysis_report.txt   # Legacy text-based report fallback
│   ├── anomalies.csv         # Detailed spreadsheet of flagged anomalies
│   └── patient_report_*.html # Personalized vital sign assessment report (Mode 2)
│
├── src/                      # Source code directory
│   ├── main.py               # Main CLI execution entry point and menu
│   ├── config.py             # Pipeline configurations, paths, and sample sizes
│   ├── reference_ranges.py   # Clinical reference ranges and status calculation logic
│   ├── patient_input.py      # Interactive CLI user prompt and validation wizard
│   ├── chart_builder.py      # Plotly interactive visualization engine
│   ├── html_report.py        # Single-file HTML generation templates and handlers
│   ├── data_loader.py        # Ingests CSV data and converts to NumPy arrays
│   ├── data_quality.py       # Validates records for missing, invalid, or duplicate fields
│   ├── feature_statistics.py # Calculates descriptive stats and percentile positions
│   ├── anomaly_detection.py  # Flags data outliers using configurable Z-score rules
│   └── correlation.py        # Computes Pearson correlation coefficients
│
├── requirements.txt          # Python dependencies (numpy, kagglehub, plotly)
└── README.md                 # Project documentation
```

---

## 🛠️ Setup and Installation

### Prerequisites
*   Python 3.10 or higher.
*   An active internet connection on the first run (to fetch the dataset from Kaggle).

### Step 1: Clone and Navigate
Navigate to the root directory of the project in your terminal:
```bash
cd hospital-patient-analyzer
```

### Step 2: Set Up Virtual Environment (Recommended)
```bash
python -m venv .venv
```
Activate the environment:
*   **Windows (PowerShell):**
    ```powershell
    .venv\Scripts\Activate.ps1
    ```
*   **Windows (CMD):**
    ```cmd
    .venv\Scripts\activate.bat
    ```
*   **macOS / Linux:**
    ```bash
    source .venv/bin/activate
    ```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run the Program

Start the interactive CLI menu:
```bash
python src/main.py
```

You will be presented with a menu:
```text
====================================================
      HOSPITAL PATIENT ANALYZER  v2
====================================================

  Select a mode:

    [1]  Analyze Dataset
         Full statistical analysis of the Kaggle sepsis dataset.
         Generates an interactive HTML report with charts.

    [2]  Patient Assessment
         Enter a patient's vital signs and receive a
         personalised traffic-light assessment report.

    [0]  Exit

  Enter your choice [0/1/2]:
```

### Mode 1: Analyze Dataset
1.  Enter `1` and press **Enter**.
2.  The program will automatically download the Kaggle sepsis prediction dataset (if not already cached locally).
3.  It will run the data ingestion, quality validation, statistics computation, correlation analysis, and anomaly detection.
4.  Once complete, it saves and outputs the file paths for the legacy text report, the CSV anomalies list, and the primary interactive HTML report (`output/analysis_report.html`).

### Mode 2: Patient Assessment
1.  Enter `2` and press **Enter**.
2.  Fill in the patient's demographics: **Name**, **Age**, and **Gender** (M/F/Other).
3.  Enter the patient's vital signs (e.g., HR, SpO₂, SBP, DBP). 
    *   *Note:* Critical parameters like SBP/DBP are required, while non-critical values like Glucose or MAP are optional (MAP will be automatically derived from SBP/DBP if omitted).
4.  The system will print a CLI summary and load the population statistics.
5.  It will output a personalized HTML report: `output/patient_report_<patientname>.html`.

---

## 📊 Visualizations & Reports

All charts in the HTML reports are powered by **Plotly** and offer interactive hover tooltips, click-to-zoom controls, and target overlays:
*   **Histograms:** Visualizes patient vital signs against the general distribution curve, with the normal clinical range shaded in soft green, and the specific patient's value marked as a solid vertical line.
*   **Heatmaps:** Color-coded Pearson correlation coefficients indicating positive or negative relationships.
*   **Group Comparison Box Plots:** Shows the distribution of vitals compared between patients flagged with sepsis vs. non-sepsis.

---

## ⚠️ Medical Disclaimer

This program is a statistical analysis tool intended **only for educational, informational, and research purposes**. 
*   It **does not** constitute medical advice, diagnosis, or treatment.
*   Statistical anomalies (|Z-score| > 2) represent statistical deviations in a high-acuity ICU population, **not** active diseases.
*   Always consult a qualified healthcare professional regarding any clinical concerns.
