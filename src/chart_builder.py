# src/chart_builder.py
# Builds Plotly figure objects for embedding into the HTML report.

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

COLOR_NORMAL   = "#3fb950"
COLOR_BORDER   = "#e3b341"
COLOR_ABNORMAL = "#f85149"
COLOR_BAR_MAIN = "#58a6ff"
COLOR_BAR_SEC  = "#bc8cff"
COLOR_BG       = "#0d1117"
COLOR_SURFACE  = "#161b22"
COLOR_GRID     = "#21262d"
COLOR_TEXT     = "#c9d1d9"

BASE_LAYOUT = dict(
    paper_bgcolor = COLOR_BG,
    plot_bgcolor  = COLOR_SURFACE,
    font          = dict(color=COLOR_TEXT, family="Inter, system-ui, sans-serif", size=12),
    margin        = dict(l=40, r=20, t=50, b=40),
    xaxis         = dict(gridcolor=COLOR_GRID, zerolinecolor=COLOR_GRID),
    yaxis         = dict(gridcolor=COLOR_GRID, zerolinecolor=COLOR_GRID),
)


def _layout(fig, title):
    layout = dict(BASE_LAYOUT)
    layout["title"] = dict(text=title, font=dict(size=15, color=COLOR_TEXT), x=0.05)
    fig.update_layout(**layout)
    return fig


def build_histogram(feature, values, stats, ref=None, patient_value=None):
    valid = values[~np.isnan(values)]
    if len(valid) == 0:
        return None
    name = ref.get("name", feature) if ref else feature
    unit = ref.get("unit", "")      if ref else ""

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x             = valid,
        nbinsx        = 60,
        name          = name,
        marker_color  = COLOR_BAR_MAIN,
        opacity       = 0.80,
        hovertemplate = f"%{{x:.1f}} {unit}<br>Count: %{{y}}<extra></extra>",
    ))

    if ref:
        min_n = ref.get("min_normal")
        max_n = ref.get("max_normal")
        if min_n is not None and max_n is not None:
            fig.add_vrect(
                x0=min_n, x1=max_n,
                fillcolor=COLOR_NORMAL, opacity=0.12, layer="below", line_width=0,
                annotation_text="Normal range",
                annotation_position="top left",
                annotation_font_color=COLOR_NORMAL,
                annotation_font_size=10,
            )

    mean_val = stats.get("mean") if stats else None
    if mean_val is not None and not np.isnan(mean_val):
        fig.add_vline(
            x=mean_val, line_color=COLOR_BORDER, line_dash="dash", line_width=1.5,
            annotation_text=f"Mean {mean_val:.1f}",
            annotation_font_color=COLOR_BORDER,
            annotation_font_size=10,
            annotation_position="top right",
        )

    if patient_value is not None:
        status_color = COLOR_ABNORMAL
        if ref:
            min_n = ref.get("min_normal", 0)
            max_n = ref.get("max_normal", 9999)
            lo    = ref.get("low_threshold", 0)
            hi    = ref.get("high_threshold", 9999)
            if min_n <= patient_value <= max_n:
                status_color = COLOR_NORMAL
            elif lo <= patient_value < min_n or max_n < patient_value <= hi:
                status_color = COLOR_BORDER
        fig.add_vline(
            x=patient_value, line_color=status_color, line_dash="solid", line_width=2.5,
            annotation_text=f"Patient: {patient_value:.1f}",
            annotation_font_color=status_color,
            annotation_font_size=11,
            annotation_position="top left",
        )

    _layout(fig, f"Distribution of {name} ({unit})")
    fig.update_xaxes(title_text=f"{name} ({unit})")
    fig.update_yaxes(title_text="Number of Observations")
    return fig


def build_correlation_heatmap(correlations):
    if not correlations:
        return None
    pairs  = [k.split(" vs ") for k in correlations.keys()]
    labels = sorted(set(f for pair in pairs for f in pair))
    n      = len(labels)
    idx    = {label: i for i, label in enumerate(labels)}
    matrix = np.full((n, n), np.nan)
    for k, v in correlations.items():
        parts = k.split(" vs ")
        if len(parts) == 2 and not np.isnan(v):
            a, b = parts
            if a in idx and b in idx:
                matrix[idx[a]][idx[b]] = v
                matrix[idx[b]][idx[a]] = v
    np.fill_diagonal(matrix, 1.0)
    text_matrix = [[f"{val:.2f}" if not np.isnan(val) else "N/A" for val in row] for row in matrix]

    fig = go.Figure(go.Heatmap(
        z=matrix, x=labels, y=labels,
        text=text_matrix, texttemplate="%{text}",
        colorscale="RdBu", zmid=0, zmin=-1, zmax=1,
        colorbar=dict(title="Pearson r", tickfont=dict(color=COLOR_TEXT)),
        hovertemplate="%{y} vs %{x}<br>r = %{z:.3f}<extra></extra>",
    ))
    _layout(fig, "Correlation Between Vital Signs")
    fig.update_xaxes(title_text="", tickangle=-30)
    fig.update_yaxes(title_text="")
    return fig


