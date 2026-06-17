# app.py
# Run with: streamlit run app.py

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

CHART_TITLE_COLOR = "#ffffff"
CHART_LABEL_COLOR = "#e8eef5"
CHART_TICK_COLOR = "#dbe6f3"
pio.templates.default = "plotly_dark"

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Carbon Budget Tracker – IPCC AR6",
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
    color: #dbe6f3 !important;
    font-size: 0.95rem;
}

.brand-wrap {
    padding: 0.2rem 0 0.8rem 0;
}

.brand-title {
    font-size: 1.45rem;
    font-weight: 850;
    letter-spacing: -0.03em;
    margin-bottom: 0.18rem;
    color: #ffffff !important;
    line-height: 1.15;
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
    color: #ffffff !important;
}

.section-subtitle {
    color: #dbe6f3 !important;
    margin-bottom: 1rem;
}

.insight-box {
    border: 1px solid rgba(25,208,107,0.30);
    border-left: 4px solid var(--green);
    background: linear-gradient(90deg, rgba(25,208,107,0.10), rgba(8,12,18,0.96));
    padding: 1.15rem 1.25rem 1.2rem;
    margin-bottom: 1.1rem;
    box-shadow: var(--shadow);
}

.insight-label {
    color: var(--green);
    font-weight: 800;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

.insight-question {
    color: #ffffff !important;
    font-weight: 850;
    font-size: 1.22rem;
    letter-spacing: -0.02em;
    margin-bottom: 0.55rem;
}

.insight-text {
    color: #dbe6f3 !important;
    line-height: 1.68;
    font-size: 1.02rem;
}

.insight-text b {
    color: #ffffff;
    font-weight: 800;
}

.hero {
    position: relative;
    overflow: hidden;
    background: #05070c;
    border: 1px solid var(--line);
    border-radius: 0;
    padding: 2rem 2.2rem;
    min-height: 300px;
    margin-bottom: 1.15rem;
    box-shadow: var(--shadow);
    color: #ffffff;
}

.hero-earth {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    width: 64%;
    background-position: center center;
    background-size: cover;
    background-repeat: no-repeat;
    transform: scaleX(-1);
    pointer-events: none;
    z-index: 0;
}

.hero-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
        90deg,
        rgba(5,7,12,0.98) 0%,
        rgba(5,7,12,0.9) 36%,
        rgba(5,7,12,0.55) 58%,
        rgba(5,7,12,0.12) 78%,
        rgba(5,7,12,0.02) 100%
    );
    pointer-events: none;
    z-index: 1;
}

.hero-content {
    position: relative;
    z-index: 2;
}

.hero-actions {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-top: 0.35rem;
}

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.35rem 0 1.1rem 0;
    border-bottom: 1px solid var(--line);
    margin-bottom: 1rem;
}

.topbar-title {
    font-size: 1.55rem;
    font-weight: 850;
    letter-spacing: -0.03em;
    white-space: nowrap;
    color: #ffffff !important;
}

.topbar-actions {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-left: auto;
}

.version-tag {
    color: var(--muted);
    border: 1px solid var(--line);
    padding: 0.45rem 0.7rem;
    font-size: 0.78rem;
    letter-spacing: 0.04em;
    white-space: nowrap;
}

.budget-pill {
    display: inline-block;
    color: var(--red);
    border: 1px solid rgba(255, 77, 115, 0.45);
    background: rgba(255, 77, 115, 0.08);
    padding: 0.18rem 0.45rem;
    font-weight: 800;
    font-size: 0.82rem;
}

.climate-warning-card {
    border: 1px solid rgba(25,208,107,0.36);
    background: #080c12;
    min-height: 100%;
    overflow: hidden;
    color: #ffffff !important;
}

.climate-warning-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 1rem 1.1rem 0.8rem;
}

.climate-warning-icon {
    width: 30px;
    height: 30px;
    border-radius: 999px;
    border: 1px solid rgba(25,208,107,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #19d06b;
    font-weight: 900;
    font-size: 1rem;
    line-height: 1;
    flex-shrink: 0;
}

.climate-warning-title {
    font-weight: 850;
    font-size: 1.15rem;
    color: #ffffff !important;
}

.climate-warning-image {
    min-height: 210px;
    background-color: #1a1410;
    background-position: center;
    background-size: cover;
    background-repeat: no-repeat;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 1.5rem 1.2rem;
}

.climate-warning-image-text {
    font-size: 1.15rem;
    font-weight: 800;
    line-height: 1.5;
    max-width: 92%;
    color: #ffffff !important;
    text-shadow: 0 2px 20px rgba(0,0,0,0.9);
}

.climate-warning-body {
    padding: 1rem 1.1rem 1.15rem 1.1rem;
}

.restoration-panel {
    background:
        linear-gradient(180deg, rgba(0,0,0,0.82), rgba(0,0,0,0.72)),
        url('https://images.unsplash.com/photo-1569163139394-de4798aa62b6?auto=format&fit=crop&w=1600&q=80') center/cover no-repeat;
    border: 1px solid var(--line);
    padding: 2rem 2.1rem;
    margin-top: 1rem;
}

.panel-header-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    margin-bottom: 0.85rem;
    color: #ffffff !important;
}

.panel-title {
    font-size: 1.15rem;
    font-weight: 850;
    color: #ffffff !important;
}

.view-all-link {
    color: #2ee58a !important;
    font-weight: 800;
    font-size: 0.95rem;
}

div[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    color: #b8c5d3 !important;
    text-align: left;
    justify-content: flex-start;
    box-shadow: none;
}

div[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: rgba(25,208,107,0.10) !important;
    border: 1px solid rgba(25,208,107,0.30) !important;
    color: #24d07a !important;
    text-align: left;
    justify-content: flex-start;
    box-shadow: inset 3px 0 0 #19d06b;
}

.nav-icon {
    display: inline-block;
    width: 1rem;
    text-align: center;
    opacity: 0.95;
    font-size: 0.92rem;
}

div[data-testid="stSidebar"] .stButton {
    margin-bottom: 0.2rem;
}

div[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 2.7rem;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 3px;
    font-weight: 600;
    font-size: 0.92rem;
    position: relative;
    padding-left: 2.45rem !important;
}

div[data-testid="stSidebar"] .stButton > button::before {
    content: "";
    position: absolute;
    left: 0.9rem;
    top: 50%;
    width: 16px;
    height: 16px;
    transform: translateY(-50%);
    background-color: currentColor;
    opacity: 0.95;
    -webkit-mask: var(--nav-icon) center / contain no-repeat;
    mask: var(--nav-icon) center / contain no-repeat;
}

