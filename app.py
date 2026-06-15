# app.py
# Run with: streamlit run app.py

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="BudgetTracker – Carbon Debt Explorer",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# THEME / STYLES
# ---------------------------------------------------------
st.markdown(
    """
<style>
:root {
    --bg: #05070c;
    --bg-2: #070b12;
    --panel: #0c1119;
    --panel-2: #0f1520;
    --panel-3: #121927;
    --line: rgba(255,255,255,0.08);
    --line-2: rgba(36,208,122,0.18);
    --text: #f4f7fb;
    --muted: #8f9baa;
    --green: #19d06b;
    --green-2: #11b85c;
    --red: #ff4d73;
    --blue: #4fa3ff;
    --amber: #f7b84b;
    --shadow: 0 0 0 1px rgba(255,255,255,0.02) inset;
}

html, body, [class*="css"] {
    color: var(--text);
}

[data-testid="stAppViewContainer"] {
    background:
        linear-gradient(rgba(255,255,255,0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.045) 1px, transparent 1px),
        radial-gradient(circle at 10% 20%, rgba(25,208,107,0.08), transparent 16%),
        radial-gradient(circle at 90% 12%, rgba(79,163,255,0.05), transparent 18%),
        var(--bg);
    background-size: 48px 48px, 48px 48px, auto, auto;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060910 0%, #05080d 100%);
    border-right: 1px solid var(--line);
}

.block-container {
    padding-top: 0.9rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

#MainMenu, header, footer {
    visibility: hidden;
}

h1, h2, h3, h4 {
    color: var(--text);
}

.small-muted {
    color: var(--muted);
    font-size: 0.92rem;
}

.brand-wrap {
    padding: 0.2rem 0 0.8rem 0;
}

.brand-title {
    font-size: 2rem;
    font-weight: 850;
    letter-spacing: -0.04em;
    margin-bottom: 0.18rem;
}

.brand-sub {
    color: var(--muted);
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.24em;
    margin-bottom: 0.9rem;
}

.section-title {
    font-size: 1.7rem;
    font-weight: 850;
    margin-bottom: 0.12rem;
    letter-spacing: -0.03em;
}

.section-subtitle {
    color: var(--muted);
    margin-bottom: 1rem;
}

.hero {
    background:
        linear-gradient(90deg, rgba(0,0,0,0.82) 0%, rgba(0,0,0,0.62) 46%, rgba(0,0,0,0.18) 100%),
        radial-gradient(circle at 88% 24%, rgba(25,208,107,0.18), transparent 18%),
        radial-gradient(circle at 90% 20%, rgba(255,255,255,0.06), transparent 14%),
        var(--bg-2);
    border: 1px solid var(--line);
    border-radius: 0;
    padding: 2rem 2.2rem;
    min-height: 280px;
    margin-bottom: 1.15rem;
    box-shadow: var(--shadow);
}

.badge {
    display: inline-block;
    background: rgba(25,208,107,0.16);
    color: var(--green);
    border: 1px solid rgba(25,208,107,0.28);
    padding: 0.32rem 0.7rem;
    font-weight: 800;
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    border-radius: 0;
    margin-bottom: 1rem;
    text-transform: uppercase;
}

.hero-title {
    font-size: 3.35rem;
    line-height: 0.95;
    font-weight: 850;
    letter-spacing: -0.05em;
    margin: 0 0 0.9rem 0;
    max-width: 760px;
}

.hero-text {
    font-size: 1.12rem;
    color: #d4dce6;
    max-width: 900px;
    line-height: 1.62;
    margin-bottom: 1rem;
}

.metric-card {
    background: linear-gradient(180deg, var(--panel) 0%, #0b1017 100%);
    border: 1px solid var(--line);
    padding: 1.1rem 1.15rem 0.95rem 1.15rem;
    min-height: 138px;
    border-radius: 0;
    box-shadow: var(--shadow);
}

.metric-label {
    color: var(--muted);
    text-transform: uppercase;
    font-size: 0.8rem;
    letter-spacing: 0.11em;
    font-weight: 700;
    margin-bottom: 0.7rem;
}

.metric-value {
    font-size: 2.15rem;
    font-weight: 850;
    letter-spacing: -0.04em;
    margin-bottom: 0.25rem;
}

.metric-foot {
    color: var(--muted);
    font-size: 0.94rem;
    line-height: 1.45;
}

.panel {
    background: linear-gradient(180deg, var(--panel-2) 0%, #0b1017 100%);
    border: 1px solid var(--line);
    padding: 1.2rem;
    border-radius: 0;
    box-shadow: var(--shadow);
}

.panel-tight {
    background: linear-gradient(180deg, var(--panel-2) 0%, #0b1017 100%);
    border: 1px solid var(--line);
    padding: 0.85rem 1rem;
    border-radius: 0;
    box-shadow: var(--shadow);
}

.warning-panel {
    background: linear-gradient(180deg, rgba(25,208,107,0.08), rgba(255,255,255,0.02));
    border: 1px solid rgba(25,208,107,0.26);
    padding: 1rem 1.1rem;
    min-height: 100%;
    box-shadow: var(--shadow);
}

.country-banner {
    display: inline-block;
    border: 1px solid var(--line);
    padding: 0.18rem 0.5rem;
    font-size: 0.8rem;
    color: #dbe5ef;
    margin-left: 0.55rem;
    transform: translateY(-0.12rem);
}

.overshoot-pill {
    display: inline-block;
    background: rgba(255, 77, 115, 0.2);
    color: #ffdbe6;
    border: 1px solid rgba(255, 77, 115, 0.34);
    padding: 0.45rem 0.75rem;
    font-weight: 800;
}

.driver-pill {
    display: inline-block;
    background: rgba(79,163,255,0.14);
    color: #b8d7ff;
    border: 1px solid rgba(79,163,255,0.28);
    padding: 0.42rem 0.7rem;
    font-weight: 700;
    font-size: 0.85rem;
}

.search-chip {
    border: 1px solid var(--line);
    background: rgba(255,255,255,0.02);
    padding: 0.55rem 0.8rem;
}

.table-wrap {
    border: 1px solid var(--line);
    background: linear-gradient(180deg, #0a0f16 0%, #080c12 100%);
    overflow: hidden;
}

.table-wrap table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.94rem;
}

.table-wrap thead th {
    text-align: left;
    color: var(--muted);
    font-weight: 700;
    padding: 0.85rem 0.8rem;
    border-bottom: 1px solid var(--line);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-size: 0.78rem;
}

.table-wrap tbody td {
    padding: 0.8rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.table-wrap tbody tr:hover {
    background: rgba(255,255,255,0.02);
}

.footer-note {
    color: var(--muted);
    text-align: center;
    padding-top: 1rem;
    font-size: 0.85rem;
}

hr {
    border: none;
    border-top: 1px solid var(--line);
    margin: 1rem 0;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.45rem;
}

.stTabs [data-baseweb="tab"] {
    background-color: #0a1017;
    border: 1px solid var(--line);
    padding: 0.52rem 1rem;
    border-radius: 0;
    color: var(--text);
}

.stTabs [aria-selected="true"] {
    background-color: #111823;
    border-color: rgba(25,208,107,0.35);
}

.stButton>button, .stDownloadButton>button {
    background: #0f151d;
    color: white;
    border: 1px solid var(--line);
    border-radius: 0;
    padding: 0.64rem 1rem;
    font-weight: 700;
}

.stButton>button:hover, .stDownloadButton>button:hover {
    border-color: rgba(25,208,107,0.45);
    color: #fff;
}

[data-testid="stSidebarNav"] {display:none;}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = BASE_DIR / "processed_data"


# ---------------------------------------------------------
# DEFAULT / DEMO DATA
# ---------------------------------------------------------
@st.cache_data
def get_default_summary():
    return pd.DataFrame({
        "iso_code": ["USA", "CHN", "RUS", "JPN", "DEU", "CAN", "SAU", "IND", "BRA", "ZAF", "GBR", "AUS", "POL", "ITA"],
        "country": [
            "United States", "China", "Russian Federation", "Japan", "Germany", "Canada",
            "Saudi Arabia", "India", "Brazil", "South Africa", "United Kingdom", "Australia", "Poland", "Italy"
        ],
        "cum_emissions_gt": [187.8, 231.6, 57.3, 41.1, 28.8, 18.4, 15.3, 74.2, 15.1, 13.9, 17.0, 12.5, 11.3, 14.3],
        "cum_fair_share_gt": [51.6, 225.6, 25.0, 21.8, 14.1, 5.7, 3.9, 225.6, 23.0, 8.9, 10.7, 3.7, 6.6, 10.1],
        "carbon_debt_gt": [136.14, 5.97, 32.26, 19.25, 14.73, 12.71, 11.48, -151.4, -7.9, 5.06, 6.34, 8.78, 4.77, 4.19],
        "debt_t_per_capita": [404.2, 4.2, 224.3, 154.6, 175.5, 317.1, 340.6, -106.2, -36.9, 80.0, 92.5, 329.5, 130.1, 71.1],
        "pct_of_fair_share_used": [364, 103, 229, 188, 208, 323, 392, 33, 66, 156, 159, 338, 171, 142],
        "overshoot_year": [1990, 2022, 1990, 1990, 1990, 1990, 1990, np.nan, np.nan, 1990, 1990, 1990, 1990, 1990],
        "pledge_year_final": [2050, 2060, 2060, 2050, 2045, 2050, 2060, 2070, 2050, 2050, 2050, 2050, 2050, 2050],
        "pledge_gap_years": [60, 38, 70, 60, 55, 60, 70, np.nan, np.nan, 60, 60, 60, 60, 60],
        "renewables_share_energy": [14, 18, 7, 14, 22, 12, 1.5, 12, 46, 12, 30, 18, 17, 19],
        "co2_per_capita": [14.3, 8.6, 11.2, 8.5, 7.9, 15.4, 18.7, 1.9, 2.1, 7.2, 4.7, 16.1, 7.9, 5.8],
        "industrialization_age": [173, 133, 170, 173, 173, 173, 88, 126, 173, 123, 173, 173, 173, 173],
        "overshoot_driver": [
            "Luxury Emitter", "Other Overshooter", "Fossil-Locked", "Other Overshooter",
            "Correcting", "Luxury Emitter", "Fossil-Locked", "Under/Not Overshoot",
            "Under/Not Overshoot", "Other Overshooter", "Correcting", "Luxury Emitter",
            "Other Overshooter", "Other Overshooter"
        ],
        "status": [
            "Overshooting", "Overshooting", "Overshooting", "Overshooting", "Overshooting",
            "Overshooting", "Overshooting", "No overshoot (yet)", "No overshoot (yet)",
            "Overshooting", "Overshooting", "Overshooting", "Overshooting", "Overshooting"
        ],
    })


@st.cache_data
def get_default_historical():
    years = list(range(1990, 2024))
    country_specs = {
        "USA": ("United States", 5000, 4800, 8, 19, 14),
        "CHN": ("China", 2500, 12000, 4, 18, 8),
        "DEU": ("Germany", 1200, 650, 3, 42, 8),
        "IND": ("India", 800, 3200, 2, 12, 2),
        "RUS": ("Russian Federation", 2400, 1700, 2.5, 7, 11),
        "JPN": ("Japan", 1100, 1050, 2.0, 14, 8),
        "CAN": ("Canada", 450, 700, 3.0, 12, 15),
        "GBR": ("United Kingdom", 800, 400, 4.5, 30, 5),
        "AUS": ("Australia", 300, 430, 3.2, 18, 16),
    }
    rows = []
    for iso, (country, start_e, end_e, start_r, end_r, end_pc) in country_specs.items():
        emissions = np.linspace(start_e, end_e, len(years))
        renew = np.linspace(start_r, end_r, len(years))
        percap = np.linspace(max(1.0, end_pc * 0.9), end_pc, len(years))
        for i, y in enumerate(years):
            rows.append({
                "iso_code": iso,
                "country": country,
                "year": y,
                "co2": float(emissions[i]),
                "renewables_share_energy": float(renew[i]),
                "co2_per_capita": float(percap[i]),
            })
    return pd.DataFrame(rows)


@st.cache_data
def get_default_scenarios():
    years = list(range(2025, 2051, 5))
    rows = []
    for iso, country, start_debt in [
        ("CHN", "China", 5.97),
        ("USA", "United States", 136.14),
        ("DEU", "Germany", 14.73),
        ("IND", "India", -151.4),
    ]:
        for scenario, growth in [("baseline", 1.03), ("ndc", 1.00), ("ambitious", 0.96)]:
            debt = start_debt
            for y in years:
                debt *= growth
                rows.append({
                    "iso_code": iso,
                    "country": country,
                    "year": y,
                    "scenario": scenario,
                    "debt_gt": float(debt),
                })
    return pd.DataFrame(rows)


@st.cache_data
def get_default_benchmarks():
    return pd.DataFrame([
        {"target": "1.5C", "probability": "50%", "remain2020_gt": 500, "emitted_2020_24_gt": 137.6, "remain2025_gt": 362.4},
        {"target": "1.5C", "probability": "66%", "remain2020_gt": 400, "emitted_2020_24_gt": 137.6, "remain2025_gt": 262.4},
        {"target": "2C",   "probability": "50%", "remain2020_gt": 1350, "emitted_2020_24_gt": 137.6, "remain2025_gt": 1212.4},
        {"target": "2C",   "probability": "67%", "remain2020_gt": 1150, "emitted_2020_24_gt": 137.6, "remain2025_gt": 1012.4},
    ])


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def normalize_summary(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "carbon_debt_gt": "debt_gt",
        "debt_t_per_capita": "debt_per_capita",
        "pct_of_fair_share_used": "pct_used",
        "budget_used_pct": "pct_used",
        "cum_fair_share_gt": "fair_share_gt",
        "fair_share_budget_gt": "fair_share_gt",
        "country_name": "country",
        "iso3": "iso_code",
        "pledge_year": "pledge_year_final",
    }
    df = df.rename(columns={c: rename_map.get(c, c) for c in df.columns}).copy()

    required = [
        "iso_code", "country", "debt_gt", "debt_per_capita", "pct_used", "overshoot_year",
        "cum_emissions_gt", "fair_share_gt", "pledge_year_final", "pledge_gap_years",
        "renewables_share_energy", "co2_per_capita", "industrialization_age", "overshoot_driver", "status"
    ]
    for col in required:
        if col not in df.columns:
            df[col] = np.nan

    df["iso_code"] = df["iso_code"].astype(str).str.strip().str.upper()
    df["country"] = df["country"].astype(str).str.strip()
    for c in [
        "debt_gt", "debt_per_capita", "pct_used", "overshoot_year", "cum_emissions_gt",
        "fair_share_gt", "pledge_year_final", "pledge_gap_years", "renewables_share_energy",
        "co2_per_capita", "industrialization_age"
    ]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def normalize_historical(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "annual_emissions_mt": "co2",
        "country_name": "country",
        "iso3": "iso_code",
    }
    df = df.rename(columns={c: rename_map.get(c, c) for c in df.columns}).copy()

    for col in ["iso_code", "country", "year", "co2"]:
        if col not in df.columns:
            df[col] = np.nan
    if "renewables_share_energy" not in df.columns:
        df["renewables_share_energy"] = np.nan
    if "co2_per_capita" not in df.columns:
        df["co2_per_capita"] = np.nan
    if "cum_emissions_gt" not in df.columns and "co2" in df.columns:
        df = df.sort_values(["iso_code", "year"])
        df["cum_emissions_gt"] = df.groupby("iso_code")["co2"].cumsum() * 1e-3

    df["iso_code"] = df["iso_code"].astype(str).str.upper().str.strip()
    df["country"] = df["country"].astype(str).str.strip()
    for c in ["year", "co2", "renewables_share_energy", "co2_per_capita", "cum_emissions_gt"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def normalize_benchmarks(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "prob": "probability",
        "remain2020": "remain2020_gt",
        "emitted2020_24": "emitted_2020_24_gt",
        "remain2025": "remain2025_gt",
    }
    df = df.rename(columns={c: rename_map.get(c, c) for c in df.columns}).copy()
    for col in ["remain2020_gt", "emitted_2020_24_gt", "remain2025_gt"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "probability" in df.columns:
        def fmt_prob(x):
            if pd.isna(x):
                return "—"
            try:
                val = float(x)
                return f"{int(val * 100)}%" if val <= 1 else f"{int(val)}%"
            except (TypeError, ValueError):
                return str(x)
        df["probability"] = df["probability"].map(fmt_prob)
    return df


def enrich_summary_from_drivers(df: pd.DataFrame) -> pd.DataFrame:
    drivers_path = PROCESSED_DIR / "step2_overshoot_drivers.csv"
    if not drivers_path.exists():
        return df
    drivers = pd.read_csv(drivers_path)
    drivers = drivers.rename(columns={
        "overshoot_driver_tag": "overshoot_driver",
        "budget_used_pct": "pct_used_driver",
    })
    merge_cols = ["iso_code", "status", "renewables_share_energy", "co2_per_capita", "industrialization_age", "overshoot_driver", "pct_used_driver"]
    drivers = drivers[[c for c in merge_cols if c in drivers.columns]].copy()
    drivers["iso_code"] = drivers["iso_code"].astype(str).str.strip().str.upper()
    merged = df.merge(drivers, on="iso_code", how="left", suffixes=("", "_driver"))
    for col in ["status", "renewables_share_energy", "co2_per_capita", "industrialization_age", "overshoot_driver"]:
        driver_col = f"{col}_driver"
        if driver_col in merged.columns:
            merged[col] = merged[col].fillna(merged[driver_col])
            merged = merged.drop(columns=[driver_col])
    if "pct_used_driver" in merged.columns:
        merged["pct_used"] = merged["pct_used"].fillna(merged["pct_used_driver"])
        merged = merged.drop(columns=["pct_used_driver"])
    return merged


def normalize_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "projected_debt_gt": "debt_gt",
        "carbon_debt_gt": "debt_gt",
        "country_name": "country",
        "iso3": "iso_code",
    }
    df = df.rename(columns={c: rename_map.get(c, c) for c in df.columns}).copy()

    for col in ["iso_code", "country", "year", "scenario", "debt_gt"]:
        if col not in df.columns:
            df[col] = np.nan

    df["iso_code"] = df["iso_code"].astype(str).str.upper().str.strip()
    df["country"] = df["country"].astype(str).str.strip()
    df["scenario"] = df["scenario"].astype(str).str.strip().str.lower()
    for c in ["year", "debt_gt"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def safe_metric_value(x, suffix="", signed=False, digits=1):
    if pd.isna(x):
        return "—"
    if signed:
        return f"{x:+,.{digits}f}{suffix}"
    return f"{x:,.{digits}f}{suffix}"


def render_metric_card(label, value, foot, accent="var(--green)"):
    st.markdown(
        f"""
        <div class="metric-card" style="border-left: 4px solid {accent};">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-foot">{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_benchmark_card(target, prob, remain2020, emitted, remain2025):
    st.markdown(
        f"""
        <div class="panel" style="border-left:4px solid var(--green); min-height: 250px;">
            <div class="badge" style="margin-bottom:0.9rem;">{target} Target</div>
            <div style="font-size:2.7rem;font-weight:850;letter-spacing:-0.04em;">{remain2025:.0f} Gt</div>
            <div class="metric-label" style="margin-top:0.1rem;">Remaining budget (2025+)</div>
            <div style="margin-top:1rem;display:grid;grid-template-columns:1fr auto;gap:0.52rem;">
                <div class="small-muted">Probability</div><div>{prob}</div>
                <div class="small-muted">2020 Budget</div><div>{remain2020:.0f} Gt</div>
                <div class="small-muted">Emitted (2020–24)</div><div style="color:var(--red);">{emitted:.1f} Gt</div>
            </div>
            <hr>
            <div class="small-muted" style="font-style:italic; line-height:1.55;">
                Budget is defined as cumulative CO₂ emissions from the start of the benchmark year until net zero is reached.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_html_table(df: pd.DataFrame, debt_col="Debt (Gt)") -> str:
    rows = []
    for _, r in df.iterrows():
        debt_html = f"<span style='color:var(--red);font-weight:800;'>{r[debt_col]}</span>" if debt_col in r else ""
        row_html = (
            f"<tr>"
            f"<td>{r.iloc[0]}</td>"
            f"<td>{r.iloc[1]}</td>"
            f"<td>{r.iloc[2]}</td>"
            f"<td>{r.iloc[3]}</td>"
            f"<td>{debt_html}</td>"
            f"<td>{r.iloc[5]}</td>"
            f"<td>{r.iloc[6]}</td>"
            f"</tr>"
        )
        rows.append(row_html)
    header = "".join([f"<th>{c}</th>" for c in df.columns])
    return f"<div class='table-wrap'><table><thead><tr>{header}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"


@st.cache_data
def load_csv_if_exists(path: Path):
    if path.exists():
        return pd.read_csv(path)
    return None


@st.cache_data
def load_project_data():
    summary = load_csv_if_exists(PROCESSED_DIR / "tracker_dashboard_summary.csv")
    if summary is None:
        summary = load_csv_if_exists(PROCESSED_DIR / "tracker_summary.csv")

    historical = load_csv_if_exists(PROCESSED_DIR / "annual_fairshare_panel.csv")
    if historical is None:
        historical = load_csv_if_exists(PROCESSED_DIR / "clean_carbon_panel.csv")

    scenarios = load_csv_if_exists(PROCESSED_DIR / "project_debt_scenarios.csv")
    benchmarks = load_csv_if_exists(PROCESSED_DIR / "ar6_adjusted_budgets.csv")

    return summary, historical, scenarios, benchmarks


# ---------------------------------------------------------
# DATA LOADING PRIORITY
# project files -> uploaded files -> demo data
# ---------------------------------------------------------
project_summary, project_historical, project_scenarios, project_benchmarks = load_project_data()

st.sidebar.markdown('<div class="brand-wrap">', unsafe_allow_html=True)
st.sidebar.markdown("## 🍃 BudgetTracker")
st.sidebar.markdown(
    '<div class="brand-sub">IPCC AR6 Analytics Engine</div>',
    unsafe_allow_html=True,
)
st.sidebar.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("### Data Input")
summary_file = st.sidebar.file_uploader("Upload summary CSV", type=["csv"], key="summary")
historical_file = st.sidebar.file_uploader("Upload historical panel CSV", type=["csv"], key="historical")
scenario_file = st.sidebar.file_uploader("Upload scenarios CSV", type=["csv"], key="scenario")
benchmark_file = st.sidebar.file_uploader("Upload benchmarks CSV", type=["csv"], key="benchmarks")

source_mode = "demo"

try:
    if project_summary is not None:
        df_summary = enrich_summary_from_drivers(normalize_summary(project_summary))
        source_mode = "project"
    elif summary_file is not None:
        df_summary = normalize_summary(pd.read_csv(summary_file))
        source_mode = "upload"
    else:
        df_summary = normalize_summary(get_default_summary())

    if project_historical is not None:
        df_historical = normalize_historical(project_historical)
    elif historical_file is not None:
        df_historical = normalize_historical(pd.read_csv(historical_file))
    else:
        df_historical = normalize_historical(get_default_historical())

    if project_scenarios is not None:
        df_scenarios = normalize_scenarios(project_scenarios)
    elif scenario_file is not None:
        df_scenarios = normalize_scenarios(pd.read_csv(scenario_file))
    else:
        df_scenarios = normalize_scenarios(get_default_scenarios())

    if project_benchmarks is not None:
        df_benchmarks = normalize_benchmarks(project_benchmarks)
    elif benchmark_file is not None:
        df_benchmarks = normalize_benchmarks(pd.read_csv(benchmark_file))
    else:
        df_benchmarks = normalize_benchmarks(get_default_benchmarks())

except Exception as e:
    st.sidebar.error(f"Data loading error: {e}")
    df_summary = normalize_summary(get_default_summary())
    df_historical = normalize_historical(get_default_historical())
    df_scenarios = normalize_scenarios(get_default_scenarios())
    df_benchmarks = normalize_benchmarks(get_default_benchmarks())
    source_mode = "demo"

if source_mode == "project":
    st.sidebar.success("Using processed_data files.")
elif source_mode == "upload":
    st.sidebar.success("Using uploaded summary file.")
else:
    st.sidebar.info("Using demo data.")

# ---------------------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------------------
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    [
        "Analytics Dashboard",
        "Country Explorer",
        "Country Deep Dive",
        "Accountability",
        "Drivers",
        "Global Benchmarks",
    ],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.subheader("Scenario Overlay")
show_ai = st.sidebar.checkbox("Show AI / datacentre overlay", value=False)
if show_ai:
    ai_twh_2030 = st.sidebar.slider("AI electricity 2030 (TWh)", 500, 3000, 1200, 100)
    ai_twh_2050 = st.sidebar.slider("AI electricity 2050 (TWh)", 1000, 8000, 2500, 200)
    clean_share_2050 = st.sidebar.slider("Clean grid share by 2050 (%)", 30, 100, 70, 5)

st.sidebar.markdown("---")
st.sidebar.markdown(f"🟢 **System Status:** {'Nominal' if source_mode != 'demo' else 'Demo Mode'}")

# ---------------------------------------------------------
# COMMON CALCULATIONS
# ---------------------------------------------------------
search_global = st.text_input("Search ISO or Country...", placeholder="Search ISO or Country...")
if search_global:
    mask = (
        df_summary["country"].str.contains(search_global, case=False, na=False)
        | df_summary["iso_code"].str.contains(search_global, case=False, na=False)
    )
    df_filtered_global = df_summary[mask].copy()
else:
    df_filtered_global = df_summary.copy()

highest_debt = df_summary.loc[df_summary["debt_gt"].idxmax()] if len(df_summary) and df_summary["debt_gt"].notna().any() else None
lowest_debt = df_summary.loc[df_summary["debt_gt"].idxmin()] if len(df_summary) and df_summary["debt_gt"].notna().any() else None
avg_per_capita = df_summary["debt_per_capita"].mean(skipna=True) if "debt_per_capita" in df_summary.columns else np.nan
median_gap = df_summary["pledge_gap_years"].median(skipna=True) if "pledge_gap_years" in df_summary.columns else np.nan
overshot_count = int(df_summary["overshoot_year"].notna().sum()) if "overshoot_year" in df_summary.columns else 0

bench_15_50 = None
if not df_benchmarks.empty:
    bench_match = df_benchmarks[df_benchmarks["target"].astype(str).str.contains("1.5", na=False)]
    if not bench_match.empty:
        bench_15_50 = bench_match.iloc[0]

color_driver = {
    "Fossil-Locked": "#ff4d73",
    "Correcting": "#24d07a",
    "Luxury Emitter": "#f8b84e",
    "Other Overshooter": "#4fa3ff",
    "Under/Not Overshoot": "#b4bec5",
}

# ---------------------------------------------------------
# PAGE: DASHBOARD
# ---------------------------------------------------------
if page == "Analytics Dashboard":
    st.markdown('<div class="section-title">Analytics Dashboard</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero">
            <div class="badge">Critical Analytics</div>
            <div class="hero-title">The Carbon Budget Deficit</div>
            <div class="hero-text">
                Explore country-level fair-share overshoot, cumulative carbon debt, and the gap between historical responsibility and climate pledges.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if highest_debt is not None:
            render_metric_card("Highest Debt", f"{highest_debt['debt_gt']:.1f} Gt", highest_debt["country"], accent="var(--red)")
    with c2:
        if lowest_debt is not None:
            render_metric_card("Net Creditor", f"{lowest_debt['debt_gt']:.1f} Gt", lowest_debt["country"], accent="var(--green)")
    with c3:
        render_metric_card("Median Pledge Gap", safe_metric_value(median_gap, " yrs", digits=0), "Overshoot year → pledge year", accent="var(--blue)")
    with c4:
        render_metric_card("Countries Overshot", f"{overshot_count}", "Countries with a recorded overshoot year", accent="var(--amber)")

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    left, right = st.columns([2.2, 1])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### Global Carbon Debt Map")
        st.markdown('<div class="small-muted">Countries colored by cumulative carbon debt or credit relative to fair share.</div>', unsafe_allow_html=True)
        try:
            fig_map = px.choropleth(
                df_filtered_global,
                locations="iso_code",
                locationmode="ISO-3",
                color="debt_gt",
                hover_name="country",
                hover_data={
                    "iso_code": True,
                    "debt_gt": ":.2f",
                    "debt_per_capita": ":.2f",
                    "pct_used": ":.0f",
                    "overshoot_year": True,
                    "pledge_year_final": True,
                },
                color_continuous_scale="RdYlGn_r",
            )
            fig_map.update_layout(
                paper_bgcolor="#0f141d",
                plot_bgcolor="#0f141d",
                font_color="#f2f5f8",
                margin=dict(l=0, r=0, t=10, b=0),
                coloraxis_colorbar=dict(title="Debt (Gt)"),
            )
            fig_map.update_geos(showframe=False, showcoastlines=False, bgcolor="#0f141d", projection_type="natural earth")
            st.plotly_chart(fig_map, use_container_width=True)
        except Exception as e:
            st.warning(f"Map could not be rendered: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        if bench_15_50 is not None:
            st.markdown(
                f"""
                <div class="warning-panel">
                    <div style="font-weight:850;font-size:1.2rem;margin-bottom:0.6rem;">⚠ Climate Warning</div>
                    <div style="font-size:1.2rem;font-weight:700;line-height:1.45;margin-bottom:0.75rem;">
                        The remaining 1.5°C budget is down to about {bench_15_50['remain2025_gt']:.0f} Gt CO₂.
                    </div>
                    <div class="small-muted" style="line-height:1.6;">
                        This budget framing turns climate data into a fairness question: who used the shared atmospheric space, and who remains within it?
                    </div>
                    <hr>
                    <div class="small-muted" style="font-style:italic;">IPCC AR6-aligned benchmark layer.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    col_table, col_story = st.columns([2, 1])
    with col_table:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### Global Carbon Debt Leaderboard")
        st.markdown('<div class="small-muted">Countries with the largest cumulative fair-share overshoot.</div>', unsafe_allow_html=True)
        leaderboard = (
            df_summary[["iso_code", "country", "cum_emissions_gt", "fair_share_gt", "debt_gt", "debt_per_capita", "overshoot_year"]]
            .sort_values("debt_gt", ascending=False)
            .head(12)
            .copy()
        )
        leaderboard = leaderboard.assign(
            **{
                "Cumulative (Gt)": leaderboard["cum_emissions_gt"].map(lambda x: f"{x:,.1f}" if pd.notna(x) else "—"),
                "Fair Share (Gt)": leaderboard["fair_share_gt"].map(lambda x: f"{x:,.1f}" if pd.notna(x) else "—"),
                "Debt (Gt)": leaderboard["debt_gt"].map(lambda x: f"{x:,.2f}" if pd.notna(x) else "—"),
                "Debt/Capita (t)": leaderboard["debt_per_capita"].map(lambda x: f"{x:,.1f}" if pd.notna(x) else "—"),
                "Overshoot Year": leaderboard["overshoot_year"].map(lambda x: f"{int(x)}" if pd.notna(x) else "—"),
            }
        )[["iso_code", "country", "Cumulative (Gt)", "Fair Share (Gt)", "Debt (Gt)", "Debt/Capita (t)", "Overshoot Year"]]
        leaderboard.columns = ["ISO", "Country", "Cumulative (Gt)", "Fair Share (Gt)", "Debt (Gt)", "Debt/Capita (t)", "Overshoot Year"]
        st.markdown(build_html_table(leaderboard), unsafe_allow_html=True)
        st.download_button("Export full table (CSV)", df_summary.to_csv(index=False).encode("utf-8"), "carbon_budget_summary.csv", "text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_story:
        st.markdown(
            """
            <div class="panel" style="min-height:100%;">
                <div style="font-size:1.2rem;font-weight:850;margin-bottom:0.6rem;">Why this matters</div>
                <div class="small-muted" style="line-height:1.7;">
                    <b>Fair-share budgets</b> turn climate accounting into an equity question.<br><br>
                    <b>Carbon debt</b> captures cumulative overuse of shared atmospheric space.<br><br>
                    <b>Overshoot timing</b> shows when countries crossed equitable limits.<br><br>
                    <b>Pledge gaps</b> connect historical responsibility to future ambition.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# PAGE: COUNTRY EXPLORER
# ---------------------------------------------------------
elif page == "Country Explorer":
    st.markdown('<div class="section-title">Country Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Browse country-level carbon debt, fair share, and overshoot timing.</div>', unsafe_allow_html=True)

    explorer_search = st.text_input("Filter by country or ISO", placeholder="Type a country name...")
    df_explorer = df_summary.copy()
    if explorer_search:
        df_explorer = df_explorer[
            df_explorer["country"].str.contains(explorer_search, case=False, na=False) |
            df_explorer["iso_code"].str.contains(explorer_search, case=False, na=False)
        ].copy()

    display = df_explorer[[
        "iso_code", "country", "cum_emissions_gt", "fair_share_gt", "debt_gt", "debt_per_capita", "overshoot_year"
    ]].copy()
    display = display.sort_values("debt_gt", ascending=False)
    display.columns = ["ISO", "Country", "Cumulative (Gt)", "Fair Share (Gt)", "Debt (Gt)", "Debt/Capita (t)", "Overshoot Year"]
    display = display.assign(
        **{
            "Cumulative (Gt)": display["Cumulative (Gt)"].map(lambda x: f"{x:,.1f}" if pd.notna(x) else "—"),
            "Fair Share (Gt)": display["Fair Share (Gt)"].map(lambda x: f"{x:,.1f}" if pd.notna(x) else "—"),
            "Debt (Gt)": display["Debt (Gt)"].map(lambda x: f"{x:,.2f}" if pd.notna(x) else "—"),
            "Debt/Capita (t)": display["Debt/Capita (t)"].map(lambda x: f"{x:,.1f}" if pd.notna(x) else "—"),
            "Overshoot Year": display["Overshoot Year"].map(lambda x: f"{int(x)}" if pd.notna(x) else "—"),
        }
    )
    st.markdown(build_html_table(display.head(40)), unsafe_allow_html=True)
    st.download_button("Export filtered table (CSV)", df_explorer.to_csv(index=False).encode("utf-8"), "filtered_countries.csv", "text/csv")

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    st.markdown("### Overshoot Timeline")
    df_timeline = df_summary.dropna(subset=["overshoot_year"]).copy()
    if len(df_timeline) > 0:
        df_timeline = df_timeline.sort_values(["overshoot_year", "debt_gt"], ascending=[True, False]).head(25)
        fig_timeline = px.scatter(
            df_timeline,
            x="overshoot_year",
            y="debt_gt",
            size=np.abs(df_timeline["debt_gt"].fillna(0)) + 1,
            color="debt_gt",
            hover_name="country",
            text="iso_code",
            color_continuous_scale="RdYlGn_r",
            labels={"overshoot_year": "Overshoot Year", "debt_gt": "Carbon Debt (Gt)"},
        )
        fig_timeline.update_traces(textposition="top center")
        fig_timeline.update_layout(
            paper_bgcolor="#0f141d",
            plot_bgcolor="#0f141d",
            font_color="#f2f5f8",
            margin=dict(l=0, r=0, t=15, b=0),
            coloraxis_colorbar=dict(title="Debt (Gt)"),
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
    else:
        st.info("No overshoot-year data available.")

# ---------------------------------------------------------
# PAGE: COUNTRY DEEP DIVE
# ---------------------------------------------------------
elif page == "Country Deep Dive":
    st.markdown('<div class="section-title">Country Deep Dive</div>', unsafe_allow_html=True)
    country_options = df_summary["country"].dropna().sort_values().unique().tolist()
    default_country = "China" if "China" in country_options else country_options[0]
    country = st.selectbox("Select country", country_options, index=country_options.index(default_country) if default_country in country_options else 0)

    row = df_summary[df_summary["country"] == country].iloc[0]
    iso = row["iso_code"]
    hist = df_historical[df_historical["iso_code"] == iso].sort_values("year").copy()
    scen = df_scenarios[df_scenarios["iso_code"] == iso].sort_values(["scenario", "year"]).copy()

    head_left, head_right = st.columns([3, 1])
    with head_left:
        st.markdown(
            f"""
            <div style="font-size:2.6rem;font-weight:850;letter-spacing:-0.04em;">
                {country} <span class="country-banner">{iso}</span>
            </div>
            <div class="section-subtitle">Climate Impact Profile & Carbon Budget Tracker</div>
            """,
            unsafe_allow_html=True,
        )
        if pd.notna(row.get("overshoot_driver")):
            st.markdown(f"<span class='driver-pill'>{row['overshoot_driver']}</span>", unsafe_allow_html=True)
    with head_right:
        if pd.notna(row["overshoot_year"]):
            st.markdown(
                f"""
                <div style="text-align:right;margin-top:0.55rem;">
                    <span class="overshoot-pill">Overshot Budget in {int(row['overshoot_year'])}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        render_metric_card("Cumulative CO₂", safe_metric_value(row.get("cum_emissions_gt"), " Gt"), "Historical emissions total", accent="var(--green)")
    with mc2:
        render_metric_card("Carbon Debt / Credit", safe_metric_value(row.get("debt_gt"), " Gt", signed=True, digits=2), "Relative to fair share", accent="var(--red)" if row.get("debt_gt", 0) >= 0 else "var(--green)")
    with mc3:
        render_metric_card("Per Capita Debt", safe_metric_value(row.get("debt_per_capita"), " t"), "Tonnes CO₂ per person", accent="var(--blue)")
    with mc4:
        render_metric_card("Budget Used", safe_metric_value(row.get("pct_used"), "%", digits=0), "Of allocated fair share", accent="var(--amber)")

    tabs = st.tabs(["Historical Trends", "Future Scenarios", "Method & Interpretation"])

    with tabs[0]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Annual Emissions (Mt CO₂)")
            if len(hist) > 0 and hist["co2"].notna().any():
                fig1 = px.area(hist, x="year", y="co2", labels={"co2": "Mt CO₂", "year": "Year"})
                fig1.update_traces(line_color="#24d07a")
                fig1.update_layout(paper_bgcolor="#0f141d", plot_bgcolor="#0f141d", font_color="#f2f5f8", margin=dict(l=0, r=0, t=10, b=0))
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("No historical emissions data available for this country.")

        with c2:
            st.markdown("#### Cumulative Emissions vs Fair Share")
            if len(hist) > 0 and hist["cum_emissions_gt"].notna().any():
                fair_series = pd.DataFrame({
                    "year": hist["year"],
                    "Cumulative emissions": hist["cum_emissions_gt"],
                    "Fair share limit": np.linspace(0, row.get("fair_share_gt", np.nan), len(hist)),
                })
                figcum = go.Figure()
                figcum.add_trace(go.Scatter(x=fair_series["year"], y=fair_series["Cumulative emissions"], mode="lines", name="Cumulative emissions", line=dict(color="#24d07a", width=3)))
                figcum.add_trace(go.Scatter(x=fair_series["year"], y=fair_series["Fair share limit"], mode="lines", name="Fair share limit", line=dict(color="#4fa3ff", width=2, dash="dash")))
                if pd.notna(row.get("overshoot_year")):
                    figcum.add_vline(x=int(row["overshoot_year"]), line_dash="dot", line_color="#ff4d73")
                figcum.update_layout(paper_bgcolor="#0f141d", plot_bgcolor="#0f141d", font_color="#f2f5f8", margin=dict(l=0, r=0, t=10, b=0), legend_title_text="")
                st.plotly_chart(figcum, use_container_width=True)
            else:
                st.info("No cumulative panel data available for this country.")

        st.markdown("<div style='height:0.4rem;'></div>", unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            st.markdown("#### Renewable Energy Share (%)")
            if len(hist) > 0 and hist["renewables_share_energy"].notna().any():
                fig2 = px.line(hist, x="year", y="renewables_share_energy", labels={"renewables_share_energy": "%", "year": "Year"})
                fig2.update_traces(line_color="#4fa3ff", line_width=3)
                fig2.update_layout(paper_bgcolor="#0f141d", plot_bgcolor="#0f141d", font_color="#f2f5f8", margin=dict(l=0, r=0, t=10, b=0))
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No renewable share data available for this country.")
        with c4:
            st.markdown("#### CO₂ per capita")
            if len(hist) > 0 and hist["co2_per_capita"].notna().any():
                figpc = px.line(hist, x="year", y="co2_per_capita", labels={"co2_per_capita": "t CO₂/person", "year": "Year"})
                figpc.update_traces(line_color="#f8b84e", line_width=3)
                figpc.update_layout(paper_bgcolor="#0f141d", plot_bgcolor="#0f141d", font_color="#f2f5f8", margin=dict(l=0, r=0, t=10, b=0))
                st.plotly_chart(figpc, use_container_width=True)
            else:
                st.info("No per-capita emissions data available for this country.")

    with tabs[1]:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("#### Future Carbon Debt Scenarios")
            if len(scen) > 0 and scen["debt_gt"].notna().any():
                fig3 = px.line(scen, x="year", y="debt_gt", color="scenario", markers=True, labels={"debt_gt": "Projected Debt (Gt)", "year": "Year"})
                fig3.update_layout(paper_bgcolor="#0f141d", plot_bgcolor="#0f141d", font_color="#f2f5f8", margin=dict(l=0, r=0, t=10, b=0), legend_title_text="Scenario")
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("No scenario data available for this country.")
        with c2:
            st.markdown("#### Accountability")
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown(f"**Overshoot year:** {int(row['overshoot_year']) if pd.notna(row['overshoot_year']) else '—'}")
            st.markdown(f"**Pledge year:** {int(row['pledge_year_final']) if pd.notna(row['pledge_year_final']) else '—'}")
            st.markdown(f"**Pledge gap:** {int(row['pledge_gap_years']) if pd.notna(row['pledge_gap_years']) else '—'} years")
            st.markdown(f"**Status:** {row['status'] if pd.notna(row['status']) else '—'}")
            st.markdown(f"**Industrialization age:** {int(row['industrialization_age']) if pd.notna(row['industrialization_age']) else '—'} years")
            if show_ai:
                extra_debt = (ai_twh_2050 * (100 - clean_share_2050) / 100 * 0.4) / 1000
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(f"**AI overlay (illustrative):** +{extra_debt:.2f} Gt by 2050")
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown(
            """
            <div class="panel">
                <div style="font-size:1.15rem;font-weight:850;margin-bottom:0.7rem;">How to read this profile</div>
                <div class="small-muted" style="line-height:1.7;">
                    <b>Fair-share budget</b> reflects the country’s equitable portion of the global carbon budget under the selected lens.<br><br>
                    <b>Carbon debt</b> is cumulative emissions minus cumulative fair share.<br><br>
                    <b>Overshoot year</b> indicates when cumulative emissions first exceeded fair share.<br><br>
                    <b>Pledge gap</b> connects overshoot timing to net-zero ambition.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.download_button("Export country profile (CSV)", row.to_frame().T.to_csv(index=False).encode("utf-8"), f"{country.lower().replace(' ', '_')}_profile.csv", "text/csv")

# ---------------------------------------------------------
# PAGE: ACCOUNTABILITY
# ---------------------------------------------------------
elif page == "Accountability":
    st.markdown('<div class="section-title">Accountability</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">How overshoot timing compares with net-zero pledges.</div>', unsafe_allow_html=True)

    acc = df_summary.dropna(subset=["overshoot_year", "pledge_year_final"]).copy()
    if len(acc) > 0:
        acc = acc.sort_values("pledge_gap_years", ascending=False)
        fig_gap = go.Figure()
        fig_gap.add_trace(go.Scatter(x=acc["country"], y=acc["overshoot_year"], mode="markers", name="Overshoot year", marker=dict(size=9, color="#ff4d73")))
        fig_gap.add_trace(go.Scatter(x=acc["country"], y=acc["pledge_year_final"], mode="markers", name="Pledge year", marker=dict(size=9, color="#24d07a")))
        for _, r in acc.head(25).iterrows():
            fig_gap.add_shape(type="line", x0=r["country"], x1=r["country"], y0=r["overshoot_year"], y1=r["pledge_year_final"], line=dict(color="rgba(255,255,255,0.22)", width=2))
        fig_gap.update_layout(
            paper_bgcolor="#0f141d", plot_bgcolor="#0f141d", font_color="#f2f5f8",
            margin=dict(l=0, r=0, t=10, b=0), xaxis_title="Country", yaxis_title="Year", height=560
        )
        st.plotly_chart(fig_gap, use_container_width=True)

        top_gap = acc[["iso_code", "country", "overshoot_year", "pledge_year_final", "pledge_gap_years", "status"]].head(20)
        st.dataframe(top_gap, use_container_width=True, hide_index=True)
    else:
        st.info("Need overshoot year and pledge year data to build this page.")

# ---------------------------------------------------------
# PAGE: DRIVERS
# ---------------------------------------------------------
elif page == "Drivers":
    st.markdown('<div class="section-title">Drivers</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Structural explanations for overshoot patterns.</div>', unsafe_allow_html=True)

    driver_df = df_summary.dropna(subset=["renewables_share_energy", "pct_used", "co2_per_capita"]).copy()
    if len(driver_df) > 0:
        fig_drivers = px.scatter(
            driver_df,
            x="renewables_share_energy",
            y="pct_used",
            size="co2_per_capita",
            color="overshoot_driver",
            hover_name="country",
            color_discrete_map=color_driver,
            labels={
                "renewables_share_energy": "Renewables Share (%)",
                "pct_used": "% Fair-Share Budget Used",
                "co2_per_capita": "CO₂ per capita",
                "overshoot_driver": "Driver"
            }
        )
        fig_drivers.add_hline(y=100, line_dash="dash", line_color="#b4bec5")
        fig_drivers.update_layout(
            paper_bgcolor="#0f141d", plot_bgcolor="#0f141d", font_color="#f2f5f8",
            margin=dict(l=0, r=0, t=10, b=0), height=560
        )
        st.plotly_chart(fig_drivers, use_container_width=True)

        counts = driver_df["overshoot_driver"].value_counts().reset_index()
        counts.columns = ["Driver", "Countries"]
        st.dataframe(counts, use_container_width=True, hide_index=True)
    else:
        st.info("Need renewables, per-capita emissions, and budget-used data for this page.")

# ---------------------------------------------------------
# PAGE: GLOBAL BENCHMARKS
# ---------------------------------------------------------
elif page == "Global Benchmarks":
    st.markdown('<div class="section-title">Global Benchmarks</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Remaining carbon budgets from IPCC AR6 adjusted to 2025.</div>', unsafe_allow_html=True)

    bench_cols = st.columns(3)
    bench_records = df_benchmarks.to_dict("records")
    for i, rec in enumerate(bench_records[:3]):
        with bench_cols[i]:
            render_benchmark_card(rec["target"], rec["probability"], rec["remain2020_gt"], rec["emitted_2020_24_gt"], rec["remain2025_gt"])

    second_row = st.columns([1, 1])
    if len(bench_records) >= 4:
        with second_row[0]:
            rec = bench_records[3]
            render_benchmark_card(rec["target"], rec["probability"], rec["remain2020_gt"], rec["emitted_2020_24_gt"], rec["remain2025_gt"])

    with second_row[1]:
        if bench_15_50 is not None:
            remain = float(bench_15_50["remain2025_gt"])
            annual = 40.0
            years_left = remain / annual
            st.markdown(
                f"""
                <div class="panel" style="min-height:250px; display:flex; align-items:center; justify-content:center; text-align:center;">
                    <div>
                        <div style="font-size:2.1rem;margin-bottom:0.35rem;">⚠️</div>
                        <div style="font-size:1.5rem;font-weight:850;margin-bottom:0.55rem;">Global Overshoot Alert</div>
                        <div class="small-muted" style="font-size:1.06rem;max-width:420px;line-height:1.6;">
                            At ~40 Gt/year, the 1.5°C (50%) budget would be exhausted in roughly <b>{years_left:.1f} years</b>.
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel">
            <div style="font-size:1.15rem;font-weight:850;margin-bottom:0.6rem;">Climate Restoration Strategy</div>
            <div class="small-muted" style="line-height:1.7;">
                These benchmarks become meaningful only when linked to equity: who used the budget, who overshot fair share, and who would carry future drawdown obligations.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(
    f"""
    <div class="footer-note">
        BudgetTracker – IPCC AR6 Fair-Share Explorer • March 2026 • Source mode: {source_mode}
    </div>
    """,
    unsafe_allow_html=True,)