def build_missing_data_chart(missing_data, total_rows):
    if not missing_data or total_rows == 0:
        return None
    features    = list(missing_data.keys())
    pct_missing = [missing_data[f] / total_rows * 100 for f in features]
    pct_present = [100 - p for p in pct_missing]
    colors_m    = [COLOR_ABNORMAL if p > 50 else COLOR_BORDER if p > 20 else COLOR_BAR_MAIN
                   for p in pct_missing]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Present", x=pct_present, y=features, orientation="h",
        marker_color=COLOR_NORMAL, opacity=0.7,
        hovertemplate="%{y}: %{x:.1f}% present<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Missing", x=pct_missing, y=features, orientation="h",
        marker_color=colors_m, opacity=0.85,
        hovertemplate="%{y}: %{x:.1f}% missing<extra></extra>",
    ))
    _layout(fig, "Data Completeness by Feature")
    fig.update_layout(barmode="stack")
    fig.update_xaxes(title_text="Percentage (%)", range=[0, 100])
    fig.update_yaxes(title_text="")
    return fig


def build_anomaly_bar_chart(anomaly_counts):
    if not anomaly_counts:
        return None
    features = list(anomaly_counts.keys())
    counts   = list(anomaly_counts.values())
    colors   = [COLOR_ABNORMAL if c > 50000 else COLOR_BORDER if c > 10000 else COLOR_BAR_MAIN
                for c in counts]
    fig = go.Figure(go.Bar(
        x=features, y=counts, marker_color=colors,
        hovertemplate="%{x}: %{y:,} anomalies<extra></extra>",
    ))
    _layout(fig, "Statistical Anomalies by Feature (|Z-score| > 2)")
    fig.update_xaxes(title_text="Feature")
    fig.update_yaxes(title_text="Anomaly Count")
    return fig


def build_sepsis_comparison(data, sepsis_labels):
    vitals = [k for k in data if k != "Age"]
    if not vitals or sepsis_labels is None:
        return None
    valid_mask = ~np.isnan(sepsis_labels)
    sep_mask   = valid_mask & (sepsis_labels == 1)
    non_mask   = valid_mask & (sepsis_labels == 0)
    if sep_mask.sum() == 0 or non_mask.sum() == 0:
        return None

    n_cols = 2
    n_rows = (len(vitals) + 1) // 2
    fig = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=vitals)

    for i, feature in enumerate(vitals):
        row  = i // 2 + 1
        col  = i % 2 + 1
        vals = data[feature]
        sep_vals = vals[sep_mask & ~np.isnan(vals)]
        non_vals = vals[non_mask & ~np.isnan(vals)]
        fig.add_trace(go.Box(
            y=non_vals[:5000], name="No Sepsis",
            marker_color=COLOR_NORMAL, boxmean=True,
            legendgroup="nosep", showlegend=(i == 0),
        ), row=row, col=col)
        fig.add_trace(go.Box(
            y=sep_vals[:5000], name="Sepsis",
            marker_color=COLOR_ABNORMAL, boxmean=True,
            legendgroup="sep", showlegend=(i == 0),
        ), row=row, col=col)

    fig.update_layout(
        **BASE_LAYOUT,
        title=dict(text="Vital Signs: Sepsis vs Non-Sepsis Patients",
                   font=dict(size=15, color=COLOR_TEXT), x=0.05),
        height=250 * n_rows,
    )
    fig.update_annotations(font_color=COLOR_TEXT)
    return fig


def build_gender_breakdown(data, patients, features):
    male_vals   = {f: [] for f in features}
    female_vals = {f: [] for f in features}
    for i, p in enumerate(patients):
        g = str(p.get("Gender", "")).strip().upper()
        for feature in features:
            vals_arr = data.get(feature)
            if vals_arr is None or i >= len(vals_arr):
                continue
            v = vals_arr[i]
            if np.isnan(v):
                continue
            if g == "M":
                male_vals[feature].append(v)
            elif g == "F":
                female_vals[feature].append(v)
    male_means   = [np.mean(male_vals[f])   if male_vals[f]   else np.nan for f in features]
    female_means = [np.mean(female_vals[f]) if female_vals[f] else np.nan for f in features]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Male", x=features, y=male_means, marker_color=COLOR_BAR_MAIN,
        hovertemplate="%{x} (Male): %{y:.2f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Female", x=features, y=female_means, marker_color=COLOR_BAR_SEC,
        hovertemplate="%{x} (Female): %{y:.2f}<extra></extra>",
    ))
    _layout(fig, "Mean Vital Signs by Gender")
    fig.update_layout(barmode="group")
    fig.update_xaxes(title_text="Feature")
    fig.update_yaxes(title_text="Mean Value")
    return fig


def fig_to_html(fig):
    if fig is None:
        return "<p style='color:#8b949e;font-style:italic;'>Chart not available (insufficient data).</p>"
    import plotly.io as pio
    return pio.to_html(
        fig,
        full_html        = False,
        include_plotlyjs = False,
        config           = {"responsive": True, "displayModeBar": False},
    )