div[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div:nth-child(2) .stButton > button { --nav-icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='3' width='7' height='7' rx='1'/%3E%3Crect x='14' y='3' width='7' height='7' rx='1'/%3E%3Crect x='14' y='14' width='7' height='7' rx='1'/%3E%3Crect x='3' y='14' width='7' height='7' rx='1'/%3E%3C/svg%3E"); }
div[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div:nth-child(3) .stButton > button { --nav-icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 3h18v18H3z'/%3E%3Cpath d='M3 9h18'/%3E%3Cpath d='M3 15h18'/%3E%3Cpath d='M9 3v18'/%3E%3C/svg%3E"); }
div[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div:nth-child(4) .stButton > button { --nav-icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 3v18h18'/%3E%3Cpath d='M7 16V9'/%3E%3Cpath d='M12 16V5'/%3E%3Cpath d='M17 16v-3'/%3E%3C/svg%3E"); }
div[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div:nth-child(5) .stButton > button { --nav-icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m8 3-4 4 4 4'/%3E%3Cpath d='M4 7h16'/%3E%3Cpath d='m16 21 4-4-4-4'/%3E%3Cpath d='M20 17H4'/%3E%3C/svg%3E"); }
div[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div:nth-child(6) .stButton > button { --nav-icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 3 9.5 8.5 3 9.5 8 14l-2 7 6-3.5L18 21l-2-7 5-4.5-6.5-1z'/%3E%3C/svg%3E"); }
div[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div:nth-child(7) .stButton > button { --nav-icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='3'/%3E%3Cpath d='M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42'/%3E%3C/svg%3E"); }
div[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div:nth-child(8) .stButton > button { --nav-icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 20V10'/%3E%3Cpath d='M18 20V4'/%3E%3Cpath d='M6 20v-4'/%3E%3C/svg%3E"); }

.stButton > button[kind="primary"] {
    background: var(--green);
    color: #04120a;
    border: 1px solid var(--green);
    font-weight: 800;
}

.stButton > button[kind="primary"]:hover {
    background: var(--green-2);
    color: #04120a;
    border-color: var(--green-2);
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
    color: #ffffff !important;
    text-shadow: 0 2px 24px rgba(0,0,0,0.55);
}

.hero-text {
    font-size: 1.12rem;
    color: #e8eef5 !important;
    max-width: 900px;
    line-height: 1.62;
    margin-bottom: 1rem;
}

.metric-card {
    position: relative;
    overflow: hidden;
    background: linear-gradient(180deg, #10141c 0%, #0c1017 100%);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 1.1rem 1.15rem 0.95rem 1.15rem;
    min-height: 148px;
    border-radius: 0;
    box-shadow: none;
    color: #ffffff;
}

.metric-card-clean {
    background: linear-gradient(180deg, #10141c 0%, #0b1017 100%);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: none;
}

.metric-card-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 0.75rem;
    margin-bottom: 0.55rem;
}

.metric-label {
    color: #c9d7e8 !important;
    text-transform: uppercase;
    font-size: 0.78rem;
    letter-spacing: 0.11em;
    font-weight: 700;
    margin-bottom: 0;
    line-height: 1.35;
}

.metric-value {
    font-size: 2.35rem;
    font-weight: 850;
    letter-spacing: -0.04em;
    margin-bottom: 0.25rem;
    color: #ffffff !important;
    line-height: 1;
}

.metric-foot {
    color: #dbe6f3 !important;
    font-size: 0.96rem;
    line-height: 1.45;
}

.metric-icon {
    float: right;
    opacity: 0.45;
    font-size: 1.15rem;
    margin-top: -0.15rem;
}

.metric-icon-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2.35rem;
    height: 2.35rem;
    border-radius: 0.55rem;
    flex-shrink: 0;
}

.metric-icon-clean {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 1.35rem;
    line-height: 1;
    opacity: 0.95;
}

.panel {
    background: linear-gradient(180deg, var(--panel-2) 0%, #0b1017 100%);
    border: 1px solid var(--line);
    padding: 1.2rem;
    border-radius: 0;
    box-shadow: var(--shadow);
    color: #ffffff;
}

.benchmark-card {
    color: #ffffff !important;
}

.bench-stat-value {
    color: #ffffff !important;
    font-weight: 700;
    text-align: right;
}

.budget-progress {
    margin-top: 0.85rem;
    height: 6px;
    background: rgba(255,255,255,0.08);
    border-radius: 999px;
    overflow: hidden;
}

.budget-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #ff4d73, #f7b84b);
    border-radius: 999px;
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
    padding: 0.45rem 0.75rem;
    font-weight: 800;
    margin-bottom: 0.75rem;
}

.driver-bench-bar {
    position: relative;
    height: 5px;
    background: rgba(255,255,255,0.08);
    margin: 0.45rem 0 0.3rem;
    border-radius: 999px;
    overflow: visible;
}

.driver-bench-fill {
    height: 100%;
    border-radius: 999px;
}

.driver-bench-median {
    position: absolute;
    top: -3px;
    width: 2px;
    height: 11px;
    background: rgba(255,255,255,0.85);
    transform: translateX(-1px);
}

.driver-vs-good { color: #5fe0a0 !important; }
.driver-vs-bad { color: #ff8fa8 !important; }
.driver-vs-neutral { color: #c9d7e8 !important; }
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
    color: #d7e4f2 !important;
    font-weight: 800;
    padding: 0.85rem 0.8rem;
    border-bottom: 1px solid var(--line);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-size: 0.80rem;
}

.table-wrap tbody td {
    padding: 0.8rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    color: #f3f7ff !important;
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

.overshoot-alert {
    border: 1px dashed rgba(247, 184, 75, 0.55);
    background: linear-gradient(180deg, rgba(247,184,75,0.06), rgba(8,12,18,0.95));
    min-height: 250px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 1.5rem;
    color: #ffffff !important;
}

.chart-panel-title {
    font-size: 0.95rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #e8eef5 !important;
    margin-bottom: 0.5rem;
}

/* Streamlit contrast overrides */
[data-testid="stMarkdown"] h1,
[data-testid="stMarkdown"] h2,
[data-testid="stMarkdown"] h3,
[data-testid="stMarkdown"] h4,
[data-testid="stMarkdown"] h5,
[data-testid="stMarkdown"] h6,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    color: #ffffff !important;
}

[data-testid="stExpander"] {
    border: 1px solid var(--line);
    background: linear-gradient(180deg, var(--panel-2) 0%, #0b1017 100%);
    border-radius: 0;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] details summary {
    color: #ffffff !important;
    font-weight: 700 !important;
}

div[data-testid="stSidebar"] [data-testid="stExpander"] summary,
div[data-testid="stSidebar"] [data-testid="stExpander"] summary p {
    color: #e8eef5 !important;
}

div[data-testid="stSidebar"] h3,
div[data-testid="stSidebar"] [data-testid="stMarkdown"] h3 {
    color: #ffffff !important;
}

.panel,
.climate-warning-card,
.hero {
    color: #ffffff !important;
}

.panel .panel-title,
.climate-warning-card > div:first-child,
.climate-warning-image > div {
    color: #ffffff !important;
}

.verified-footer {
    border: 1px solid var(--line);
    background: rgba(25,208,107,0.06);
    padding: 0.85rem 1rem;
    margin-top: 1rem;
    font-weight: 700;
    color: var(--green);
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = BASE_DIR / "processed_data"
ASSETS_DIR = BASE_DIR / "assets"


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
def safe_metric_float(value, default=0.0) -> float:
    if value is None or pd.isna(value):
        return default
    return float(value)


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


REGION_ISO = {
    "Europe": {
        "DEU", "FRA", "GBR", "ITA", "ESP", "POL", "NLD", "BEL", "AUT", "CHE", "SWE", "NOR", "DNK", "FIN",
        "IRL", "PRT", "GRC", "CZE", "ROU", "HUN", "UKR", "RUS", "BGR", "SVK", "SVN", "HRV", "LTU", "LVA",
        "EST", "LUX", "ISL",
    },
    "North America": {"USA", "CAN", "MEX", "CRI", "PAN", "GTM", "HND", "NIC", "SLV", "CUB", "JAM", "DOM"},
    "Asia": {
        "CHN", "IND", "JPN", "KOR", "IDN", "PAK", "BGD", "VNM", "THA", "MYS", "SGP", "PHL", "TWN", "HKG",
        "ARE", "SAU", "IRN", "IRQ", "TUR", "KAZ", "UZB", "QAT", "KWT", "ISR", "JOR", "LBN", "OMN", "YEM",
    },
    "Africa": {
        "NGA", "ZAF", "EGY", "KEN", "ETH", "GHA", "TZA", "UGA", "DZA", "MAR", "AGO", "CMR", "CIV", "SEN",
        "ZWE", "MOZ", "TUN", "LBY", "SDN",
    },
    "South America": {"BRA", "ARG", "COL", "CHL", "PER", "VEN", "ECU", "BOL", "PRY", "URY"},
    "Oceania": {"AUS", "NZL", "PNG", "FJI"},
}


def iso_region(iso_code: str) -> str:
    iso = str(iso_code).upper()
    for region, codes in REGION_ISO.items():
        if iso in codes:
            return region
    return "Other"


def add_justice_scores(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    scores = []
    for _, row in df.iterrows():
        pct = row.get("pct_used", np.nan)
        debt_pc = abs(row.get("debt_per_capita", 0)) if pd.notna(row.get("debt_per_capita")) else 0
        debt_gt = row.get("debt_gt", 0)
        overshoot_years = (2024 - row["overshoot_year"]) if pd.notna(row.get("overshoot_year")) else 0

        if pd.isna(pct):
            scores.append(np.nan)
            continue

        if debt_gt < 0:
            score = min(100, 80 + min(abs(debt_gt), 80))
        else:
            budget_component = max(0, 100 - max(0, pct - 100) * 0.35) if pct > 100 else max(60, 100 - pct * 0.4)
            debt_component = max(0, 100 - min(debt_pc, 400) / 4)
            duration_component = max(0, 100 - overshoot_years * 1.1) if overshoot_years > 0 else 100
            score = 0.45 * budget_component + 0.35 * debt_component + 0.20 * duration_component

        scores.append(round(max(0, min(100, score)), 1))
    df["justice_score"] = scores
    return df


def sector_driver_scores(row, hist: pd.DataFrame) -> pd.DataFrame:
    latest = hist.iloc[-1] if len(hist) else None
    fossil_share = row.get("renewables_share_energy", np.nan)
    fossil_share = (100 - fossil_share) if pd.notna(fossil_share) else np.nan
    co2pc = row.get("co2_per_capita", latest["co2_per_capita"] if latest is not None and "co2_per_capita" in latest else np.nan)
    ind_age = row.get("industrialization_age", np.nan)
    energy = latest["primary_energy_consumption"] if latest is not None and "primary_energy_consumption" in latest else np.nan
    population = latest["population"] if latest is not None and "population" in latest else np.nan

    drivers = {
        "Coal": fossil_share * 0.95 if pd.notna(fossil_share) else 45,
        "Industry": min(100, ind_age / 2.4) if pd.notna(ind_age) else 40,
        "Transport": min(100, co2pc * 9) if pd.notna(co2pc) else 35,
        "Electricity": min(100, energy / 80) if pd.notna(energy) else 30,
        "Population": min(100, np.log10(population) * 14) if pd.notna(population) and population > 0 else 25,
    }
    out = pd.DataFrame({"Driver": list(drivers.keys()), "Score": list(drivers.values())})
    return out.sort_values("Score", ascending=True)


def normalize_ai_scenario_table(df: pd.DataFrame, row=None) -> pd.DataFrame:
    rename_map = {
        "Scenario": "scenario",
        "overshoot year": "overshoot_year",
        "overshoot_year_ai": "overshoot_year",
        "overshoot_year_aiaware": "overshoot_year",
        "carbon_debt_gt": "debt_gt",
        "projected_debt_gt": "debt_gt",
    }
    df = df.rename(columns={c: rename_map.get(c, c) for c in df.columns}).copy()
    if "scenario" not in df.columns:
        return pd.DataFrame()

    if "year" in df.columns and "debt_gt" in df.columns:
        df = df.sort_values("year").groupby("scenario", as_index=False).tail(1)

    keep = [c for c in ["scenario", "overshoot_year", "debt_gt"] if c in df.columns]
    df = df[keep].copy()

    if "overshoot_year" not in df.columns and row is not None and pd.notna(row.get("overshoot_year")):
        base_year = int(row["overshoot_year"])
        offsets = {"baseline": 0, "ai +10%": -2, "ai +25%": -5, "ai +50%": -8}
        df["overshoot_year"] = df["scenario"].astype(str).str.lower().map(
            lambda s: next((max(1990, base_year + off) for key, off in offsets.items() if key in s), base_year)
        )

    if "debt_gt" in df.columns:
        df["debt_gt"] = pd.to_numeric(df["debt_gt"], errors="coerce")
    if "overshoot_year" in df.columns:
        df["overshoot_year"] = pd.to_numeric(df["overshoot_year"], errors="coerce")

    df = df.drop_duplicates(subset=["scenario"])
    if "debt_gt" not in df.columns or "overshoot_year" not in df.columns:
        return pd.DataFrame()
    if df["debt_gt"].isna().all() or df["overshoot_year"].isna().all():
        return pd.DataFrame()
    return df


def get_driver_context_metrics(row, summary_df: pd.DataFrame):
    pct = float(row.get("pct_used")) if pd.notna(row.get("pct_used")) else np.nan
    fossil = (100 - float(row["renewables_share_energy"])) if pd.notna(row.get("renewables_share_energy")) else np.nan
    co2 = float(row.get("co2_per_capita")) if pd.notna(row.get("co2_per_capita")) else np.nan
    ind_age = float(row.get("industrialization_age")) if pd.notna(row.get("industrialization_age")) else np.nan

    global_pct = summary_df["pct_used"].median(skipna=True)
    global_fossil = (100 - summary_df["renewables_share_energy"]).median(skipna=True)
    global_co2 = summary_df["co2_per_capita"].median(skipna=True)
    global_ind = summary_df["industrialization_age"].median(skipna=True)

    caps = {"Budget Used": 250, "Fossil Share": 100}

    def vs_global(value, benchmark, higher_is_worse=True):
        if pd.isna(value) or pd.isna(benchmark):
            return "—", "neutral"
        diff = value - benchmark
        if abs(diff) < 0.05 * max(abs(benchmark), 1):
            return "Near global median", "neutral"
        direction = "above" if diff > 0 else "below"
        is_worse = (diff > 0) == higher_is_worse
        tone = "bad" if is_worse else "good"
        return f"{abs(diff):,.1f} {direction} global median", tone

    def bar_widths(value, benchmark, label):
        cap = caps.get(label) or max(value, benchmark, 1) * 1.2
        return min(100, value / cap * 100), min(100, benchmark / cap * 100)

    specs = [
        ("Budget Used", pct, global_pct, safe_metric_value(pct, "%", digits=0), True, "#ff4d73"),
        ("Fossil Share", fossil, global_fossil, safe_metric_value(fossil, "%", digits=1), True, "#f7b84b"),
        ("CO₂ per Capita", co2, global_co2, safe_metric_value(co2, " t", digits=2), True, "#ff4d73"),
        ("Industrialization Age", ind_age, global_ind, safe_metric_value(ind_age, " yrs", digits=0), False, "#dbe6f3"),
    ]
    metrics = []
    for label, value, benchmark, display, higher_is_worse, value_color in specs:
        vs_text, tone = vs_global(value, benchmark, higher_is_worse)
        fill_w, median_w = bar_widths(value, benchmark, label)
        metrics.append({
            "label": label,
            "display": display,
            "value_color": value_color,
            "vs_global": vs_text,
            "tone": tone,
            "fill_width": fill_w,
            "median_width": median_w,
        })
    return metrics


DRIVER_ARCHETYPE_OVERRIDES = {
    "Germany": "Industrial Legacy Economy",
    "Saudi Arabia": "Fossil Export Economy",
    "Poland": "Coal Intensive Economy",
    "China": "Rapid Industrial Expansion",
    "India": "Population-Scale Development Economy",
    "United States": "Industrial Legacy Economy",
    "United Kingdom": "Industrial Legacy Economy",
    "Japan": "Industrial Legacy Economy",
    "Australia": "Fossil Export Economy",
    "Norway": "Fossil Export Economy",
    "United Arab Emirates": "Fossil Export Economy",
    "Qatar": "Fossil Export Economy",
    "Kuwait": "Fossil Export Economy",
    "Russia": "Fossil Export Economy",
    "Indonesia": "Population-Scale Development Economy",
    "Brazil": "Population-Scale Development Economy",
    "Nigeria": "Population-Scale Development Economy",
}


def infer_driver_archetype(row) -> str:
    country = row.get("country")
    if country in DRIVER_ARCHETYPE_OVERRIDES:
        return DRIVER_ARCHETYPE_OVERRIDES[country]

    renew = row.get("renewables_share_energy")
    fossil = (100 - float(renew)) if pd.notna(renew) else np.nan
    ind_age = row.get("industrialization_age")
    co2_pc = row.get("co2_per_capita")
    pct = row.get("pct_used")

    if pd.notna(fossil) and fossil > 88 and pd.notna(co2_pc) and co2_pc > 12:
        return "Fossil Export Economy"
    if pd.notna(fossil) and fossil > 82 and pd.notna(ind_age) and ind_age > 200:
        return "Coal Intensive Economy"
    if pd.notna(ind_age) and ind_age > 210:
        return "Industrial Legacy Economy"
    if pd.notna(ind_age) and ind_age < 130 and pd.notna(pct) and pct > 90:
        return "Rapid Industrial Expansion"
    if pd.notna(co2_pc) and co2_pc < 3.5:
        return "Population-Scale Development Economy"
    if pd.notna(renew) and renew > 40:
        return "Clean-Energy Transition Economy"
    return "Fossil-Dependent Economy"


def driver_phrase(name: str) -> str:
    return {
        "Population": "population pressure",
        "Industry": "industry",
        "Coal": "coal use",
        "Transport": "transport emissions",
        "Electricity": "electricity demand",
    }.get(name, name.lower())


def format_driver_list(driver_names: list) -> str:
    phrases = [driver_phrase(d) for d in driver_names]
    if not phrases:
        return "multiple structural drivers"
    if len(phrases) == 1:
        return phrases[0]
    if len(phrases) == 2:
        return f"{phrases[0]} and {phrases[1]}"
    return f"{', '.join(phrases[:-1])}, and {phrases[-1]}"


def legacy_industrial_driver_text(drivers_df: pd.DataFrame) -> str:
    ranked = drivers_df.sort_values("Score", ascending=False)["Driver"].tolist()
    primary = [d for d in ["Industry", "Coal", "Transport", "Electricity"] if d in ranked][:2]
    if len(primary) < 2:
        primary = [d for d in ranked if d != "Population"][:2]
    primary_text = format_driver_list(primary)
    reinforce = "transport emissions" if "Transport" in ranked else driver_phrase(ranked[1] if len(ranked) > 1 else "")
    return primary_text, reinforce


def build_driver_interpretation(row, archetype: str, drivers_df: pd.DataFrame) -> str:
    country = row.get("country", "This country")
    top_drivers = drivers_df.sort_values("Score", ascending=False).head(3)["Driver"].tolist()
    driver_text = format_driver_list(top_drivers)

    if country == "Germany":
        return (
            f"{country}'s overshoot is primarily associated with its long industrial history, "
            f"high cumulative emissions, and historical dependence on fossil fuels. "
            f"Industrial activity and coal use emerge as the strongest structural contributors, "
            f"while transport emissions further reinforce overshoot dynamics."
        )

    if archetype == "Industrial Legacy Economy":
        primary_text, reinforce = legacy_industrial_driver_text(drivers_df)
        reinforce_clause = (
            f", while {reinforce} further reinforce overshoot dynamics"
            if reinforce and reinforce not in primary_text
            else ""
        )
        return (
            f"{country}'s overshoot is primarily associated with its long industrial history, "
            f"high cumulative emissions, and historical dependence on fossil fuels. "
            f"{primary_text.capitalize()} emerge as the strongest structural contributors"
            f"{reinforce_clause}."
        )

    archetype_templates = {
        "Fossil Export Economy": (
            f"{country}'s overshoot is closely tied to an export-oriented fossil fuel economy, "
            f"high per-capita emissions, and limited renewable penetration. {driver_text.capitalize()} "
            f"are the leading structural pressures behind its fair-share budget breach."
        ),
        "Coal Intensive Economy": (
            f"{country}'s carbon debt reflects a coal-heavy energy system and long-standing "
            f"industrial emissions. {driver_text.capitalize()} dominate the overshoot profile, "
            f"with coal dependence remaining a central constraint on Paris-aligned pathways."
        ),
        "Rapid Industrial Expansion": (
            f"{country}'s overshoot is driven by rapid industrialisation, rising energy demand, "
            f"and fast accumulation of cumulative emissions. {driver_text.capitalize()} stand out "
            f"as the primary structural contributors."
        ),
        "Population-Scale Development Economy": (
            f"{country}'s emissions profile is shaped by large-scale development needs, population "
            f"pressure, and expanding energy access. {driver_text.capitalize()} are the most "
            f"important drivers, even where per-capita emissions remain comparatively moderate."
        ),
        "Clean-Energy Transition Economy": (
            f"{country}'s overshoot reflects historical emissions accumulated before recent "
            f"renewables expansion. {driver_text.capitalize()} explain most of the remaining "
            f"fair-share gap despite improving clean-energy momentum."
        ),
    }

    if archetype in archetype_templates:
        return archetype_templates[archetype]

    return (
        f"{country}'s carbon debt is primarily associated with its {archetype.lower()} emissions "
        f"profile and structural dependence on high-carbon activity. {driver_text.capitalize()} "
        f"emerge as the dominant contributors to its fair-share overshoot."
    )


def build_driver_comparative_narrative(row, summary_df: pd.DataFrame) -> str:
    country = row.get("country", "This country")
    renew = row.get("renewables_share_energy")
    fossil = (100 - float(renew)) if pd.notna(renew) else np.nan
    ind_age = float(row.get("industrialization_age")) if pd.notna(row.get("industrialization_age")) else np.nan
    co2 = float(row.get("co2_per_capita")) if pd.notna(row.get("co2_per_capita")) else np.nan

    global_fossil = (100 - summary_df["renewables_share_energy"]).median(skipna=True)
    global_ind = summary_df["industrialization_age"].median(skipna=True)
    global_co2 = summary_df["co2_per_capita"].median(skipna=True)

    fossil_high = pd.notna(fossil) and pd.notna(global_fossil) and fossil > global_fossil * 1.03
    ind_high = pd.notna(ind_age) and pd.notna(global_ind) and ind_age > global_ind * 1.08
    co2_high = pd.notna(co2) and pd.notna(global_co2) and co2 > global_co2 * 1.08

    if country == "Germany":
        return (
            f"{country}'s overshoot appears more strongly linked to historical industrial emissions "
            f"than to unusually high current fossil dependence."
        )
    if ind_high and not fossil_high:
        return (
            f"{country}'s overshoot appears more strongly linked to historical industrial emissions "
            f"than to unusually high current fossil dependence."
        )
    if fossil_high and ind_high:
        return (
            f"{country}'s overshoot reflects both a long industrial history and persistently high "
            f"fossil dependence relative to global peers."
        )
    if fossil_high:
        return (
            f"{country}'s overshoot is closely tied to above-median fossil fuel dependence in the "
            f"current energy mix."
        )
    if co2_high:
        return (
            f"{country}'s overshoot is driven more by high current emissions intensity than by "
            f"population scale alone."
        )
    return (
        f"{country}'s driver profile sits near or below global medians on several structural "
        f"indicators, suggesting overshoot is shaped by cumulative historical emissions rather "
        f"than a single extreme current factor."
    )


def build_driver_policy_relevance(row, archetype: str) -> str:
    country = row.get("country", "This country")

    if country == "Germany":
        return (
            f"Because {country}'s overshoot is driven largely by accumulated historical emissions, "
            f"future mitigation alone may not eliminate its carbon debt. Long-term decarbonisation "
            f"and carbon-removal strategies are likely to play an increasingly important role in "
            f"reducing overshoot."
        )

    policy_templates = {
        "Fossil Export Economy": (
            f"For {country}, reducing overshoot will require diversifying away from fossil-export "
            f"dependence while managing the economic transition of hydrocarbon-intensive sectors. "
            f"Carbon pricing, export diversification, and clean-energy investment are likely to be "
            f"central policy levers."
        ),
        "Coal Intensive Economy": (
            f"{country}'s policy challenge centres on coal phase-out, industrial decarbonisation, "
            f"and retrofitting legacy infrastructure. Without accelerated coal retirement, fair-share "
            f"recovery is likely to remain out of reach."
        ),
        "Rapid Industrial Expansion": (
            f"{country} must align new industrial capacity with low-carbon standards before emissions "
            f"lock in further. Early investment in clean electricity and efficiency can reduce the "
            f"long-term cost of reversing overshoot."
        ),
        "Population-Scale Development Economy": (
            f"{country}'s pathway depends on meeting development needs through low-carbon energy "
            f"expansion rather than fossil-intensive growth. Fair-share outcomes will hinge on "
            f"clean electrification, urban planning, and equitable access policies."
        ),
        "Clean-Energy Transition Economy": (
            f"{country} is already shifting toward renewables, but historical debt may require "
            f"complementary drawdown or removal measures. Policy should focus on finishing the "
            f"transition while addressing legacy emissions."
        ),
    }

    if archetype in policy_templates:
        return policy_templates[archetype]

    return (
        f"Because {country}'s overshoot is structurally entrenched, incremental efficiency gains "
        f"alone are unlikely to restore a Paris-compatible pathway. A combination of accelerated "
        f"mitigation, sectoral transition, and long-term carbon management will be needed."
    )


DRIVER_SUMMARY_BY_ARCHETYPE = {
    "Industrial Legacy Economy": {
        "primary": "Industrial Legacy",
        "secondary": "Coal Dependence",
        "risk": "Historical Emissions Lock-In",
    },
    "Fossil Export Economy": {
        "primary": "Fossil Export Dependence",
        "secondary": "High Per-Capita Emissions",
        "risk": "Hydrocarbon Revenue Lock-In",
    },
    "Coal Intensive Economy": {
        "primary": "Coal Dependence",
        "secondary": "Industrial Activity",
        "risk": "Coal Infrastructure Lock-In",
    },
    "Rapid Industrial Expansion": {
        "primary": "Rapid Industrialisation",
        "secondary": "Rising Energy Demand",
        "risk": "Emissions Growth Lock-In",
    },
    "Population-Scale Development Economy": {
        "primary": "Development-Scale Growth",
        "secondary": "Population Pressure",
        "risk": "Rising Demand Trajectory",
    },
    "Clean-Energy Transition Economy": {
        "primary": "Legacy Fossil Dependence",
        "secondary": "Historical Emissions",
        "risk": "Transition Lag Risk",
    },
    "Fossil-Dependent Economy": {
        "primary": "Fossil Fuel Dependence",
        "secondary": "Energy-Intensive Activity",
        "risk": "Structural Emissions Lock-In",
    },
}

DRIVER_SUMMARY_SECONDARY = {
    "Coal": "Coal Dependence",
    "Industry": "Industrial Activity",
    "Transport": "Transport Emissions",
    "Electricity": "Electricity Demand",
    "Population": "Population Pressure",
}

COUNTRY_DRIVER_SUMMARY_OVERRIDES = {
    "Germany": {
        "primary": "Industrial Legacy",
        "secondary": "Coal Dependence",
        "risk": "Historical Emissions Lock-In",
    },
}


def build_driver_summary(row, archetype: str, drivers_df: pd.DataFrame) -> dict:
    country = row.get("country")
    if country in COUNTRY_DRIVER_SUMMARY_OVERRIDES:
        return COUNTRY_DRIVER_SUMMARY_OVERRIDES[country]

    summary = DRIVER_SUMMARY_BY_ARCHETYPE.get(
        archetype,
        {
            "primary": archetype.replace(" Economy", ""),
            "secondary": "Fossil Dependence",
            "risk": "Structural Emissions Lock-In",
        },
    ).copy()

    ranked = drivers_df.sort_values("Score", ascending=False)["Driver"].tolist()
    if archetype == "Industrial Legacy Economy":
        for driver in ["Coal", "Transport", "Electricity"]:
            if driver in ranked:
                summary["secondary"] = DRIVER_SUMMARY_SECONDARY[driver]
                break
    elif len(ranked) > 1:
        secondary_driver = ranked[1] if ranked[0] == "Population" and len(ranked) > 2 else ranked[1]
        summary["secondary"] = DRIVER_SUMMARY_SECONDARY.get(secondary_driver, summary["secondary"])
    elif ranked:
        summary["secondary"] = DRIVER_SUMMARY_SECONDARY.get(ranked[0], summary["secondary"])

    return summary


def render_driver_summary_card(summary: dict):
    st.html(
        f"""
        <div class="panel" style="margin-bottom:0.85rem;padding:1rem 1.1rem;">
            <div class="metric-label">Driver Summary</div>
            <div style="margin-top:0.8rem;display:grid;gap:0.55rem;">
                <div style="color:#dbe6f3;font-size:1rem;line-height:1.5;">
                    <span style="color:#8f9baa;font-weight:600;">Primary Driver:</span>
                    <span style="color:#ffffff;font-weight:800;margin-left:0.35rem;">{summary['primary']}</span>
                </div>
                <div style="color:#dbe6f3;font-size:1rem;line-height:1.5;">
                    <span style="color:#8f9baa;font-weight:600;">Secondary Driver:</span>
                    <span style="color:#ffffff;font-weight:800;margin-left:0.35rem;">{summary['secondary']}</span>
                </div>
                <div style="color:#dbe6f3;font-size:1rem;line-height:1.5;">
                    <span style="color:#8f9baa;font-weight:600;">Risk Pattern:</span>
                    <span style="color:#ffffff;font-weight:800;margin-left:0.35rem;">{summary['risk']}</span>
                </div>
            </div>
        </div>
        """
    )


def render_driver_archetype_box(archetype: str):
    st.html(
        f"""
        <div class="panel" style="margin-top:0.35rem;margin-bottom:0.85rem;">
            <div class="metric-label">Driver Archetype</div>
            <div style="font-size:1.75rem;font-weight:850;color:#ffffff;margin-top:0.35rem;letter-spacing:-0.02em;">
                {archetype}
            </div>
        </div>
        """
    )


def render_driver_comparative_context(row, summary_df: pd.DataFrame):
    country = row.get("country", "Country")
    pct = float(row.get("pct_used")) if pd.notna(row.get("pct_used")) else np.nan
    renew = row.get("renewables_share_energy")
    fossil = (100 - float(renew)) if pd.notna(renew) else np.nan
    co2 = float(row.get("co2_per_capita")) if pd.notna(row.get("co2_per_capita")) else np.nan
    ind_age = float(row.get("industrialization_age")) if pd.notna(row.get("industrialization_age")) else np.nan

    global_pct = summary_df["pct_used"].median(skipna=True)
    global_fossil = (100 - summary_df["renewables_share_energy"]).median(skipna=True)
    global_co2 = summary_df["co2_per_capita"].median(skipna=True)
    global_ind = summary_df["industrialization_age"].median(skipna=True)

    rows = [
        ("Budget Used", safe_metric_value(pct, "%", digits=0), safe_metric_value(global_pct, "%", digits=0)),
        ("CO₂ per Capita", safe_metric_value(co2, " t", digits=1), safe_metric_value(global_co2, " t", digits=1)),
        ("Fossil Share", safe_metric_value(fossil, "%", digits=0), safe_metric_value(global_fossil, "%", digits=0)),
        ("Industrialization Age", safe_metric_value(ind_age, " yrs", digits=0), safe_metric_value(global_ind, " yrs", digits=0)),
    ]
    body = "".join(
        f"<tr>"
        f"<td style='color:#8f9baa;font-weight:600;'>{label}</td>"
        f"<td style='color:#ffffff;font-weight:800;'>{country_val}</td>"
        f"<td style='color:#dbe6f3;font-weight:700;'>{median_val}</td>"
        f"</tr>"
        for label, country_val, median_val in rows
    )
    narrative = build_driver_comparative_narrative(row, summary_df)

    st.html(
        f"""
        <div class="insight-box" style="margin-top:0.85rem;border-left-color: var(--amber);
            border-color: rgba(247,184,75,0.28);
            background: linear-gradient(90deg, rgba(247,184,75,0.08), rgba(8,12,18,0.96));">
            <div class="insight-label" style="color: var(--amber);">Comparative Context</div>
            <div class="table-wrap" style="margin:0.75rem 0 0.9rem;">
                <table>
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>{country}</th>
                            <th>Global Median</th>
                        </tr>
                    </thead>
                    <tbody>{body}</tbody>
                </table>
            </div>
            <div class="insight-text">{narrative}</div>
        </div>
        """
    )


def render_driver_policy_relevance_box(insight_html: str):
    st.html(
        f"""
        <div class="insight-box" style="margin-top:0.85rem;border-left-color: var(--green);
            border-color: rgba(25,208,107,0.28);
            background: linear-gradient(90deg, rgba(25,208,107,0.08), rgba(8,12,18,0.96));">
            <div class="insight-label">Policy Relevance</div>
            <div class="insight-text">{insight_html}</div>
        </div>
        """
    )


def render_driver_context_panel(row, summary_df: pd.DataFrame):
    country = row.get("country", "Country")
    metrics = get_driver_context_metrics(row, summary_df)
    rows_html = "".join(
        f"<tr>"
        f"<td style='color:#dbe6f3;font-weight:700;'>{m['label']}</td>"
        f"<td style='color:{m['value_color']};font-weight:800;white-space:nowrap;'>{m['display']}</td>"
        f"<td>"
        f"<div class='driver-bench-bar'>"
        f"<div class='driver-bench-fill' style='width:{m['fill_width']:.1f}%;background:{m['value_color']};'></div>"
        f"<div class='driver-bench-median' style='left:{m['median_width']:.1f}%;'></div>"
        f"</div>"
        f"<div class='driver-vs-{m['tone']}' style='font-size:0.88rem;'>{m['vs_global']}</div>"
        f"</td>"
        f"</tr>"
        for m in metrics
    )
    st.html(
        f"""
        <div class="panel" style="margin-top:0.75rem;">
            <div class="panel-title">Driver context</div>
            <div class="small-muted" style="margin-bottom:0.85rem;">
                Structural indicators for {country} against the global median.
            </div>
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>Indicator</th>
                            <th>Value</th>
                            <th>Vs global median</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
        </div>
        """
    )


def format_ai_scenario_display(df: pd.DataFrame) -> pd.DataFrame:
    labels = {
        "scenario": "Scenario",
        "overshoot_year": "Overshoot Year",
        "debt_gt": "Carbon Debt (Gt)",
    }
    cols = [c for c in labels if c in df.columns]
    out = df[cols].copy()
    out.columns = [labels[c] for c in cols]
    if "Overshoot Year" in out.columns:
        out["Overshoot Year"] = out["Overshoot Year"].map(lambda x: f"{int(x)}" if pd.notna(x) else "—")
    if "Carbon Debt (Gt)" in out.columns:
        out["Carbon Debt (Gt)"] = out["Carbon Debt (Gt)"].map(lambda x: f"{x:.2f}" if pd.notna(x) else "—")
    return out


def enrich_pledge_from_scenarios(summary: pd.DataFrame, scenarios: pd.DataFrame) -> pd.DataFrame:
    if scenarios is None or scenarios.empty or "pledge_year" not in scenarios.columns:
        return summary

    summary = summary.copy()
    pledge_map = scenarios.groupby("iso_code")["pledge_year"].first()
    pledge_map.index = pledge_map.index.astype(str).str.upper().str.strip()
    scenario_pledge = summary["iso_code"].map(pledge_map)
    scenario_pledge = pd.to_numeric(scenario_pledge, errors="coerce")

    summary["pledge_year_final"] = pd.to_numeric(summary["pledge_year_final"], errors="coerce")
    summary.loc[summary["pledge_year_final"].isna(), "pledge_year_final"] = scenario_pledge

    placeholder_mask = (summary["pledge_year_final"] == 2020) & scenario_pledge.notna() & (scenario_pledge > 2020)
    summary.loc[placeholder_mask, "pledge_year_final"] = scenario_pledge[placeholder_mask]

    gap_mask = summary["overshoot_year"].notna() & summary["pledge_year_final"].notna()
    summary.loc[gap_mask, "pledge_gap_years"] = (
        summary.loc[gap_mask, "pledge_year_final"] - summary.loc[gap_mask, "overshoot_year"]
    )
    return summary


def build_policy_gap_dumbbell(gap_df: pd.DataFrame):
    plot_df = (
        gap_df.dropna(subset=["overshoot_year", "net_zero_year", "policy_gap_years"])
        .sort_values("policy_gap_years", ascending=True)
        .tail(20)
        .copy()
    )
    fig = go.Figure()
    for _, row in plot_df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["overshoot_year"], row["net_zero_year"]],
            y=[row["country"], row["country"]],
            mode="lines+markers",
            line=dict(color="rgba(255,255,255,0.28)", width=3),
            marker=dict(size=10, color=["#ff4d73", "#24d07a"]),
            showlegend=False,
            hovertemplate=(
                f"{row['country']}<br>"
                f"Overshoot: {int(row['overshoot_year'])}<br>"
                f"Pledge: {int(row['net_zero_year'])}<br>"
                f"Gap: {int(row['policy_gap_years'])} yrs<br>"
                f"Debt: {row['debt_gt']:.1f} Gt<extra></extra>"
            ),
        ))
    apply_chart_layout(
        fig,
        height=560,
        title="Overshoot year → net-zero pledge",
        xaxis_title="Year",
        yaxis=dict(categoryorder="total ascending"),
    )
    return fig


def prepare_policy_gap_df(summary: pd.DataFrame) -> pd.DataFrame:
    gap_df = summary.copy()
    gap_df["net_zero_year"] = pd.to_numeric(gap_df["pledge_year_final"], errors="coerce")
    gap_df["policy_gap_years"] = pd.to_numeric(gap_df["pledge_gap_years"], errors="coerce")
    gap_mask = gap_df["net_zero_year"].notna() & gap_df["overshoot_year"].notna()
    gap_df.loc[gap_mask, "policy_gap_years"] = (
        gap_df.loc[gap_mask, "net_zero_year"] - gap_df.loc[gap_mask, "overshoot_year"]
    )
    return gap_df


def format_overshoot_year(row) -> str:
    debt = row.get("debt_gt")
    pct = row.get("pct_used")
    overshoot = row.get("overshoot_year")
    if pd.isna(overshoot) or (pd.notna(debt) and debt <= 0) or (pd.notna(pct) and pct <= 100):
        return "Not Overshot"
    return str(int(overshoot))


def policy_gap_severity(gap_years):
    if pd.isna(gap_years):
        return "N/A", "#8f9baa"
    gap = float(gap_years)
    if gap < 0:
        return "Ahead of overshoot", "#24d07a"
    if gap <= 10:
        return "Low Gap", "#24d07a"
    if gap <= 25:
        return "Moderate Gap", "#6bcf9a"
    if gap <= 40:
        return "High Gap", "#f7b84b"
    return "Extreme Gap", "#ff4d73"


def policy_gap_severity_for_row(row):
    debt = row.get("debt_gt")
    if pd.notna(debt) and debt <= 0:
        return "Within fair share", "#24d07a"
    return policy_gap_severity(country_policy_gap(row))


def build_policy_gap_quadrant_plot(df: pd.DataFrame, x_thresh: float = 25):
    plot_df = df.dropna(subset=["policy_gap_years", "debt_gt"]).copy()
    if plot_df.empty:
        return None

    x_max = max(float(plot_df["policy_gap_years"].max()) * 1.08, x_thresh * 2)
    x_min = min(float(plot_df["policy_gap_years"].min()) * 1.08, -5)
    y_max = max(float(plot_df["debt_gt"].max()) * 1.08, 10)
    y_min = min(float(plot_df["debt_gt"].min()) * 1.08, -10)
    y_thresh = 0.0

    fig = go.Figure()
    quadrants = [
        (x_thresh, x_max, y_thresh, y_max, "rgba(255,77,115,0.10)", 0.72, 0.82, "High Debt + High Gap<br><b>Highest concern</b>"),
        (x_min, x_thresh, y_thresh, y_max, "rgba(247,184,75,0.08)", 0.28, 0.82, "High Debt + Low Gap<br><b>Strong mitigation</b>"),
        (x_thresh, x_max, y_min, y_thresh, "rgba(247,184,75,0.08)", 0.72, 0.18, "Low Debt + High Gap<br><b>Future risk</b>"),
        (x_min, x_thresh, y_min, y_thresh, "rgba(36,208,122,0.10)", 0.28, 0.18, "Low Debt + Low Gap<br><b>Paris-aligned</b>"),
    ]
    for x0, x1, y0, y1, fill, ax_pct, ay_pct, label in quadrants:
        fig.add_shape(
            type="rect", x0=x0, x1=x1, y0=y0, y1=y1,
            fillcolor=fill, line=dict(width=0), layer="below",
        )
        fig.add_annotation(
            x=x0 + (x1 - x0) * ax_pct,
            y=y0 + (y1 - y0) * ay_pct,
            text=label,
            showarrow=False,
            font=dict(size=10, color="rgba(255,255,255,0.62)"),
            align="center",
        )

    marker_colors = plot_df["justice_score"].fillna(50) if "justice_score" in plot_df.columns else 50
    fig.add_trace(go.Scatter(
        x=plot_df["policy_gap_years"],
        y=plot_df["debt_gt"],
        mode="markers",
        text=plot_df["country"],
        marker=dict(
            size=11,
            color=marker_colors,
            colorscale="RdYlGn",
            cmin=0,
            cmax=100,
            showscale=True,
            colorbar=dict(title="Justice"),
            line=dict(width=0.5, color="rgba(255,255,255,0.35)"),
        ),
        hovertemplate="%{text}<br>Gap: %{x:.0f} yrs<br>Debt: %{y:.1f} Gt<extra></extra>",
    ))
    fig.add_vline(x=x_thresh, line_dash="dash", line_color="rgba(255,255,255,0.28)")
    fig.add_hline(y=y_thresh, line_dash="dash", line_color="rgba(255,255,255,0.28)")
    apply_chart_layout(
        fig,
        height=520,
        title="Policy gap vs carbon debt",
        xaxis_title="Policy gap (years)",
        yaxis_title="Carbon debt (Gt)",
    )
    return fig


def build_policy_interpretation(row) -> str:
    country = row.get("country", "This country")
    debt = row.get("debt_gt")
    overshoot = row.get("overshoot_year")
    net_zero = row.get("pledge_year_final")
    gap = country_policy_gap(row)
    severity, _ = policy_gap_severity_for_row(row)

    if pd.notna(debt) and debt <= 0:
        return (
            f"{country} remains within its fair-share allocation and therefore does not exhibit "
            f"a historical overshoot gap under the current methodology. Future development pathways "
            f"will determine whether this position is maintained."
        )

    if country == "United States":
        gap_text = f"approximately <b>{int(gap)} years</b>" if pd.notna(gap) else "one of the largest globally"
        debt_text = f"<b>{debt:.0f} Gt</b>" if pd.notna(debt) else "the largest globally"
        return (
            f"The United States exhibits the largest carbon debt globally ({debt_text}) and maintains "
            f"one of the largest policy gaps ({gap_text}). Its current net-zero timeline implies a "
            f"prolonged period between overshoot and climate neutrality, increasing reliance on future "
            f"mitigation measures. Severity: <b>{severity}</b>."
        )

    if country == "Germany":
        nz = int(net_zero) if pd.notna(net_zero) else "—"
        gap_int = int(gap) if pd.notna(gap) else "—"
        oy = int(overshoot) if pd.notna(overshoot) else "—"
        return (
            f"Germany exhausted its fair-share carbon budget around <b>{oy}</b> but plans to reach "
            f"climate neutrality in <b>{nz}</b>. This creates a policy gap of approximately "
            f"<b>{gap_int} years</b>. While Germany has reduced emissions substantially and expanded "
            f"renewable energy deployment, its historical emissions remain significantly above its "
            f"allocated fair-share budget. Closing this gap would require accelerated decarbonization "
            f"and/or large-scale carbon drawdown efforts. Severity: <b>{severity}</b>."
        )

    if pd.isna(overshoot) or pd.isna(gap):
        return (
            f"{country}'s policy gap cannot be fully assessed with the available pledge and overshoot data."
        )

    oy = int(overshoot)
    nz = int(net_zero) if pd.notna(net_zero) else "—"
    gap_int = int(gap)
    debt_line = f" Carbon debt stands at <b>{debt:.1f} Gt</b>." if pd.notna(debt) and debt > 0 else ""
    return (
        f"{country} exhausted its fair-share carbon budget around <b>{oy}</b> and targets climate "
        f"neutrality by <b>{nz}</b>, yielding a policy gap of <b>{gap_int} years</b> "
        f"({severity}).{debt_line} Closing this gap depends on accelerated mitigation, carbon "
        f"removals, or sustained emissions cuts through the net-zero horizon."
    )


def render_policy_comparison_table(summary: pd.DataFrame, country_names: list):
    rows = []
    for name in country_names:
        match = summary[summary["country"] == name]
        if len(match):
            rows.append(match.iloc[0])
    if not rows:
        st.info("Select at least one country to compare.")
        return

    headers = "".join(f"<th>{r['country']}</th>" for r in rows)

    def cell(value_fn):
        return "".join(f"<td>{value_fn(r)}</td>" for r in rows)

    metric_rows = [
        ("Carbon Debt", lambda r: f"{r['debt_gt']:.1f} Gt" if pd.notna(r.get("debt_gt")) else "—"),
        ("Overshoot Year", format_overshoot_year),
        ("Net Zero Target", lambda r: str(int(r["pledge_year_final"])) if pd.notna(r.get("pledge_year_final")) else "—"),
        ("Budget Used", lambda r: f"{int(round(r['pct_used']))}%" if pd.notna(r.get("pct_used")) else "—"),
        ("Justice Score", lambda r: f"{int(round(r['justice_score']))}" if pd.notna(r.get("justice_score")) else "—"),
        ("Gap Severity", lambda r: policy_gap_severity_for_row(r)[0]),
    ]
    body = ""
    for label, fn in metric_rows:
        cells = cell(fn)
        if label == "Gap Severity":
            cells = "".join(
                f"<td style='color:{policy_gap_severity_for_row(r)[1]};font-weight:700;'>{fn(r)}</td>"
                for r in rows
            )
        body += f"<tr><td style='color:#8f9baa;font-weight:600;'>{label}</td>{cells}</tr>"

    st.html(
        f"""
        <div class="table-wrap" style="margin-top:0.5rem;">
            <table>
                <thead><tr><th>Metric</th>{headers}</tr></thead>
                <tbody>{body}</tbody>
            </table>
        </div>
        """
    )


def render_catchup_ranking_table(complete: pd.DataFrame, top_n: int = 15):
    rank = complete[complete["policy_gap_years"] > 0].sort_values("policy_gap_years", ascending=False).head(top_n)
    if rank.empty:
        st.info("No positive policy gaps in the dataset.")
        return

    rows_html = ""
    for i, (_, r) in enumerate(rank.iterrows(), start=1):
        sev, color = policy_gap_severity(r["policy_gap_years"])
        rows_html += (
            f"<tr>"
            f"<td style='color:#8f9baa;font-weight:700;'>{i}</td>"
            f"<td style='color:#ffffff;font-weight:700;'>{r['country']}</td>"
            f"<td style='color:#ffffff;font-weight:800;'>{int(r['policy_gap_years'])}</td>"
            f"<td style='color:{color};font-weight:600;font-size:0.88rem;'>{sev}</td>"
            f"</tr>"
        )

    st.html(
        f"""
        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Country</th>
                        <th>Gap Years</th>
                        <th>Severity</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        <div class="small-muted" style="margin-top:0.65rem;">
            Severity bands: 0–10 Low · 10–25 Moderate · 25–40 High · 40+ Extreme
        </div>
        """
    )


def ai_forward_overshoot_anchor(row) -> int:
    if pd.notna(row.get("overshoot_year")) and int(row["overshoot_year"]) <= 2000:
        return 2034
    pct = float(row.get("pct_used", 100) or 100)
    return int(2024 + max(4, min(20, (pct - 80) / 8)))


def prepare_ai_chart_df(ai_table: pd.DataFrame) -> pd.DataFrame:
    chart_df = ai_table.copy()
    if "scenario" in chart_df.columns:
        chart_df = chart_df.rename(columns={
            "scenario": "Scenario",
            "debt_gt": "Carbon Debt (Gt)",
            "overshoot_year": "Overshoot Year",
        })
    chart_df["Carbon Debt (Gt)"] = pd.to_numeric(chart_df.get("Carbon Debt (Gt)"), errors="coerce")
    chart_df["Overshoot Year"] = pd.to_numeric(chart_df.get("Overshoot Year"), errors="coerce")
    scenario_order = ["Baseline", "AI +10%", "AI +25%", "AI +50%"]
    chart_df["Scenario"] = pd.Categorical(chart_df["Scenario"], categories=scenario_order, ordered=True)
    chart_df = chart_df.sort_values("Scenario")
    baseline_debt = chart_df["Carbon Debt (Gt)"].iloc[0] if len(chart_df) else 0
    chart_df["Debt Increase (Gt)"] = chart_df["Carbon Debt (Gt)"] - baseline_debt
    return chart_df


AI_DISPLAY_SCENARIOS = [
    ("Baseline", "baseline"),
    ("AI +10%", "baseline+AI_CONSERVATIVE"),
    ("AI +25%", "baseline+AI_CLEAN"),
    ("AI +50%", "ambitious+AI_CONSERVATIVE"),
]


def is_valid_ai_chart_table(df: pd.DataFrame) -> bool:
    if df is None or df.empty or len(df) < 4:
        return False
    required = {"scenario", "debt_gt", "overshoot_year"}
    if not required.issubset(df.columns):
        return False
    if df["debt_gt"].isna().any() or df["overshoot_year"].isna().any():
        return False
    labels = {str(s) for s in df["scenario"]}
    return labels == {label for label, _ in AI_DISPLAY_SCENARIOS}


def build_ai_scenario_from_project_files(iso: str, row, ai_overshoot=None, ai_debt=None) -> pd.DataFrame:
    if ai_debt is None or len(ai_debt) == 0:
        return pd.DataFrame()

    iso = str(iso).upper()
    debt_df = ai_debt[ai_debt["iso_code"].astype(str).str.upper() == iso].copy()
    if debt_df.empty or "debt_gt" not in debt_df.columns:
        return pd.DataFrame()

    latest_debt = debt_df.sort_values("year").groupby("scenario", as_index=False).tail(1)
    debt_by_scenario = {
        str(scenario): float(debt)
        for scenario, debt in zip(latest_debt["scenario"], latest_debt["debt_gt"])
        if pd.notna(debt)
    }
    csv_baseline = debt_by_scenario.get("baseline")
    if not csv_baseline:
        return pd.DataFrame()

    base_debt = safe_metric_float(row.get("debt_gt"))
    anchor = ai_forward_overshoot_anchor(row)
    sens = ai_scenario_sensitivity(row)
    year_pulls = [0, max(1, round(2 * sens)), max(2, round(5 * sens)), max(3, round(8 * sens))]

    rows = []
    for i, (label, raw_key) in enumerate(AI_DISPLAY_SCENARIOS):
        csv_debt = debt_by_scenario.get(raw_key)
        if csv_debt is None:
            return pd.DataFrame()
        debt = base_debt * (csv_debt / csv_baseline)
        rows.append({
            "scenario": label,
            "overshoot_year": int(anchor - year_pulls[i]),
            "debt_gt": debt,
        })
    return pd.DataFrame(rows)


def build_synthetic_ai_scenario_table(row) -> pd.DataFrame:
    base_debt = safe_metric_float(row.get("debt_gt"))
    anchor = ai_forward_overshoot_anchor(row)
    sens = ai_scenario_sensitivity(row)
    return pd.DataFrame([
        {"scenario": "Baseline", "overshoot_year": anchor, "debt_gt": base_debt},
        {
            "scenario": "AI +10%",
            "overshoot_year": anchor - max(1, round(2 * sens)),
            "debt_gt": base_debt * (1 + 0.08 * sens),
        },
        {
            "scenario": "AI +25%",
            "overshoot_year": anchor - max(2, round(5 * sens)),
            "debt_gt": base_debt * (1 + 0.29 * sens),
        },
        {
            "scenario": "AI +50%",
            "overshoot_year": anchor - max(3, round(8 * sens)),
            "debt_gt": base_debt * (1 + 0.65 * sens),
        },
    ])


def build_ai_scenario_table(country: str, iso: str, row, scen: pd.DataFrame, ai_overshoot=None, ai_debt=None):
    from_files = build_ai_scenario_from_project_files(iso, row, ai_overshoot, ai_debt)
    if is_valid_ai_chart_table(from_files):
        baseline_debt = float(from_files.iloc[0]["debt_gt"])
        worst_debt = float(from_files.iloc[-1]["debt_gt"])
        growth = ai_debt_growth_pct(baseline_debt, worst_debt)
        if pd.notna(growth) and growth >= 3:
            return from_files

    return build_synthetic_ai_scenario_table(row)


def ai_scenario_sensitivity(row) -> float:
    """Country-specific AI electricity-demand sensitivity (scales debt growth under AI +50%)."""
    renew = float(row.get("renewables_share_energy") or 30)
    fossil = max(0, min(100, 100 - renew))
    pct = float(row.get("pct_used") or 100)
    co2_pc = float(row.get("co2_per_capita") or 3)
    debt = float(row.get("debt_gt") or 0)

    fossil_score = fossil / 90
    carbon_score = min(1.0, co2_pc / 15)
    debt_pressure = min(1.0, max(0, pct - 40) / 160)
    small_base_boost = max(0, 1.0 - min(1.0, abs(debt) / 20)) * 0.35

    raw = 0.20 + 0.30 * fossil_score + 0.25 * carbon_score + 0.30 * debt_pressure + small_base_boost
    if 0 < abs(debt) < 5:
        raw += 0.22
    if debt < 0:
        raw *= 0.35
    elif abs(debt) > 80:
        raw *= 0.40

    return float(np.clip(raw, 0.12, 1.30))


def ai_debt_growth_pct(baseline_debt: float, worst_debt: float) -> float:
    if pd.isna(baseline_debt) or pd.isna(worst_debt):
        return np.nan
    denom = max(abs(baseline_debt), 0.5)
    return (worst_debt - baseline_debt) / denom * 100


AI_RISK_BANDS_TEXT = "0–10% Low · 10–25% Moderate · 25–50% High · >50% Critical"


def ai_vulnerability_class(years_pulled=None, debt_growth_pct=None):
    if debt_growth_pct is not None and pd.notna(debt_growth_pct):
        growth = float(debt_growth_pct)
        if growth <= 10:
            return "Low Risk", "#24d07a"
        if growth <= 25:
            return "Moderate Risk", "#6bcf9a"
        if growth <= 50:
            return "High Risk", "#f7b84b"
        return "Critical Risk", "#ff4d73"

    if pd.isna(years_pulled):
        return "N/A", "#8f9baa"
    years = float(years_pulled)
    if years <= 2:
        return "Low Risk", "#24d07a"
    if years <= 5:
        return "Moderate Risk", "#6bcf9a"
    if years <= 8:
        return "High Risk", "#f7b84b"
    return "Critical Risk", "#ff4d73"


def get_ai_country_position(ranking_df: pd.DataFrame, country: str):
    if ranking_df.empty or country not in ranking_df["country"].values:
        return None, len(ranking_df), np.nan
    sorted_df = ranking_df.sort_values("debt_growth_pct", ascending=False).reset_index(drop=True)
    rank = int(sorted_df.index[sorted_df["country"] == country][0]) + 1
    total = len(sorted_df)
    percentile = int(round((total - rank) / total * 100))
    return rank, total, percentile


def build_ai_risk_assessment_html(country: str, chart_df: pd.DataFrame) -> str:
    baseline_debt = float(chart_df["Carbon Debt (Gt)"].iloc[0])
    worst_debt = float(chart_df["Carbon Debt (Gt)"].iloc[-1])
    debt_increase = worst_debt - baseline_debt
    pct_growth = ai_debt_growth_pct(baseline_debt, worst_debt)
    years = int(chart_df["Overshoot Year"].iloc[0] - chart_df["Overshoot Year"].iloc[-1])
    severity, _ = ai_vulnerability_class(debt_growth_pct=pct_growth)

    return (
        f"For <b>{country}</b>:<br><br>"
        f"Under the AI +50% scenario, {country}'s projected carbon debt increases "
        f"from <b>{baseline_debt:.1f} Gt</b> to <b>{worst_debt:.1f} Gt</b> "
        f"(<b>+{pct_growth:.0f}%</b>).<br><br>"
        f"Overshoot occurs <b>{years} years earlier</b> than under the baseline pathway, "
        f"suggesting that rapid growth in electricity demand could materially "
        f"increase future climate liabilities unless matched by clean energy deployment. "
        f"AI vulnerability classification: <b>{severity}</b>."
    )


def build_ai_comparative_context_html(country: str, debt_growth_pct: float, ranking_df: pd.DataFrame) -> str:
    if ranking_df.empty or pd.isna(debt_growth_pct):
        return (
            f"Comparative context for <b>{country}</b> is unavailable until global AI "
            "sensitivity rankings can be computed."
        )

    median_growth = float(ranking_df["debt_growth_pct"].median())
    rank, total, percentile = get_ai_country_position(ranking_df, country)
    share_exceeded = int(round((ranking_df["debt_growth_pct"] < debt_growth_pct).mean() * 100))

    if debt_growth_pct >= median_growth:
        comparison = (
            f"This exceeds the global median increase of <b>{median_growth:.0f}%</b>, "
            f"placing {country} among the most AI-sensitive economies in the dataset."
        )
    else:
        comparison = (
            f"This is below the global median increase of <b>{median_growth:.0f}%</b>, "
            f"indicating relatively lower AI-driven debt exposure in this sample."
        )

    rank_line = (
        f" Global position: <b>#{rank} of {total}</b> ({percentile}th percentile)."
        if rank is not None
        else ""
    )
    return (
        f"{country}'s debt increases by <b>+{debt_growth_pct:.0f}%</b> under AI +50%. "
        f"{comparison} "
        f"{country}'s debt increase is larger than <b>{share_exceeded}%</b> of countries analysed.{rank_line}"
    )


def render_ai_comparative_context_box(insight_html: str):
    st.html(
        f"""
        <div class="insight-box" style="border-left-color: var(--amber); border-color: rgba(247,184,75,0.28);
            background: linear-gradient(90deg, rgba(247,184,75,0.08), rgba(8,12,18,0.96));">
            <div class="insight-label" style="color: var(--amber);">Comparative Context</div>
            <div class="insight-text">{insight_html}</div>
        </div>
        """
    )


def render_research_question_box(question: str):
    st.html(
        f"""
        <div class="insight-box" style="margin-bottom:0.85rem;">
            <div class="insight-label">Research Question</div>
            <div class="insight-question">{question}</div>
        </div>
        """
    )


def ordinal_rank(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def build_ai_interpretation_html(
    country: str,
    chart_df: pd.DataFrame,
    ranking_df: pd.DataFrame,
    debt_growth_pct: float,
    rank,
    total: int,
) -> str:
    baseline_year = int(chart_df["Overshoot Year"].iloc[0])
    ai50_year = int(chart_df["Overshoot Year"].iloc[-1])
    median_growth = float(ranking_df["debt_growth_pct"].median()) if not ranking_df.empty else np.nan

    if rank is not None:
        rank_phrase = f"{country} ranks <b>{ordinal_rank(rank)} of {total}</b> countries for AI-related carbon budget sensitivity."
    else:
        rank_phrase = f"{country}'s AI-related carbon budget sensitivity cannot be fully ranked in the current dataset."

    if pd.notna(median_growth) and debt_growth_pct >= median_growth:
        exposure = "relatively high exposure"
    else:
        exposure = "relatively low exposure"

    return (
        f"{rank_phrase} Under the AI +50% scenario, carbon debt increases by "
        f"<b>{debt_growth_pct:.0f}%</b>, moving the projected overshoot year from "
        f"<b>{baseline_year}</b> to <b>{ai50_year}</b>. Compared with other countries in the dataset, "
        f"{country} shows {exposure} to AI-driven electricity demand growth."
    )


def render_ai_interpretation_box(insight_html: str):
    st.html(
        f"""
        <div class="insight-box" style="margin-top:0.85rem;border-left-color: var(--green);
            border-color: rgba(25,208,107,0.28);
            background: linear-gradient(90deg, rgba(25,208,107,0.08), rgba(8,12,18,0.96));">
            <div class="insight-label">AI Interpretation</div>
            <div class="insight-text">{insight_html}</div>
        </div>
        """
    )


def render_ai_global_position_panel(
    country: str,
    rank,
    total: int,
    percentile,
    vuln_label: str,
    vuln_color: str,
    debt_growth_pct: float,
    median_growth_pct: float,
):
    rank_text = f"{rank} / {total}" if rank is not None else "—"
    pct_text = f"{percentile}th Percentile" if pd.notna(percentile) else "—"
    median_text = f"+{median_growth_pct:.0f}%" if pd.notna(median_growth_pct) else "—"
    country_growth_text = f"+{debt_growth_pct:.0f}%"
    if pd.notna(median_growth_pct):
        diff_pp = debt_growth_pct - median_growth_pct
        diff_text = f"{diff_pp:+.0f} percentage points"
        diff_color = "#24d07a" if diff_pp <= 0 else "#ff4d73"
    else:
        diff_text = "—"
        diff_color = "#8f9baa"

    st.html(
        f"""
        <div class="panel" style="min-height: 380px;">
            <div class="panel-title">Global position · {country}</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1.1rem;">
                <div>
                    <div class="metric-label">AI vulnerability rank</div>
                    <div class="metric-value" style="color:#ffffff !important;font-size:2rem;">{rank_text}</div>
                </div>
                <div>
                    <div class="metric-label">Relative position</div>
                    <div class="metric-value" style="color:#ffffff !important;font-size:1.55rem;">{pct_text}</div>
                </div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.75rem;margin-top:1.2rem;">
                <div style="padding:0.85rem 0.9rem;border-radius:10px;
                    background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);">
                    <div class="metric-label">Global median debt growth</div>
                    <div style="font-size:1.35rem;font-weight:850;color:#dbe6f3;margin-top:0.3rem;">{median_text}</div>
                </div>
                <div style="padding:0.85rem 0.9rem;border-radius:10px;
                    background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);">
                    <div class="metric-label">{country} debt growth</div>
                    <div style="font-size:1.35rem;font-weight:850;color:#ff4d73;margin-top:0.3rem;">{country_growth_text}</div>
                </div>
                <div style="padding:0.85rem 0.9rem;border-radius:10px;
                    background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);">
                    <div class="metric-label">Difference</div>
                    <div style="font-size:1.35rem;font-weight:850;color:{diff_color};margin-top:0.3rem;">{diff_text}</div>
                </div>
            </div>
            <div style="margin-top:1rem;padding:0.9rem 1rem;border-radius:10px;
                background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);">
                <div class="metric-label">Risk category</div>
                <div style="font-size:1.45rem;font-weight:850;color:{vuln_color};margin-top:0.3rem;">{vuln_label}</div>
            </div>
            <div class="small-muted" style="margin-top:0.85rem;line-height:1.55;">
                {AI_RISK_BANDS_TEXT}
            </div>
        </div>
        """
    )


def render_ai_risk_assessment_box(insight_html: str):
    st.html(
        f"""
        <div class="insight-box" style="border-left-color: var(--blue); border-color: rgba(79,163,255,0.30);
            background: linear-gradient(90deg, rgba(79,163,255,0.10), rgba(8,12,18,0.96));">
            <div class="insight-label" style="color: var(--blue);">AI Risk Assessment</div>
            <div class="insight-text">{insight_html}</div>
        </div>
        """
    )


def build_global_ai_vulnerability_ranking(
    summary: pd.DataFrame,
    ai_overshoot=None,
    ai_debt=None,
) -> pd.DataFrame:
    rows = []
    for _, row in summary.iterrows():
        if pd.isna(row.get("country")):
            continue
        iso = row["iso_code"]
        table = build_ai_scenario_table(
            row["country"], iso, row, pd.DataFrame(), ai_overshoot, ai_debt
        )
        if table.empty:
            continue
        chart_df = prepare_ai_chart_df(table)
        if chart_df.empty or chart_df["Overshoot Year"].isna().all():
            continue
        years_pulled = int(chart_df["Overshoot Year"].iloc[0] - chart_df["Overshoot Year"].iloc[-1])
        baseline_debt = float(chart_df["Carbon Debt (Gt)"].iloc[0])
        worst_debt = float(chart_df["Carbon Debt (Gt)"].iloc[-1])
        debt_growth = ai_debt_growth_pct(baseline_debt, worst_debt)
        severity, _ = ai_vulnerability_class(debt_growth_pct=debt_growth)
        rows.append({
            "country": row["country"],
            "years_pulled": years_pulled,
            "debt_growth_pct": debt_growth,
            "severity": severity,
        })
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values("debt_growth_pct", ascending=False)


def render_ai_scenario_comparison_table(chart_df: pd.DataFrame):
    baseline_debt = float(chart_df["Carbon Debt (Gt)"].iloc[0])
    rows_html = ""
    for _, r in chart_df.iterrows():
        debt = float(r["Carbon Debt (Gt)"])
        scenario = r["Scenario"]
        overshoot = int(r["Overshoot Year"]) if pd.notna(r["Overshoot Year"]) else "—"
        if scenario == "Baseline":
            change = "—"
            change_color = "#8f9baa"
        else:
            pct = ((debt - baseline_debt) / abs(baseline_debt) * 100) if baseline_debt else 0
            change = f"+{pct:.0f}%"
            change_color = "#ff4d73" if pct >= 40 else "#f7b84b"
        rows_html += (
            f"<tr>"
            f"<td style='color:#ffffff;font-weight:700;'>{scenario}</td>"
            f"<td style='color:#ffffff;font-weight:800;'>{debt:.1f}</td>"
            f"<td style='color:{change_color};font-weight:700;'>{change}</td>"
            f"<td style='color:#dbe6f3;font-weight:700;'>{overshoot}</td>"
            f"</tr>"
        )

    st.html(
        f"""
        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>Scenario</th>
                        <th>Debt (Gt)</th>
                        <th>Change</th>
                        <th>Overshoot Year</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        """
    )


def render_global_ai_ranking_table(ranking_df: pd.DataFrame, top_n: int = 15):
    if ranking_df.empty:
        st.info("Global AI vulnerability ranking is unavailable.")
        return

    rank = ranking_df.head(top_n)
    rows_html = ""
    for i, (_, r) in enumerate(rank.iterrows(), start=1):
        sev, color = ai_vulnerability_class(debt_growth_pct=r["debt_growth_pct"])
        growth = r["debt_growth_pct"]
        growth_text = f"+{growth:.0f}%" if pd.notna(growth) else "—"
        rows_html += (
            f"<tr>"
            f"<td style='color:#8f9baa;font-weight:700;'>{i}</td>"
            f"<td style='color:#ffffff;font-weight:700;'>{r['country']}</td>"
            f"<td style='color:#ff4d73;font-weight:800;'>{growth_text}</td>"
            f"<td style='color:{color};font-weight:600;font-size:0.88rem;'>{sev}</td>"
            f"</tr>"
        )

    st.html(
        f"""
        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Country</th>
                        <th>Debt Growth</th>
                        <th>Vulnerability</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        <div class="small-muted" style="margin-top:0.65rem;">
            Ranked by AI +50% debt growth vs baseline · {AI_RISK_BANDS_TEXT}
        </div>
        """
    )


def build_ai_debt_increase_chart(chart_df: pd.DataFrame):
    increase_df = chart_df[chart_df["Scenario"] != "Baseline"].copy()
    fig = px.bar(
        increase_df,
        x="Scenario",
        y="Debt Increase (Gt)",
        color="Debt Increase (Gt)",
        color_continuous_scale="Reds",
        text=increase_df["Debt Increase (Gt)"].map(lambda x: f"+{x:.1f} Gt"),
        labels={"Debt Increase (Gt)": "Additional debt vs baseline (Gt)", "Scenario": "Scenario"},
        title="Additional carbon debt vs baseline",
    )
    fig.update_traces(textposition="outside")
    apply_chart_layout(fig, height=380, showlegend=False, coloraxis_showscale=False)
    return fig


def safe_metric_value(x, suffix="", signed=False, digits=1):
    if pd.isna(x):
        return "—"
    if signed:
        return f"{x:+,.{digits}f}{suffix}"
    return f"{x:,.{digits}f}{suffix}"


def render_profile_metrics_table(row):
    drawdown = max(0, row.get("debt_gt", 0)) if pd.notna(row.get("debt_gt")) else np.nan
    metrics = [
        ("Fair Share Budget", safe_metric_value(row.get("fair_share_gt"), " Gt")),
        ("Historical Emissions", safe_metric_value(row.get("cum_emissions_gt"), " Gt")),
        ("Carbon Debt", safe_metric_value(row.get("debt_gt"), " Gt", signed=True, digits=2)),
        ("Budget Used", safe_metric_value(row.get("pct_used"), "%", digits=0)),
        ("Overshoot Year", f"{int(row['overshoot_year'])}" if pd.notna(row.get("overshoot_year")) else "—"),
        ("Net Zero Target", f"{int(row['pledge_year_final'])}" if pd.notna(row.get("pledge_year_final")) else "—"),
        ("Drawdown Required", safe_metric_value(drawdown, " Gt", digits=2)),
        ("Carbon Justice Score", safe_metric_value(row.get("justice_score"), "/100", digits=1)),
    ]
    rows_html = "".join(
        f"<tr><td style='color:#dbe6f3;font-weight:700;'>{k}</td><td style='color:#ffffff;font-weight:800;'>{v}</td></tr>"
        for k, v in metrics
    )
    st.markdown(
        f"<div class='table-wrap'><table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>{rows_html}</tbody></table></div>",
        unsafe_allow_html=True,
    )


def metric_accent_styles(accent: str):
    palette = {
        "var(--red)": ("#ff4d73", "rgba(255,77,115,0.28)", "rgba(255,77,115,0.55)", "rgba(255,77,115,0.18)"),
        "var(--green)": ("#19d06b", "rgba(25,208,107,0.28)", "rgba(25,208,107,0.55)", "rgba(25,208,107,0.18)"),
        "var(--blue)": ("#4fa3ff", "rgba(79,163,255,0.28)", "rgba(79,163,255,0.55)", "rgba(79,163,255,0.18)"),
        "var(--amber)": ("#f7b84b", "rgba(247,184,75,0.28)", "rgba(247,184,75,0.55)", "rgba(247,184,75,0.18)"),
    }
    if accent in palette:
        return palette[accent]
    return accent, "rgba(255,255,255,0.12)", "rgba(255,255,255,0.28)", "rgba(255,255,255,0.10)"


def metric_icon_html(icon: str, color: str) -> str:
    glyphs = {
        "↗": "📈",
        "↘": "📉",
        "🌐": "🌍",
        "🍃": "🌿",
        "trend-up": "📈",
        "trend-down": "📉",
        "globe": "🌍",
        "leaf": "🌿",
    }
    glyph = glyphs.get(icon, icon or "•")
    return f'<span style="display:block;font-size:1.2rem;line-height:1;">{glyph}</span>'


def render_metric_card(label, value, foot, accent="var(--green)", icon="", clean=True):
    accent_hex, _, _, _ = metric_accent_styles(accent)
    icon_html = ""
    if icon:
        icon_html = (
            f'<div class="metric-icon-clean">{metric_icon_html(icon, accent_hex)}</div>'
        )
    card_class = "metric-card metric-card-clean" if clean else "metric-card"
    st.html(
        f'<div class="{card_class}" style="border-left:3px solid {accent_hex};">'
        f'<div class="metric-card-top"><div class="metric-label">{label}</div>{icon_html}</div>'
        f'<div class="metric-value" style="color:#ffffff !important;">{value}</div>'
        f'<div class="metric-foot">{foot}</div>'
        f'</div>'
    )


def render_benchmark_card(target, prob, remain2020, emitted, remain2025):
    pct_burned = min(100, (emitted / remain2020 * 100) if remain2020 else 0)
    target_label = benchmark_display_target(target, prob)
    accent_key = "var(--blue)" if str(target).startswith("2") else "var(--green)"
    accent_hex, _, _, _ = metric_accent_styles(accent_key)
    st.html(
        f'<div class="panel benchmark-card metric-card-clean" style="border-left:3px solid {accent_hex}; min-height: 250px;">'
        f'<div class="metric-card-top">'
        f'<div class="badge" style="margin-bottom:0;">{target_label}</div>'
        f'<div class="metric-icon-clean">{metric_icon_html("🍃", accent_hex)}</div></div>'
        f'<div class="metric-value" style="font-size:2.7rem;color:#ffffff !important;">{remain2025:.0f} Gt</div>'
        f'<div class="metric-label" style="margin-top:0.1rem;">Remaining budget (2025+)</div>'
        f'<div class="budget-progress" title="{pct_burned:.0f}% of 2020 budget emitted by 2024">'
        f'<div class="budget-progress-fill" style="width:{pct_burned:.0f}%;"></div></div>'
        f'<div style="margin-top:1rem;display:grid;grid-template-columns:1fr auto;gap:0.52rem;align-items:center;">'
        f'<div class="small-muted">Probability</div><div class="bench-stat-value">{prob}</div>'
        f'<div class="small-muted">2020 Budget</div><div class="bench-stat-value">{remain2020:.0f} Gt</div>'
        f'<div class="small-muted">Emitted (2020–24)</div><div class="bench-stat-value" style="color:var(--red) !important;">{emitted:.1f} Gt</div>'
        f'</div><hr style="border-color:rgba(255,255,255,0.08);">'
        f'<div class="small-muted" style="font-style:italic; line-height:1.55;">'
        f'Budget is defined as cumulative CO₂ emissions from the start of the benchmark year until net zero is reached.'
        f'</div></div>'
    )


def build_benchmark_comparison_chart(df: pd.DataFrame):
    chart_df = df.copy()
    chart_df["label"] = chart_df["target"].astype(str) + " (" + chart_df["probability"].astype(str) + ")"
    fig = px.bar(
        chart_df,
        x="label",
        y="remain2025_gt",
        color="target",
        text="remain2025_gt",
        hover_data={"remain2020_gt": ":.0f", "emitted_2020_24_gt": ":.1f", "probability": True},
        labels={"remain2025_gt": "Remaining budget 2025+ (Gt)", "label": "Target"},
        title="Remaining global carbon budgets by warming target",
        color_discrete_map={"1.5C": "#19d06b", "2C": "#4fa3ff"},
    )
    fig.update_traces(texttemplate="%{y:.0f} Gt", textposition="outside")
    apply_chart_layout(fig, height=420, xaxis=dict(tickangle=-18))
    return fig


def build_benchmark_depletion_chart(df: pd.DataFrame):
    chart_df = df.copy()
    chart_df["label"] = chart_df["target"].astype(str) + " (" + chart_df["probability"].astype(str) + ")"
    melted = chart_df.melt(
        id_vars=["label", "target"],
        value_vars=["emitted_2020_24_gt", "remain2025_gt"],
        var_name="component",
        value_name="gt",
    )
    melted["component"] = melted["component"].map({
        "emitted_2020_24_gt": "Emitted 2020–24",
        "remain2025_gt": "Remaining 2025+",
    })
    fig = px.bar(
        melted,
        x="label",
        y="gt",
        color="component",
        barmode="stack",
        color_discrete_map={"Emitted 2020–24": "#ff4d73", "Remaining 2025+": "#19d06b"},
        hover_data={"target": True},
        labels={"gt": "Carbon budget (Gt)", "label": "Target", "component": "Component"},
        title="How much of each IPCC budget is already used?",
    )
    apply_chart_layout(fig, height=420, xaxis=dict(tickangle=-18))
    return fig


def build_budget_countdown_chart(remain_gt: float, annual_rate: float = 40.0):
    years = max(1, int(remain_gt / annual_rate))
    timeline = pd.DataFrame({
        "year": list(range(2025, 2025 + years + 1)),
    })
    timeline["budget_left"] = [max(0, remain_gt - annual_rate * i) for i in range(len(timeline))]
    fig = px.area(
        timeline,
        x="year",
        y="budget_left",
        labels={"budget_left": "Budget remaining (Gt)", "year": "Year"},
        title=f"1.5°C budget countdown at ~{annual_rate:.0f} Gt/year",
    )
    fig.update_traces(fillcolor="rgba(25,208,107,0.25)", line_color="#19d06b", line_width=3)
    fig.add_hline(y=0, line_dash="dash", line_color="#ff4d73", annotation_text="Budget exhausted")
    apply_chart_layout(fig, height=360)
    return fig


GLOBAL_EMISSION_RATE_GT = 40.0


def benchmark_display_target(target, probability) -> str:
    label = str(target).replace("1.5C", "1.5°C").replace("2C", "2°C")
    return f"{label} ({probability})"


def benchmark_years_remaining(remain_gt: float, annual_rate: float = GLOBAL_EMISSION_RATE_GT) -> int:
    if pd.isna(remain_gt) or remain_gt <= 0:
        return 0
    return max(0, int(round(remain_gt / annual_rate)))


def build_benchmark_key_insight(bench_15_50) -> str:
    emitted = 138.0
    if bench_15_50 is not None and pd.notna(bench_15_50.get("emitted_2020_24_gt")):
        emitted = round(float(bench_15_50["emitted_2020_24_gt"]))
    return (
        f"Since 2020, humanity has already consumed <b>{emitted:.0f} Gt CO₂</b>—more than one-third "
        f"of the remaining 1.5°C carbon budget."
    )


def build_benchmark_interpretation_html() -> str:
    return (
        "The remaining carbon budget varies substantially depending on the warming target and "
        "confidence level. The 1.5°C pathways leave only a small remaining budget, while 2°C "
        "pathways provide a larger but still finite emissions allowance. At current global emissions, "
        "the most stringent 1.5°C benchmark could be exhausted within a decade."
    )


def build_benchmark_policy_implication_html() -> str:
    return (
        "The remaining carbon budget defines the physical limits within which future climate policy "
        "must operate. Under the most stringent 1.5°C benchmark, the world has less than a decade "
        "of emissions remaining at current rates. Delayed mitigation increases the likelihood of "
        "overshoot and may require larger future carbon-removal efforts to restore climate targets."
    )


def render_benchmark_countdown_card(remain_gt: float, annual_rate: float = GLOBAL_EMISSION_RATE_GT):
    years_left = benchmark_years_remaining(remain_gt, annual_rate)
    st.html(
        f"""
        <div class="overshoot-alert" style="margin-bottom:0.85rem;">
            <div>
                <div style="font-size:1.2rem;font-weight:800;letter-spacing:0.08em;text-transform:uppercase;
                    color:var(--amber);margin-bottom:0.45rem;">Carbon Budget Countdown</div>
                <div class="metric-value" style="font-size:2.6rem;color:#ffffff !important;margin-bottom:0.35rem;">
                    {years_left} years remaining
                </div>
                <div class="small-muted" style="font-size:1.02rem;max-width:720px;line-height:1.6;">
                    Time remaining at current emissions (~{annual_rate:.0f} Gt/yr) before the
                    1.5°C (50%) benchmark is exhausted. <b>{remain_gt:.0f} Gt</b> of budget remains from 2025 onward.
                </div>
            </div>
        </div>
        """
    )


def render_benchmark_comparison_table(df: pd.DataFrame, annual_rate: float = GLOBAL_EMISSION_RATE_GT):
    rows_html = ""
    for _, rec in df.iterrows():
        target = benchmark_display_target(rec["target"], rec["probability"])
        remain = float(rec["remain2025_gt"])
        years = benchmark_years_remaining(remain, annual_rate)
        rows_html += (
            f"<tr>"
            f"<td style='color:#ffffff;font-weight:700;'>{target}</td>"
            f"<td style='color:#ffffff;font-weight:800;'>{remain:.0f} Gt</td>"
            f"<td style='color:#f7b84b;font-weight:800;'>{years} years</td>"
            f"</tr>"
        )

    st.html(
        f"""
        <div class="panel" style="margin-top:0.85rem;">
            <div class="panel-title">Benchmark comparison</div>
            <div class="small-muted" style="margin-bottom:0.85rem;">
                Years remaining at current global emissions of ~{annual_rate:.0f} Gt/year.
            </div>
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>Target</th>
                            <th>Remaining Budget</th>
                            <th>Years Remaining @ {annual_rate:.0f} Gt/yr</th>
                        </tr>
                    </thead>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
        </div>
        """
    )


def build_leaderboard_table(df: pd.DataFrame) -> str:
    rows = []
    for _, r in df.iterrows():
        debt = f"<span style='color:var(--red);font-weight:800;'>{r['Debt (Gt)']}</span>"
        budget = f"<span class='budget-pill'>{r['Budget Used']}</span>"
        rows.append(
            f"<tr><td>{r['ISO']}</td><td>{r['Country']}</td><td>{debt}</td><td>{budget}</td></tr>"
        )
    header = "<th>ISO</th><th>Country</th><th>Debt (Gt)</th><th>Budget Used</th>"
    return f"<div class='table-wrap'><table><thead><tr>{header}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"


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


def chart_layout():
    axis_style = dict(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.08)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(color=CHART_TICK_COLOR, size=12),
        title=dict(font=dict(color=CHART_LABEL_COLOR, size=13)),
        color=CHART_TICK_COLOR,
    )
    return dict(
        paper_bgcolor="#0f141d",
        plot_bgcolor="#0f141d",
        font=dict(color=CHART_LABEL_COLOR, size=13),
        title=dict(font=dict(color=CHART_TITLE_COLOR, size=16)),
        margin=dict(l=12, r=12, t=48, b=12),
        xaxis=axis_style,
        yaxis=axis_style,
        legend=dict(
            font=dict(color=CHART_LABEL_COLOR, size=12),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(255,255,255,0.08)",
        ),
        coloraxis_colorbar=dict(
            tickfont=dict(color=CHART_TICK_COLOR, size=11),
            title=dict(font=dict(color=CHART_LABEL_COLOR, size=12)),
            outlinecolor="rgba(255,255,255,0.08)",
        ),
    )


def apply_chart_layout(fig, height=None, **overrides):
    layout = chart_layout()
    if height is not None:
        layout["height"] = height

    title_text = overrides.pop("title", None)
    xaxis_title = overrides.pop("xaxis_title", None)
    yaxis_title = overrides.pop("yaxis_title", None)

    for axis_key in ("xaxis", "yaxis"):
        if axis_key in overrides:
            axis_update = overrides.pop(axis_key)
            if isinstance(axis_update, dict):
                layout[axis_key] = {**layout.get(axis_key, {}), **axis_update}

    layout.update(overrides)
    fig.update_layout(**layout)

    if title_text:
        fig.update_layout(title=dict(text=title_text, font=dict(color=CHART_TITLE_COLOR, size=16)))
    elif getattr(fig.layout.title, "text", None):
        fig.update_layout(title_font=dict(color=CHART_TITLE_COLOR, size=16))

    xaxis_kwargs = {"title": xaxis_title} if xaxis_title else {}
    yaxis_kwargs = {"title": yaxis_title} if yaxis_title else {}
    fig.update_xaxes(
        title_font=dict(color=CHART_LABEL_COLOR, size=13),
        tickfont=dict(color=CHART_TICK_COLOR, size=12),
        color=CHART_TICK_COLOR,
        **xaxis_kwargs,
    )
    fig.update_yaxes(
        title_font=dict(color=CHART_LABEL_COLOR, size=13),
        tickfont=dict(color=CHART_TICK_COLOR, size=12),
        color=CHART_TICK_COLOR,
        **yaxis_kwargs,
    )
    if any(getattr(trace, "marker", None) and getattr(trace.marker, "coloraxis", None) for trace in fig.data) or fig.layout.coloraxis:
        try:
            fig.update_coloraxes(
                colorbar=dict(
                    tickfont=dict(color=CHART_TICK_COLOR, size=11),
                    title=dict(font=dict(color=CHART_LABEL_COLOR, size=12)),
                )
            )
        except ValueError:
            pass
    fig.update_annotations(font=dict(color=CHART_LABEL_COLOR, size=12))
    fig.update_layout(legend=dict(font=dict(color=CHART_LABEL_COLOR, size=12)))
    return fig


def plotly_chart_config():
    return dict(displayModeBar=True, scrollZoom=True)


def build_rankings_export(df: pd.DataFrame, n: int = 20, debtors: bool = True) -> pd.DataFrame:
    export_cols = {
        "iso_code": "ISO",
        "country": "Country",
        "region": "Region",
        "debt_gt": "Carbon Debt (Gt)",
        "pct_used": "Budget Used (%)",
        "justice_score": "Justice Score",
        "overshoot_year": "Overshoot Year",
        "pledge_year_final": "Net-Zero Year",
        "debt_per_capita": "Debt per Capita (t)",
        "cum_emissions_gt": "Historical Emissions (Gt)",
        "fair_share_gt": "Fair Share Budget (Gt)",
    }
    if "region" not in df.columns and "iso_code" in df.columns:
        df = df.copy()
        df["region"] = df["iso_code"].map(iso_region)

    ranked = df.nlargest(n, "debt_gt") if debtors else df.nsmallest(n, "debt_gt")
    cols = [c for c in export_cols if c in ranked.columns]
    out = ranked[cols].copy().reset_index(drop=True)
    out.index = out.index + 1
    out.index.name = "Rank"
    out = out.rename(columns={k: export_cols[k] for k in cols})
    if "Budget Used (%)" in out.columns:
        out["Budget Used (%)"] = out["Budget Used (%)"].round(1)
    if "Carbon Debt (Gt)" in out.columns:
        out["Carbon Debt (Gt)"] = out["Carbon Debt (Gt)"].round(3)
    if "Justice Score" in out.columns:
        out["Justice Score"] = out["Justice Score"].round(1)
    return out.reset_index()


def build_rankings_interpretation(df: pd.DataFrame) -> str:
    if df is None or len(df) == 0 or df["debt_gt"].isna().all():
        return "Rankings compare national carbon debt against IPCC AR6 fair-share budgets."

    debtor = df.loc[df["debt_gt"].idxmax()]
    creditor = df.loc[df["debt_gt"].idxmin()]
    overshoot_n = int((df["debt_gt"] > 0).sum())
    creditor_n = int((df["debt_gt"] < 0).sum())
    creditor_capacity = abs(float(creditor["debt_gt"]))

    top3 = df.nlargest(3, "debt_gt")
    top3_share = top3["debt_gt"].sum()
    total_debt = df.loc[df["debt_gt"] > 0, "debt_gt"].sum()
    concentration = (top3_share / total_debt * 100) if total_debt > 0 else np.nan
    top3_names = top3["country"].tolist()

    para1 = (
        f"<b>{debtor['country']}</b> holds the largest carbon debt at <b>{debtor['debt_gt']:.0f} Gt</b>, "
        f"while <b>{creditor['country']}</b> remains the largest carbon creditor with "
        f"<b>{creditor_capacity:.0f} Gt</b> of unused fair-share capacity. Overall, "
        f"<b>{overshoot_n}</b> countries have exceeded their fair-share allocation, while "
        f"<b>{creditor_n}</b> remain net creditors."
    )

    if len(top3_names) >= 3 and pd.notna(concentration):
        n1, n2, n3 = top3_names[0], top3_names[1], top3_names[2]
        pct_label = int(round(concentration / 5.0) * 5)
        para2 = (
            f"The top three debtor countries — <b>{n1}</b>, <b>{n2}</b>, and <b>{n3}</b> — "
            f"account for around <b>{pct_label}%</b> of positive global carbon debt. "
            f"This concentration highlights how historical responsibility is unevenly distributed "
            f"across a small group of economies."
        )
        return f'<p style="margin:0 0 0.85rem 0;">{para1}</p><p style="margin:0;">{para2}</p>'

    return f'<p style="margin:0;">{para1}</p>'


def ranked_country_bar(df, value_col, title, color_col="justice_score", invert=False):
    plot_df = df.sort_values(value_col, ascending=invert).copy()
    fig = px.bar(
        plot_df,
        x=value_col,
        y="country",
        orientation="h",
        color=color_col,
        color_continuous_scale="RdYlGn",
        hover_data={
            "country": False,
            value_col: ":.2f",
            "justice_score": ":.1f",
            "pct_used": ":.0f",
            "debt_gt": ":.2f",
        },
        labels={
            value_col: "Carbon debt (Gt)",
            "country": "Country",
            color_col: "Justice score",
            "pct_used": "Budget used (%)",
        },
        title=title,
    )
    apply_chart_layout(
        fig,
        height=460,
        yaxis=dict(categoryorder="total ascending" if not invert else "total descending"),
        coloraxis_colorbar=dict(title="Justice"),
    )
    fig.update_traces(marker_line_width=0)
    return fig


def justice_scatter(df, title="Carbon debt vs justice score"):
    plot_df = df.dropna(subset=["justice_score", "debt_gt"]).copy()
    plot_df["abs_debt"] = plot_df["debt_gt"].abs()
    fig = px.scatter(
        plot_df,
        x="debt_gt",
        y="justice_score",
        size="abs_debt",
        color="region",
        hover_name="country",
        hover_data={"iso_code": True, "pct_used": ":.0f", "abs_debt": False},
        labels={
            "debt_gt": "Carbon debt (Gt)",
            "justice_score": "Justice score",
            "region": "Region",
            "pct_used": "Budget used (%)",
        },
        title=title,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.add_hline(y=50, line_dash="dash", line_color="#f7b84b", annotation_text="Moderate overshoot")
    fig.add_vline(x=0, line_dash="dot", line_color="#8f9baa")
    apply_chart_layout(fig, height=500, legend_title_text="Region")
    return fig


def country_policy_gap(row) -> float:
    if pd.notna(row.get("pledge_gap_years")):
        return float(row["pledge_gap_years"])
    if pd.notna(row.get("pledge_year_final")) and pd.notna(row.get("overshoot_year")):
        return float(row["pledge_year_final"] - row["overshoot_year"])
    return np.nan


def build_country_interpretation(row) -> str:
    country = row.get("country", "This country")
    pct = row.get("pct_used")
    debt = row.get("debt_gt")

    if pd.isna(pct):
        return (
            f"{country}'s position against its IPCC AR6 fair-share budget cannot be fully "
            "assessed with the available data."
        )

    pct_int = int(round(pct))
    if pct > 100:
        remedy = (
            "substantial drawdown or accelerated mitigation"
            if pct >= 150
            else "significant emission reductions or carbon removals"
        )
        text = (
            f"{country} has exhausted approximately <b>{pct_int}%</b> of its fair-share allocation "
            f"and would require {remedy} to return to a Paris-compatible pathway."
        )
        if pd.notna(debt) and debt > 0:
            text += f" Outstanding carbon debt is <b>{debt:.1f} Gt</b>."
    elif pct > 85:
        text = (
            f"{country} has used approximately <b>{pct_int}%</b> of its fair-share allocation, "
            f"leaving limited room before breaching a Paris-compatible pathway."
        )
    else:
        text = (
            f"{country} retains headroom within its fair-share allocation, having used "
            f"approximately <b>{pct_int}%</b> of its equitable carbon budget to date."
        )

    gap = country_policy_gap(row)
    net_zero = row.get("pledge_year_final")
    overshoot = row.get("overshoot_year")
    if pd.notna(gap) and pd.notna(net_zero) and pd.notna(overshoot):
        if gap > 0:
            text += (
                f" Its net-zero pledge of <b>{int(net_zero)}</b> implies a policy gap of "
                f"<b>{int(gap)} years</b> beyond the {int(overshoot)} overshoot year."
            )
        else:
            text += (
                f" Its net-zero pledge of <b>{int(net_zero)}</b> is earlier than or aligned with "
                "its historical overshoot timing on paper."
            )

    justice = row.get("justice_score")
    if pd.notna(justice) and pct > 100:
        if justice < 40:
            text += f" A justice score of <b>{justice:.0f}/100</b> places it among the highest-responsibility overshooters."
        elif justice > 60:
            text += f" Despite overshoot, its justice score of <b>{justice:.0f}/100</b> is lower than many peer economies."

    return text


def render_interpretation_box(insight_html: str, label: str = "Interpretation"):
    st.html(
        f"""
        <div class="insight-box">
            <div class="insight-label">{label}</div>
            <div class="insight-text">{insight_html}</div>
        </div>
        """
    )


def render_country_profile(country: str):
    row = df_summary[df_summary["country"] == country].iloc[0]
    iso = row["iso_code"]
    hist = df_historical[df_historical["iso_code"] == iso].sort_values("year").copy()
    scen = df_scenarios[df_scenarios["iso_code"] == iso].sort_values(["scenario", "year"]).copy()

    back_col, title_col, pill_col = st.columns([0.4, 3, 1.2])
    with back_col:
        if st.button("←", help="Back"):
            st.session_state.country_profile = None
            st.rerun()
    with title_col:
        st.markdown(
            f"""
            <div style="font-size:2.6rem;font-weight:850;letter-spacing:-0.04em;margin-top:0.1rem;color:#ffffff;">
                {country} <span class="country-banner">{iso}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with pill_col:
        if pd.notna(row.get("pct_used")):
            pct_label = f"{int(round(row['pct_used']))}% fair share used"
            st.markdown(
                f"""
                <div style="text-align:right;margin-top:0.9rem;">
                    <span class="overshoot-pill">{pct_label}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    policy_gap = country_policy_gap(row)
    gap_label = f"{int(policy_gap)} yrs" if pd.notna(policy_gap) else "—"
    gap_foot = "Pledge minus overshoot year"
    overshoot_label = f"{int(row['overshoot_year'])}" if pd.notna(row.get("overshoot_year")) else "—"
    net_zero_label = f"{int(row['pledge_year_final'])}" if pd.notna(row.get("pledge_year_final")) else "—"

    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
    with r1c1:
        render_metric_card(
            "Fair Share Budget",
            safe_metric_value(row.get("fair_share_gt"), " Gt"),
            "Equitable IPCC allocation",
            accent="var(--blue)",
        )
    with r1c2:
        render_metric_card(
            "Historical Emissions",
            safe_metric_value(row.get("cum_emissions_gt"), " Gt"),
            "Cumulative CO₂ to date",
            accent="var(--green)",
        )
    with r1c3:
        debt_accent = "var(--red)" if float(row.get("debt_gt", 0) or 0) > 0 else "var(--green)"
        render_metric_card(
            "Carbon Debt",
            safe_metric_value(row.get("debt_gt"), " Gt", signed=True, digits=2),
            "Versus fair-share budget",
            accent=debt_accent,
        )
    with r1c4:
        render_metric_card(
            "Overshoot Year",
            overshoot_label,
            "Fair-share budget exceeded",
            accent="var(--red)",
        )

    r2c1, r2c2, r2c3, _ = st.columns(4)
    with r2c1:
        render_metric_card(
            "Justice Score",
            safe_metric_value(row.get("justice_score"), "/100", digits=1),
            "Carbon justice index",
            accent="var(--amber)",
        )
    with r2c2:
        render_metric_card(
            "Net-Zero Year",
            net_zero_label,
            "Current climate pledge",
            accent="var(--green)",
        )
    with r2c3:
        gap_accent = "var(--red)" if pd.notna(policy_gap) and policy_gap > 30 else "var(--amber)"
        render_metric_card(
            "Policy Gap",
            gap_label,
            gap_foot,
            accent=gap_accent,
        )

    render_interpretation_box(build_country_interpretation(row))

    tabs = st.tabs(["Historical Trends", "Debt & Overshoot", "Future Scenarios"])
    with tabs[0]:
        c1, c2 = st.columns(2)
        with c1:
            st.html('<div class="chart-panel-title">📉 Annual Emissions (Mt CO₂)</div>')
            if len(hist) > 0 and hist["co2"].notna().any():
                fig1 = px.area(hist, x="year", y="co2", labels={"co2": "Mt CO₂", "year": "Year"})
                fig1.update_traces(line_color="#24d07a", fillcolor="rgba(36,208,122,0.18)")
                apply_chart_layout(fig1)
                st.plotly_chart(fig1, use_container_width=True, config=plotly_chart_config())
            else:
                st.info("No historical emissions data available for this country.")
        with c2:
            st.html('<div class="chart-panel-title">⚡ Renewable Energy Share (%)</div>')
            if len(hist) > 0 and hist["renewables_share_energy"].notna().any():
                fig2 = px.line(hist, x="year", y="renewables_share_energy", labels={"renewables_share_energy": "%", "year": "Year"})
                fig2.update_traces(line_color="#24d07a", line_width=3)
                apply_chart_layout(fig2)
                st.plotly_chart(fig2, use_container_width=True, config=plotly_chart_config())
            else:
                st.info("No renewable share data available for this country.")

    with tabs[1]:
        c1, c2 = st.columns(2)
        with c1:
            st.html('<div class="chart-panel-title">Debt Accumulation Curve</div>')
            if len(hist) > 0:
                if "cum_emissions_gt" not in hist.columns and "cumulative_co2" in hist.columns:
                    hist["cum_emissions_gt"] = hist["cumulative_co2"] * 1e-3
                if hist["cum_emissions_gt"].notna().any():
                    fair_share = row.get("fair_share_gt", np.nan)
                    debt_series = pd.DataFrame({
                        "year": hist["year"],
                        "Cumulative emissions": hist["cum_emissions_gt"],
                        "Fair share budget": np.linspace(0, fair_share, len(hist)) if pd.notna(fair_share) else np.nan,
                    })
                    fig_debt = go.Figure()
                    fig_debt.add_trace(go.Scatter(x=debt_series["year"], y=debt_series["Cumulative emissions"], mode="lines", name="Cumulative emissions", line=dict(color="#24d07a", width=3)))
                    if pd.notna(fair_share):
                        fig_debt.add_trace(go.Scatter(x=debt_series["year"], y=debt_series["Fair share budget"], mode="lines", name="Fair share budget", line=dict(color="#4fa3ff", width=2, dash="dash")))
                    if pd.notna(row.get("overshoot_year")):
                        fig_debt.add_vline(x=int(row["overshoot_year"]), line_dash="dot", line_color="#ff4d73", annotation_text="Overshoot")
                    apply_chart_layout(fig_debt, showlegend=True)
                    st.plotly_chart(fig_debt, use_container_width=True, config=plotly_chart_config())
                else:
                    st.info("No cumulative emissions data available.")
            else:
                st.info("No historical panel for debt curve.")
        with c2:
            st.html('<div class="chart-panel-title">Overshoot Timeline</div>')
            overshoot = int(row["overshoot_year"]) if pd.notna(row.get("overshoot_year")) else None
            pledge = int(row["pledge_year_final"]) if pd.notna(row.get("pledge_year_final")) else None
            if overshoot:
                fig_tl = go.Figure()
                fig_tl.add_trace(go.Scatter(x=[overshoot, pledge or 2050], y=[country, country], mode="lines+markers", line=dict(color="#ff4d73", width=4), marker=dict(size=10)))
                fig_tl.add_vline(x=overshoot, line_dash="dot", line_color="#ff4d73")
                if pledge:
                    fig_tl.add_vline(x=pledge, line_dash="dot", line_color="#24d07a")
                apply_chart_layout(fig_tl, height=280, title="Overshoot year → Net-zero pledge", xaxis_title="Year")
                fig_tl.update_yaxes(visible=False)
                st.plotly_chart(fig_tl, use_container_width=True, config=plotly_chart_config())
            else:
                st.info("No overshoot year recorded for this country.")

    with tabs[2]:
        st.html('<div class="chart-panel-title">Future Carbon Debt Scenarios</div>')
        if len(scen) > 0 and scen["debt_gt"].notna().any():
            fig3 = px.line(scen, x="year", y="debt_gt", color="scenario", markers=True, labels={"debt_gt": "Projected Debt (Gt)", "year": "Year"})
            apply_chart_layout(fig3, legend_title_text="Scenario")
            st.plotly_chart(fig3, use_container_width=True, config=plotly_chart_config())
        else:
            st.info("No scenario data available for this country.")

    st.markdown(
        '<div class="verified-footer">🛡 Verified Science-Based Approach</div>',
        unsafe_allow_html=True,
    )


def build_executive_insight(summary: pd.DataFrame, bench_15_50) -> str:
    if summary is None or len(summary) == 0 or summary["debt_gt"].isna().all():
        return (
            "This dashboard compares national cumulative emissions against IPCC AR6 fair-share "
            "budgets to reveal who has overshot—and who retains unused atmospheric capacity."
        )

    debtor = summary.loc[summary["debt_gt"].idxmax()]
    creditor = summary.loc[summary["debt_gt"].idxmin()]
    overshoot_n = int((summary["debt_gt"] > 0).sum())
    creditor_n = int((summary["debt_gt"] < 0).sum())
    creditor_capacity = abs(float(creditor["debt_gt"]))

    insight = (
        f"<b>{debtor['country']}</b> has accumulated the highest carbon debt "
        f"({debtor['debt_gt']:.0f} Gt), while <b>{creditor['country']}</b> remains "
        f"the largest carbon creditor ({creditor_capacity:.0f} Gt of unused fair-share capacity). "
        f"{overshoot_n} countries have overshot their fair-share allocation"
    )
    if creditor_n > 0:
        insight += f"; {creditor_n} remain net creditors under an equity-based budget."
    else:
        insight += "."

    if bench_15_50 is not None and pd.notna(bench_15_50.get("remain2025_gt")):
        remain = float(bench_15_50["remain2025_gt"])
        years_left = max(1, round(remain / 40.0))
        insight += (
            " Current global trajectories are incompatible with an equitable allocation "
            f"of the remaining 1.5°C carbon budget. At present emission rates, the remaining "
            f"<b>{remain:.0f} Gt</b> budget would be exhausted in less than <b>{years_left}</b> years."
        )
    else:
        insight += (
            " Current global trajectories are incompatible with an equitable allocation "
            "of the remaining 1.5°C carbon budget."
        )

    return insight


def render_key_insight_box(question: str, insight_html: str, label: str = "Key Insight"):
    question_html = f'<div class="insight-question">{question}</div>' if question else ""
    st.html(
        f"""
        <div class="insight-box">
            <div class="insight-label">{label}</div>
            {question_html}
            <div class="insight-text">{insight_html}</div>
        </div>
        """
    )


@st.cache_data
def climate_warning_image_uri() -> str:
    import base64

    image_path = ASSETS_DIR / "climate-factory.jpg"
    if image_path.exists():
        encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
        return f"data:image/jpeg;base64,{encoded}"
    return (
        "https://images.pexels.com/photos/257700/pexels-photo-257700.jpeg"
        "?auto=compress&cs=tinysrgb&w=1200"
    )


@st.cache_data
def hero_earth_image_uri() -> str:
    import base64

    image_path = ASSETS_DIR / "hero-earth-limb.png"
    if image_path.exists():
        encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
        return f"data:image/png;base64,{encoded}"
    return ""


def render_executive_hero():
    earth_uri = hero_earth_image_uri()
    earth_style = f"background-image:url('{earth_uri}');" if earth_uri else ""
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-earth" style="{earth_style}"></div>
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <div class="badge">Critical Analytics</div>
                <div class="hero-title" style="color:#ffffff !important;">
                    Carbon Budget Tracker: Who Owes the Atmosphere?
                </div>
                <div class="hero-text" style="color:#e8eef5 !important;">
                    Exploration of national carbon budgets based on IPCC AR6 data. Quantifying the divide between
                    cumulative historical emissions and planetary fair-share allocations.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_climate_warning(bench_15_50):
    remain = bench_15_50["remain2025_gt"] if bench_15_50 is not None else 362
    image_uri = climate_warning_image_uri()
    st.markdown(
        f"""
        <div class="climate-warning-card">
            <div class="climate-warning-header">
                <div class="climate-warning-icon">!</div>
                <div class="climate-warning-title">Climate Warning</div>
            </div>
            <div class="climate-warning-image" style="
                background-image:
                    linear-gradient(180deg, rgba(0,0,0,0.20), rgba(0,0,0,0.78)),
                    url('{image_uri}');
            ">
                <div class="climate-warning-image-text">
                    Global budget for 1.5°C is nearly exhausted at current rates.
                </div>
            </div>
            <div class="climate-warning-body">
                <div class="small-muted" style="line-height:1.6;margin-bottom:0.75rem;">
                    Remaining 1.5°C (50%) budget from 2025:
                    <b style="color:#ffffff;">{remain:.0f} Gt CO₂</b>.
                </div>
                <div class="small-muted" style="font-style:italic;line-height:1.55;">
                    The cumulative net global CO₂ emissions from 1850–2019 were 2400 ± 240 GtCO₂.
                    The remaining carbon budget for 1.5°C is less than 500 GtCO₂. — IPCC AR6 SYR
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
    ai_debt = load_csv_if_exists(PROCESSED_DIR / "project_debt_scenarios_with_ai.csv")

    benchmarks = load_csv_if_exists(PROCESSED_DIR / "ar6_adjusted_budgets.csv")
    drivers = load_csv_if_exists(PROCESSED_DIR / "step2_overshoot_drivers.csv")
    ai_overshoot = load_csv_if_exists(PROCESSED_DIR / "ai_overshoot_years_by_scenario.csv")

    return summary, historical, scenarios, benchmarks, drivers, ai_overshoot, ai_debt


# ---------------------------------------------------------
# DATA LOADING PRIORITY
# project files -> uploaded files -> demo data
# ---------------------------------------------------------
project_summary, project_historical, project_scenarios, project_benchmarks, project_drivers, project_ai_overshoot, project_ai_debt = load_project_data()

if "page" not in st.session_state:
    st.session_state.page = "Executive Dashboard"
if "country_profile" not in st.session_state:
    st.session_state.country_profile = None
if "ai_country" not in st.session_state:
    st.session_state.ai_country = "Germany"
if "driver_country" not in st.session_state:
    st.session_state.driver_country = "Germany"

summary_file = None
historical_file = None
scenario_file = None
benchmark_file = None
show_ai = False
ai_twh_2030 = 1200
ai_twh_2050 = 2500
clean_share_2050 = 70
source_mode = "demo"

st.sidebar.html(
    """
    <div class="brand-wrap">
        <div class="brand-title">🍃 Carbon Budget Tracker</div>
        <div class="brand-sub">IPCC AR6 Analytics Engine</div>
    </div>
    """
)

NAV_PAGES = [
    "Executive Dashboard",
    "Country Explorer",
    "Carbon Debt Rankings",
    "Policy Gap Analysis",
    "AI Scenario Explorer",
    "Overshoot Drivers",
    "Global Benchmarks",
]
for nav_page in NAV_PAGES:
    if st.sidebar.button(
        nav_page,
        key=f"nav_{nav_page}",
        use_container_width=True,
        type="primary" if st.session_state.page == nav_page else "secondary",
    ):
        st.session_state.page = nav_page
        st.session_state.country_profile = None

with st.sidebar.expander("Data & advanced options", expanded=False):
    st.markdown("### Data Input")
    summary_file = st.file_uploader("Upload summary CSV", type=["csv"], key="summary")
    historical_file = st.file_uploader("Upload historical panel CSV", type=["csv"], key="historical")
    scenario_file = st.file_uploader("Upload scenarios CSV", type=["csv"], key="scenario")
    benchmark_file = st.file_uploader("Upload benchmarks CSV", type=["csv"], key="benchmarks")
    show_ai = st.checkbox("Show AI / datacentre overlay", value=False)
    if show_ai:
        ai_twh_2030 = st.slider("AI electricity 2030 (TWh)", 500, 3000, 1200, 100)
        ai_twh_2050 = st.slider("AI electricity 2050 (TWh)", 1000, 8000, 2500, 200)
        clean_share_2050 = st.slider("Clean grid share by 2050 (%)", 30, 100, 70, 5)

try:
    if project_summary is not None:
        df_summary = add_justice_scores(enrich_summary_from_drivers(normalize_summary(project_summary)))
        source_mode = "project"
    elif summary_file is not None:
        df_summary = add_justice_scores(normalize_summary(pd.read_csv(summary_file)))
        source_mode = "upload"
    else:
        df_summary = add_justice_scores(normalize_summary(get_default_summary()))

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

    df_summary = enrich_pledge_from_scenarios(df_summary, df_scenarios)

except Exception as e:
    st.sidebar.error(f"Data loading error: {e}")
    df_summary = add_justice_scores(normalize_summary(get_default_summary()))
    df_historical = normalize_historical(get_default_historical())
    df_scenarios = normalize_scenarios(get_default_scenarios())
    df_benchmarks = normalize_benchmarks(get_default_benchmarks())
    source_mode = "demo"
    df_summary = enrich_pledge_from_scenarios(df_summary, df_scenarios)

st.sidebar.markdown("---")
if source_mode == "project":
    st.sidebar.success("Using processed_data files.")
elif source_mode == "upload":
    st.sidebar.success("Using uploaded summary file.")
else:
    st.sidebar.info("Using demo data.")
st.sidebar.markdown(f"🟢 **System Status:** {'Nominal' if source_mode != 'demo' else 'Demo Mode'}")

page = st.session_state.page
page_titles = {
    "Executive Dashboard": "Dashboard",
    "Country Explorer": "Country Explorer",
    "Carbon Debt Rankings": "Rankings",
    "Policy Gap Analysis": "Policy Gap",
    "AI Scenario Explorer": "AI Scenarios",
    "Overshoot Drivers": "Drivers",
    "Global Benchmarks": "Benchmarks",
}

# ---------------------------------------------------------
# COMMON CALCULATIONS
# ---------------------------------------------------------
topbar_left, topbar_mid, topbar_sync, topbar_ver = st.columns([1.2, 2.6, 0.9, 0.8])
with topbar_left:
    st.markdown(
        f'<div class="topbar-title">{page_titles.get(page, page)}</div>',
        unsafe_allow_html=True,
    )
with topbar_mid:
    search_global = st.text_input(
        "Search ISO or Country...",
        placeholder="Search ISO or Country...",
        label_visibility="collapsed",
        key="global_search",
    )
with topbar_sync:
    if st.button("Sync Data", use_container_width=True):
        load_project_data.clear()
        st.rerun()
with topbar_ver:
    st.markdown('<div class="version-tag">2026.03.16-V1</div>', unsafe_allow_html=True)
st.markdown('<div style="border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:1rem;"></div>', unsafe_allow_html=True)
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
avg_per_capita = df_summary["debt_per_capita"].abs().mean(skipna=True) if "debt_per_capita" in df_summary.columns else np.nan

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
# PAGE: EXECUTIVE DASHBOARD
# ---------------------------------------------------------
if page == "Executive Dashboard":
    render_executive_hero()

    hero_actions = st.columns([1, 1, 4])
    with hero_actions[0]:
        if st.button("Start Exploration", type="primary", use_container_width=True):
            st.session_state.page = "Country Explorer"
            st.session_state.country_profile = "Germany" if "Germany" in df_summary["country"].values else None
            st.rerun()
    with hero_actions[1]:
        if st.button("IPCC Methodology", use_container_width=True):
            st.session_state.page = "Global Benchmarks"
            st.session_state.country_profile = None
            st.rerun()

    render_key_insight_box(
        "Who owes the atmosphere?",
        build_executive_insight(df_summary, bench_15_50),
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if highest_debt is not None:
            render_metric_card(
                "Highest Debt",
                f"{highest_debt['debt_gt']:.1f} Gt",
                highest_debt["country"],
                accent="var(--red)",
                icon="↗",
            )
    with c2:
        if lowest_debt is not None:
            render_metric_card(
                "Net Creditor",
                f"{lowest_debt['debt_gt']:.1f} Gt",
                lowest_debt["country"],
                accent="var(--green)",
                icon="↘",
            )
    with c3:
        render_metric_card(
            "Avg Per Capita",
            safe_metric_value(avg_per_capita, " t"),
            "Global metric",
            accent="var(--blue)",
            icon="🌐",
        )
    with c4:
        remain_label = f"{bench_15_50['remain2025_gt']:.0f} Gt" if bench_15_50 is not None else "—"
        render_metric_card(
            "Remaining 1.5°C Budget",
            remain_label,
            "Global budget from 2025",
            accent="var(--green)",
            icon="🍃",
        )

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    col_table, col_warning = st.columns([2, 1])
    with col_table:
        leaderboard = (
            df_summary[["iso_code", "country", "debt_gt", "pct_used"]]
            .sort_values("debt_gt", ascending=False)
            .head(10)
            .copy()
        )
        leaderboard = leaderboard.assign(
            **{
                "Debt (Gt)": leaderboard["debt_gt"].map(lambda x: f"{x:,.1f}" if pd.notna(x) else "—"),
                "Budget Used": leaderboard["pct_used"].map(lambda x: f"{int(x)}%" if pd.notna(x) else "—"),
            }
        )
        leaderboard = leaderboard.rename(columns={"iso_code": "ISO", "country": "Country"})[["ISO", "Country", "Debt (Gt)", "Budget Used"]]
        st.html(
            f"""
            <div class="panel">
                <div class="panel-header-row">
                    <div>
                        <div class="panel-title">Global Carbon Debt Leaderboard</div>
                        <div class="small-muted">Countries with the highest historical fair-share overshoot.</div>
                    </div>
                    <div class="view-all-link">View All &gt;</div>
                </div>
                {build_leaderboard_table(leaderboard)}
            </div>
            """
        )
        st.download_button("Export full table (CSV)", df_summary.to_csv(index=False).encode("utf-8"), "carbon_budget_summary.csv", "text/csv")

    with col_warning:
        render_climate_warning(bench_15_50)

    with st.expander("Global Carbon Debt Map"):
        try:
            fig_map = px.choropleth(
                df_filtered_global,
                locations="iso_code",
                locationmode="ISO-3",
                color="debt_gt",
                hover_name="country",
                hover_data={"iso_code": True, "debt_gt": ":.2f", "pct_used": ":.0f"},
                color_continuous_scale="RdYlGn_r",
            )
            fig_map.update_layout(
                paper_bgcolor="#0f141d",
                plot_bgcolor="#0f141d",
                font=dict(color=CHART_LABEL_COLOR),
                title=dict(font=dict(color=CHART_TITLE_COLOR)),
                margin=dict(l=0, r=0, t=10, b=0),
                coloraxis_colorbar=dict(
                    tickfont=dict(color=CHART_TICK_COLOR),
                    title=dict(font=dict(color=CHART_LABEL_COLOR)),
                    title_text="Debt (Gt)",
                ),
            )
            fig_map.update_geos(showframe=False, showcoastlines=False, bgcolor="#0f141d", projection_type="natural earth")
            st.plotly_chart(fig_map, use_container_width=True)
        except Exception as e:
            st.warning(f"Map could not be rendered: {e}")

# ---------------------------------------------------------
# PAGE: COUNTRY EXPLORER / COUNTRY PROFILE
# ---------------------------------------------------------
elif page == "Country Explorer":
    if st.session_state.country_profile:
        render_country_profile(st.session_state.country_profile)
    else:
        st.markdown('<div class="section-subtitle">Browse country-level carbon debt, fair share, and overshoot timing.</div>', unsafe_allow_html=True)

        explorer_search = search_global
        df_explorer = df_summary.copy()
        if explorer_search:
            df_explorer = df_explorer[
                df_explorer["country"].str.contains(explorer_search, case=False, na=False)
                | df_explorer["iso_code"].str.contains(explorer_search, case=False, na=False)
            ].copy()

        country_options = df_explorer["country"].dropna().sort_values().unique().tolist()
        default_country = "Germany" if "Germany" in country_options else (country_options[0] if country_options else None)
        pick_col, open_col = st.columns([3, 1])
        with pick_col:
            selected_country = st.selectbox(
                "Open country profile",
                country_options,
                index=country_options.index(default_country) if default_country in country_options else 0,
                label_visibility="collapsed",
            )
        with open_col:
            if st.button("Open Profile", type="primary", use_container_width=True) and selected_country:
                st.session_state.country_profile = selected_country
                st.rerun()

        display = (
            df_explorer[["iso_code", "country", "debt_gt", "pct_used"]]
            .sort_values("debt_gt", ascending=False)
            .head(40)
            .copy()
        )
        display = display.assign(
            **{
                "Debt (Gt)": display["debt_gt"].map(lambda x: f"{x:,.2f}" if pd.notna(x) else "—"),
                "Budget Used": display["pct_used"].map(lambda x: f"{int(round(x))}%" if pd.notna(x) else "—"),
            }
        )
        display = display.rename(columns={"iso_code": "ISO", "country": "Country"})[["ISO", "Country", "Debt (Gt)", "Budget Used"]]
        st.markdown(build_leaderboard_table(display), unsafe_allow_html=True)
        st.download_button("Export filtered table (CSV)", df_explorer.to_csv(index=False).encode("utf-8"), "filtered_countries.csv", "text/csv")

# ---------------------------------------------------------
# PAGE: CARBON DEBT RANKINGS
# ---------------------------------------------------------
elif page == "Carbon Debt Rankings":
    st.markdown(
        '<div class="section-subtitle">Responsibility lens: who owes the atmosphere, and who remains within fair share?</div>',
        unsafe_allow_html=True,
    )

    rank_df = df_summary.copy()
    rank_df["region"] = rank_df["iso_code"].map(iso_region)

    render_key_insight_box(
        "Who bears the burden — and who retains capacity?",
        build_rankings_interpretation(rank_df),
    )

    dl1, dl2, dl3 = st.columns([1.15, 1.15, 1.7])
    with dl1:
        st.download_button(
            "Download Top 20 Debtors (CSV)",
            build_rankings_export(rank_df, n=20, debtors=True).to_csv(index=False).encode("utf-8"),
            "top_20_carbon_debtors.csv",
            "text/csv",
            use_container_width=True,
        )
    with dl2:
        st.download_button(
            "Download Top 20 Creditors (CSV)",
            build_rankings_export(rank_df, n=20, debtors=False).to_csv(index=False).encode("utf-8"),
            "top_20_carbon_creditors.csv",
            "text/csv",
            use_container_width=True,
        )
    with dl3:
        st.markdown(
            '<div class="small-muted" style="padding-top:0.45rem;line-height:1.55;">'
            "Exports include ISO, region, debt, budget use, justice score, and pledge metadata."
            "</div>",
            unsafe_allow_html=True,
        )

    rank_tabs = st.tabs(["Debtors & Creditors", "Justice Lens", "Regional View", "World Map"])

    with rank_tabs[0]:
        c1, c2 = st.columns(2)
        debtors = rank_df.nlargest(12, "debt_gt")
        creditors = rank_df.nsmallest(12, "debt_gt")
        with c1:
            st.plotly_chart(
                ranked_country_bar(debtors, "debt_gt", "Top carbon debtors", invert=True),
                use_container_width=True,
                config=plotly_chart_config(),
            )
        with c2:
            st.plotly_chart(
                ranked_country_bar(creditors, "debt_gt", "Top carbon creditors", invert=False),
                use_container_width=True,
                config=plotly_chart_config(),
            )

        fig_rank = px.bar(
            rank_df.sort_values("debt_gt", ascending=False).head(20),
            x="country",
            y="debt_gt",
            color="justice_score",
            color_continuous_scale="RdYlGn",
            labels={"debt_gt": "Carbon debt (Gt)", "country": "Country", "justice_score": "Justice score"},
            title="Global debt ranking (interactive)",
        )
        apply_chart_layout(fig_rank, height=480, xaxis=dict(tickangle=-35))
        st.plotly_chart(fig_rank, use_container_width=True, config=plotly_chart_config())

    with rank_tabs[1]:
        justice_top = rank_df.sort_values("justice_score", ascending=False).head(20)
        c1, c2 = st.columns([1.2, 1])
        with c1:
            fig_justice_bar = px.bar(
                justice_top,
                x="justice_score",
                y="country",
                orientation="h",
                color="debt_gt",
                color_continuous_scale="RdYlGn_r",
                hover_data={"pct_used": ":.0f", "debt_gt": ":.2f"},
                labels={"justice_score": "Justice score", "country": "Country", "debt_gt": "Debt (Gt)"},
                title="Carbon Justice Score — top performers",
            )
            apply_chart_layout(fig_justice_bar, height=560, yaxis=dict(categoryorder="total ascending"))
            st.plotly_chart(fig_justice_bar, use_container_width=True, config=plotly_chart_config())
        with c2:
            fig_justice_low = px.bar(
                rank_df.sort_values("justice_score", ascending=True).head(15),
                x="justice_score",
                y="country",
                orientation="h",
                color="justice_score",
                color_continuous_scale="Reds",
                labels={"justice_score": "Justice score", "country": "Country"},
                title="Lowest justice scores",
            )
            apply_chart_layout(fig_justice_low, height=560, yaxis=dict(categoryorder="total ascending"))
            st.plotly_chart(fig_justice_low, use_container_width=True, config=plotly_chart_config())

        st.plotly_chart(justice_scatter(rank_df), use_container_width=True, config=plotly_chart_config())

    with rank_tabs[2]:
        regional = (
            rank_df.groupby("region", as_index=False)
            .agg(total_debt_gt=("debt_gt", "sum"), countries=("iso_code", "count"), avg_justice=("justice_score", "mean"))
            .sort_values("total_debt_gt", ascending=False)
        )
        c1, c2 = st.columns(2)
        with c1:
            fig_region = px.bar(
                regional,
                x="region",
                y="total_debt_gt",
                color="avg_justice",
                color_continuous_scale="RdYlGn",
                hover_data={"countries": True, "avg_justice": ":.1f"},
                labels={"region": "Region", "total_debt_gt": "Total debt (Gt)", "avg_justice": "Avg justice score"},
                title="Regional carbon debt totals",
            )
            apply_chart_layout(fig_region, height=420)
            st.plotly_chart(fig_region, use_container_width=True, config=plotly_chart_config())
        with c2:
            rank_df_treemap = rank_df.copy()
            rank_df_treemap["abs_debt"] = rank_df_treemap["debt_gt"].abs().clip(lower=0.01)
            fig_treemap = px.treemap(
                rank_df_treemap,
                path=["region", "country"],
                values="abs_debt",
                color="justice_score",
                color_continuous_scale="RdYlGn",
                hover_data={"pct_used": ":.0f", "debt_gt": ":.2f"},
                title="Debt by region and country",
            )
            apply_chart_layout(fig_treemap, height=420)
            st.plotly_chart(fig_treemap, use_container_width=True, config=plotly_chart_config())

    with rank_tabs[3]:
        try:
            fig_map = px.choropleth(
                rank_df,
                locations="iso_code",
                locationmode="ISO-3",
                color="justice_score",
                hover_name="country",
                hover_data={"debt_gt": ":.2f", "pct_used": ":.0f", "region": True},
                color_continuous_scale="RdYlGn",
                labels={"justice_score": "Justice score"},
                title="Global Carbon Justice Score map",
            )
            apply_chart_layout(fig_map, height=560, margin=dict(l=0, r=0, t=40, b=0))
            fig_map.update_geos(showframe=False, showcoastlines=True, bgcolor="#0f141d", projection_type="natural earth")
            st.plotly_chart(fig_map, use_container_width=True, config=plotly_chart_config())
        except Exception as e:
            st.warning(f"Map could not be rendered: {e}")

    st.markdown("#### Drill into a country")
    rank_country = st.selectbox(
        "Open country profile from rankings",
        rank_df["country"].dropna().sort_values().unique().tolist(),
        key="rank_country_pick",
    )
    if st.button("Open Country Profile", type="primary"):
        st.session_state.page = "Country Explorer"
        st.session_state.country_profile = rank_country
        st.rerun()

# ---------------------------------------------------------
# PAGE: POLICY GAP ANALYSIS
# ---------------------------------------------------------
elif page == "Policy Gap Analysis":
    st.markdown(
        '<div class="section-subtitle">Are current climate pledges sufficient to eliminate carbon debt?</div>',
        unsafe_allow_html=True,
    )

    render_key_insight_box(
        "",
        (
            "Many countries exhausted their fair-share carbon budgets decades before their announced "
            "net-zero targets. The resulting <b>policy gap</b> represents the number of years between "
            "budget overshoot and planned climate neutrality. Larger gaps indicate greater reliance on "
            "future mitigation, carbon removals, or delayed action."
        ),
        label="Policy Reality Check",
    )

    gap_df = prepare_policy_gap_df(df_summary)
    complete = gap_df.dropna(subset=["net_zero_year", "policy_gap_years"]).copy()

    avg_gap = complete["policy_gap_years"].mean() if len(complete) else np.nan
    overshoot_count = int((df_summary["debt_gt"] > 0).sum()) if "debt_gt" in df_summary.columns else 0
    largest_gap = complete["policy_gap_years"].max() if len(complete) else np.nan
    within_count = int((df_summary["debt_gt"] <= 0).sum()) if "debt_gt" in df_summary.columns else 0

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card(
            "Average Policy Gap",
            f"{avg_gap:.0f} years" if pd.notna(avg_gap) else "—",
            "Mean years between overshoot and pledge",
            accent="var(--amber)",
        )
    with m2:
        render_metric_card(
            "Countries Overshooting",
            str(overshoot_count),
            "Nations with positive carbon debt",
            accent="var(--red)",
        )
    with m3:
        render_metric_card(
            "Largest Gap",
            f"{int(largest_gap)} years" if pd.notna(largest_gap) else "—",
            "Maximum policy gap in dataset",
            accent="var(--red)",
        )
    with m4:
        render_metric_card(
            "Within Fair Share",
            str(within_count),
            "Countries still under equitable budget",
            accent="var(--green)",
        )

    if len(complete) == 0:
        st.info("Policy gap analysis needs both overshoot year and net-zero pledge data.")
    else:
        rank_col, quad_col = st.columns([1, 1.15])
        with rank_col:
            st.markdown("#### Who needs the biggest catch-up?")
            render_catchup_ranking_table(complete)

        with quad_col:
            st.markdown("#### Policy gap quadrants")
            fig_quad = build_policy_gap_quadrant_plot(complete)
            if fig_quad is not None:
                st.plotly_chart(fig_quad, use_container_width=True, config=plotly_chart_config())

        st.markdown("#### Country comparison")
        all_countries = df_summary["country"].dropna().sort_values().unique().tolist()
        default_compare = [c for c in ["Germany", "United States", "India"] if c in all_countries]
        compare_countries = st.multiselect(
            "Select countries to compare",
            all_countries,
            default=default_compare,
            max_selections=5,
            key="policy_compare_countries",
        )
        render_policy_comparison_table(df_summary, compare_countries)

        st.markdown("#### Policy interpretation")
        default_policy = "Germany" if "Germany" in all_countries else all_countries[0]
        policy_country = st.selectbox(
            "Select country for interpretation",
            all_countries,
            index=all_countries.index(default_policy),
            key="policy_interp_country",
        )
        policy_row = df_summary[df_summary["country"] == policy_country].iloc[0]
        render_interpretation_box(
            build_policy_interpretation(policy_row),
            label="Policy Interpretation",
        )

        st.markdown("#### Largest policy gaps")
        gap_bar_df = complete.sort_values("policy_gap_years", ascending=True).tail(15)
        fig_gap_bar = px.bar(
            gap_bar_df,
            x="policy_gap_years",
            y="country",
            orientation="h",
            color="debt_gt",
            color_continuous_scale="Reds",
            hover_data={"overshoot_year": ":.0f", "net_zero_year": ":.0f", "justice_score": ":.1f"},
            labels={
                "policy_gap_years": "Gap (years)",
                "country": "Country",
                "debt_gt": "Debt (Gt)",
                "overshoot_year": "Overshoot year",
                "net_zero_year": "Net-zero year",
            },
            title="Years between overshoot and net-zero pledge",
        )
        apply_chart_layout(fig_gap_bar, height=480, yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig_gap_bar, use_container_width=True, config=plotly_chart_config())

        with st.expander("Overshoot-to-pledge timeline and full data"):
            st.plotly_chart(build_policy_gap_dumbbell(gap_df), use_container_width=True, config=plotly_chart_config())
            table = complete[
                ["country", "debt_gt", "overshoot_year", "net_zero_year", "policy_gap_years", "justice_score"]
            ].copy()
            table["overshoot_year"] = table["overshoot_year"].astype("Int64")
            table["net_zero_year"] = table["net_zero_year"].astype("Int64")
            table["policy_gap_years"] = table["policy_gap_years"].astype(int)
            table["severity"] = table["policy_gap_years"].map(lambda g: policy_gap_severity(g)[0])
            table = table.sort_values("policy_gap_years", ascending=False)
            table.columns = [
                "Country", "Debt (Gt)", "Overshoot Year", "Net Zero Year",
                "Gap (years)", "Justice Score", "Severity",
            ]
            st.dataframe(table, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# PAGE: AI SCENARIO EXPLORER
# ---------------------------------------------------------
elif page == "AI Scenario Explorer":
    render_research_question_box(
        "How sensitive are national carbon budgets to<br>AI-driven electricity demand growth?"
    )

    ai_countries = df_summary["country"].dropna().sort_values().unique().tolist()
    default_ai = "Germany" if "Germany" in ai_countries else ai_countries[0]
    ai_country = st.selectbox(
        "Select country",
        ai_countries,
        index=ai_countries.index(default_ai),
        key="ai_country_select",
    )
    ai_row = df_summary[df_summary["country"] == ai_country].iloc[0]
    ai_iso = ai_row["iso_code"]
    ai_scen = df_scenarios[df_scenarios["iso_code"] == ai_iso].sort_values(["scenario", "year"])
    ai_table = build_ai_scenario_table(ai_country, ai_iso, ai_row, ai_scen, project_ai_overshoot, project_ai_debt)
    chart_df = prepare_ai_chart_df(ai_table)
    global_ai_rank = build_global_ai_vulnerability_ranking(df_summary, project_ai_overshoot, project_ai_debt)

    render_ai_risk_assessment_box(build_ai_risk_assessment_html(ai_country, chart_df))

    baseline_debt = float(chart_df["Carbon Debt (Gt)"].iloc[0])
    worst_debt = float(chart_df["Carbon Debt (Gt)"].iloc[-1])
    debt_increase = worst_debt - baseline_debt
    debt_growth_pct = ai_debt_growth_pct(baseline_debt, worst_debt)
    years_accelerated = int(chart_df["Overshoot Year"].iloc[0] - chart_df["Overshoot Year"].iloc[-1])
    vuln_label, vuln_color = ai_vulnerability_class(debt_growth_pct=debt_growth_pct)
    global_rank, global_total, global_pctile = get_ai_country_position(global_ai_rank, ai_country)
    global_median_growth = (
        float(global_ai_rank["debt_growth_pct"].median()) if not global_ai_rank.empty else np.nan
    )

    render_ai_comparative_context_box(
        build_ai_comparative_context_html(ai_country, debt_growth_pct, global_ai_rank)
    )

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        render_metric_card("Baseline Debt", f"{baseline_debt:.1f} Gt", "Current carbon debt", accent="var(--blue)")
    with m2:
        render_metric_card("AI +50% Debt", f"{worst_debt:.1f} Gt", "High-growth scenario", accent="var(--red)")
    with m3:
        render_metric_card("Overshoot Acceleration", f"{years_accelerated} yrs", "Earlier under AI +50%", accent="var(--amber)")
    with m4:
        render_metric_card("Debt Increase", f"+{debt_increase:.1f} Gt", "AI +50% vs baseline", accent="var(--red)")
    with m5:
        render_metric_card(
            "Debt Growth",
            f"+{debt_growth_pct:.0f}%",
            f"Global rank #{global_rank} of {global_total}" if global_rank else "AI +50% vs baseline",
            accent=vuln_color,
        )

    rank_col, vuln_col = st.columns([1.35, 1])
    with rank_col:
        st.markdown("#### Which countries are most vulnerable to AI-driven overshoot?")
        render_global_ai_ranking_table(global_ai_rank)
    with vuln_col:
        st.markdown("#### AI vulnerability classification")
        rank_display = f"#{global_rank} of {global_total}" if global_rank else "—"
        st.html(
            f"""
            <div class="panel" style="min-height: 280px;">
                <div class="panel-title">{ai_country}</div>
                <div style="margin-top:1.2rem;">
                    <div class="metric-label">Debt growth (AI +50%)</div>
                    <div class="metric-value" style="color:#ff4d73 !important;font-size:2.4rem;">+{debt_growth_pct:.0f}%</div>
                </div>
                <div style="margin-top:1.2rem;padding:0.85rem 1rem;border-radius:10px;
                    background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);">
                    <div class="metric-label">AI vulnerability rank</div>
                    <div style="font-size:1.55rem;font-weight:850;color:#ffffff;margin-top:0.35rem;">{rank_display}</div>
                </div>
                <div style="margin-top:1rem;padding:0.85rem 1rem;border-radius:10px;
                    background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);">
                    <div class="metric-label">Classification</div>
                    <div style="font-size:1.55rem;font-weight:850;color:{vuln_color};margin-top:0.35rem;">
                        {vuln_label}
                    </div>
                </div>
                <div class="small-muted" style="margin-top:1rem;line-height:1.55;">
                    {AI_RISK_BANDS_TEXT}
                </div>
            </div>
            """
        )

    c1, c2 = st.columns(2)
    with c1:
        fig_ai_debt = px.bar(
            chart_df,
            x="Scenario",
            y="Carbon Debt (Gt)",
            color="Carbon Debt (Gt)",
            color_continuous_scale="Reds",
            hover_data={"Debt Increase (Gt)": ":.2f", "Overshoot Year": ":.0f"},
            labels={"Carbon Debt (Gt)": "Carbon debt (Gt)", "Scenario": "Scenario"},
            title="Carbon debt increase under AI scenarios",
        )
        apply_chart_layout(fig_ai_debt, height=420, showlegend=False)
        st.plotly_chart(fig_ai_debt, use_container_width=True, config=plotly_chart_config())

    with c2:
        fig_ai_year = px.line(
            chart_df,
            x="Scenario",
            y="Overshoot Year",
            markers=True,
            hover_data={"Carbon Debt (Gt)": ":.2f", "Debt Increase (Gt)": ":.2f"},
            labels={"Overshoot Year": "Projected overshoot year", "Scenario": "Scenario"},
            title="AI pulls overshoot earlier",
        )
        fig_ai_year.update_traces(line_color="#ff4d73", line_width=3, marker=dict(size=10))
        apply_chart_layout(fig_ai_year, height=420)
        st.plotly_chart(fig_ai_year, use_container_width=True, config=plotly_chart_config())

    d1, d2 = st.columns(2)
    with d1:
        render_ai_global_position_panel(
            ai_country,
            global_rank,
            global_total,
            global_pctile,
            vuln_label,
            vuln_color,
            debt_growth_pct,
            global_median_growth,
        )
        render_ai_interpretation_box(
            build_ai_interpretation_html(
                ai_country, chart_df, global_ai_rank, debt_growth_pct, global_rank, global_total
            )
        )
    with d2:
        st.plotly_chart(build_ai_debt_increase_chart(chart_df), use_container_width=True, config=plotly_chart_config())

    st.markdown("#### Scenario comparison")
    render_ai_scenario_comparison_table(chart_df)

    with st.expander("View AI scenario data table"):
        st.dataframe(format_ai_scenario_display(ai_table), use_container_width=True, hide_index=True)

    if project_ai_overshoot is None and project_ai_debt is None:
        st.caption(
            "Using modelled AI sensitivity scenarios until "
            "`ai_overshoot_years_by_scenario.csv` or `project_debt_scenarios_with_ai.csv` "
            "is added to `processed_data/`."
        )
    else:
        st.caption(
            "AI scenario curves use project pathway files where available; otherwise "
            "country-specific sensitivity estimates are applied from fair-share debt metrics."
        )

# ---------------------------------------------------------
# PAGE: OVERSHOOT DRIVERS
# ---------------------------------------------------------
elif page == "Overshoot Drivers":
    render_research_question_box(
        "What structural factors contributed most to this country's carbon budget overshoot?"
    )

    driver_countries = df_summary["country"].dropna().sort_values().unique().tolist()
    default_driver = "Germany" if "Germany" in driver_countries else driver_countries[0]
    driver_country = st.selectbox(
        "Select country",
        driver_countries,
        index=driver_countries.index(default_driver),
        key="driver_country_select",
    )
    d_row = df_summary[df_summary["country"] == driver_country].iloc[0]
    d_iso = d_row["iso_code"]
    d_hist = df_historical[df_historical["iso_code"] == d_iso].sort_values("year")

    driver_archetype = infer_driver_archetype(d_row)
    render_driver_archetype_box(driver_archetype)

    drivers = sector_driver_scores(d_row, d_hist)
    render_driver_summary_card(build_driver_summary(d_row, driver_archetype, drivers))
    render_interpretation_box(
        build_driver_interpretation(d_row, driver_archetype, drivers),
        label="Interpretation",
    )

    st.markdown("#### Relative Contribution of Overshoot Drivers")
    fig_drv = px.bar(
        drivers,
        x="Score",
        y="Driver",
        orientation="h",
        color="Score",
        color_continuous_scale="Reds",
        labels={"Score": "Relative contribution", "Driver": "Driver"},
        title="Structural drivers of overshoot",
    )
    apply_chart_layout(fig_drv, height=420, showlegend=False)
    st.plotly_chart(fig_drv, use_container_width=True, config=plotly_chart_config())

    render_driver_context_panel(d_row, df_summary)
    render_driver_comparative_context(d_row, df_summary)
    render_driver_policy_relevance_box(build_driver_policy_relevance(d_row, driver_archetype))

# ---------------------------------------------------------
# PAGE: GLOBAL BENCHMARKS
# ---------------------------------------------------------
elif page == "Global Benchmarks":
    render_research_question_box(
        "How much carbon budget remains under different warming targets, "
        "and how quickly is humanity consuming it?"
    )

    bench_records = df_benchmarks.to_dict("records")
    if bench_records:
        b1, b2, b3, b4 = st.columns(4)
        for col, rec in zip([b1, b2, b3, b4], bench_records[:4]):
            with col:
                render_benchmark_card(
                    rec["target"],
                    rec["probability"],
                    rec["remain2020_gt"],
                    rec["emitted_2020_24_gt"],
                    rec["remain2025_gt"],
                )

    if bench_15_50 is not None:
        render_benchmark_countdown_card(float(bench_15_50["remain2025_gt"]))

    render_key_insight_box("", build_benchmark_key_insight(bench_15_50), label="Key Insight")

    if not df_benchmarks.empty:
        st.markdown("#### Remaining global carbon budgets")
        st.plotly_chart(build_benchmark_comparison_chart(df_benchmarks), use_container_width=True, config=plotly_chart_config())
        render_benchmark_comparison_table(df_benchmarks)
        render_interpretation_box(build_benchmark_interpretation_html(), label="Interpretation")
        render_interpretation_box(build_benchmark_policy_implication_html(), label="Policy Implication")

    st.html(
        """
        <div class="restoration-panel" style="margin-top:1rem;">
            <div style="font-size:1.55rem;font-weight:850;letter-spacing:0.04em;margin-bottom:0.75rem;color:#ffffff !important;">Climate Restoration Strategy</div>
            <div class="small-muted" style="line-height:1.75;max-width:980px;">
                Mitigation requires not just emission reduction, but active CDR (Carbon Dioxide Removal) and debt repayment
                mechanisms for nations that have historically overshot their fair share of the planetary carbon budget.
                These benchmarks become meaningful only when linked to equity: who used the budget, who overshot fair share,
                and who would carry future drawdown obligations. Most dashboards stop at whether a carbon budget remains —
                this tracker asks what happens after countries overshoot.
            </div>
        </div>
        """
    )

    with st.expander("Additional budget views"):
        if not df_benchmarks.empty:
            st.plotly_chart(build_benchmark_depletion_chart(df_benchmarks), use_container_width=True, config=plotly_chart_config())
            if bench_15_50 is not None:
                st.plotly_chart(
                    build_budget_countdown_chart(float(bench_15_50["remain2025_gt"])),
                    use_container_width=True,
                    config=plotly_chart_config(),
                )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(
    f"""
    <div class="footer-note">
        Carbon Budget Tracker – IPCC AR6 Fair-Share Explorer • March 2026 • Source mode: {source_mode}
    </div>
    """,
    unsafe_allow_html=True,)
