# Carbon Budget Tracker

## From Fair Shares to Carbon Debt: Quantifying National Responsibility and Policy Gaps under the Paris Agreement

![Dashboard Preview](assets/dashboard-preview.png)

### Climate Equity Analytics Framework

The Carbon Budget Tracker is a Python-based interactive research platform that quantifies national fair-share carbon budgets, carbon debt, overshoot timing, and policy gaps under Paris Agreement temperature targets.

By integrating historical emissions data, equity-based allocation methods, and future policy scenarios, the framework evaluates whether countries are operating within their fair share of the remaining global carbon budget and identifies where overshoot has already occurred.

The project moves beyond conventional emissions accounting by introducing **carbon debt** as a measurable indicator of historical responsibility. Carbon debt represents the cumulative emissions a country has produced beyond its allocated share of the remaining global carbon budget.

> *"Equity is at the heart of climate justice: the atmosphere is finite, and so is the remaining carbon budget."*

---

# Live Demo

**[Open the Carbon Budget Tracker →](https://carbon-budget-tracker-ko3xfkqxqq8suy57iccvqr.streamlit.app)**

Hosted on Streamlit Community Cloud. No installation required.

---

# Research Question

**To what extent have countries exceeded their fair-share allocation of the remaining global carbon budget, and what carbon debt and future drawdown obligations does this create under Paris-aligned pathways?**

---

# Why This Matters

The Paris Agreement establishes a finite global carbon budget consistent with limiting warming to 1.5°C and well below 2°C.

While emissions inventories reveal who emits carbon today, they do not answer a critical equity question:

## How much of the remaining carbon budget should each country be entitled to use?

This project addresses that gap by translating global climate targets into country-level fair-share budgets and measuring the consequences of overshoot.

The framework enables researchers, policymakers, and sustainability practitioners to explore:

* Which countries have already exceeded their fair share?
* How large is the resulting carbon debt?
* When did overshoot occur?
* What future mitigation or carbon-removal obligations arise?
* How do alternative policy pathways influence climate equity outcomes?

---

# Novel Contribution

Most climate dashboards focus on annual emissions, carbon intensity, or net-zero pledges.

This project introduces a fair-share accounting framework that evaluates whether countries remain within their equitable share of the remaining global carbon budget. By translating cumulative emissions into carbon debt, overshoot timing, and future drawdown obligations, the framework provides a climate-justice perspective largely absent from conventional emissions reporting.

The project combines equity allocation, historical responsibility, and future policy pathways into a unified analytical framework designed for sustainability research and policy evaluation.

---

# Results Snapshot

| Indicator                           | Finding       |
| ----------------------------------- | ------------- |
| Largest Carbon Debtor               | United States |
| Largest Carbon Creditor             | India         |
| Countries in Overshoot              | 51            |
| Countries Remaining Within Budget   | 27            |
| Remaining 1.5°C Budget (2025+)      | 362 Gt CO₂    |
| Time Remaining at Current Emissions | ~9 years      |

---

# Key Findings

Preliminary analysis suggests that:

* Many industrialized economies have already exhausted their fair-share allocation of the remaining Paris-aligned carbon budget.
* Carbon debt varies substantially across countries and regions.
* Current climate pledges reduce but often do not eliminate overshoot.
* Delayed mitigation significantly increases future drawdown obligations.
* Alternative allocation methodologies can materially alter responsibility distributions.
* Historical emissions remain the dominant determinant of present-day carbon debt.

---

# Dashboard Pages

Narrative flow:

**Responsibility → Overshoot → Policy Gap → Future Risk**

### Executive Dashboard

Global carbon debt overview, climate warnings, debt leaders, and key metrics.

### Country Explorer

Interactive country profiles including debt, overshoot timing, budget utilization, and structural drivers.

### Carbon Debt Rankings

Global rankings of debtors and creditors with comparative analysis.

### Policy Gap Analysis

Comparison between overshoot timing and national net-zero commitments.

### AI Scenario Explorer

Future overshoot trajectories under alternative economic and technology-demand scenarios.

### Overshoot Drivers

Analysis of structural factors associated with national carbon budget overshoot.

### Global Benchmarks

IPCC AR6 carbon budget benchmarks and remaining budget assessments.

---

# Methodology

## 1. Fair-Share Allocation

Remaining global carbon budgets from IPCC AR6 are allocated using:

* Equal per-capita allocation
* Ability-to-Pay (ATP) weighted allocation

## 2. Carbon Debt Calculation

**Carbon Debt = Historical Emissions − Fair-Share Budget**

Historical fossil-fuel and industrial CO₂ emissions are compared against allocated fair-share budgets.

## 3. Overshoot Analysis

Overshoot years are estimated for countries and regions under multiple decarbonization pathways.

## 4. Scenario Modeling

Future pathways integrate:

* Current Policies (CurPol)
* Current Pledges (NDCs)
* Paris-aligned mitigation pathways

## 5. Drawdown Obligations

Carbon debt is translated into per-capita negative-emissions requirements between 2025 and 2100.

---

# Data Sources

| Dataset                 | Content                                             | Source            |
| ----------------------- | --------------------------------------------------- | ----------------- |
| OWID CO₂ Dataset        | Historical emissions, population, energy indicators | Our World in Data |
| IPCC AR6 Carbon Budgets | Remaining global carbon budgets                     | IPCC AR6 WG1      |
| UNFCCC NDC Registry     | National climate pledges                            | UNFCCC            |
| World Bank Open Data    | GDP and development indicators                      | World Bank        |

---

# Dashboard Data Files

Place processed CSV files inside:

```text
processed_data/
```

| File                        | Purpose                                  |
| --------------------------- | ---------------------------------------- |
| tracker_summary.csv         | Country-level debt and overshoot metrics |
| clean_carbon_panel.csv      | Historical emissions panel               |
| project_debt_scenarios.csv  | Future pathway projections               |
| ar6_adjusted_budgets.csv    | IPCC benchmark budgets                   |
| step2_overshoot_drivers.csv | Structural driver indicators             |

---

# Run Locally

```bash
cd Carbon-budget-dashboard

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# Deploy on Streamlit Community Cloud

**Live app:** [https://carbon-budget-tracker-ko3xfkqxqq8suy57iccvqr.streamlit.app](https://carbon-budget-tracker-ko3xfkqxqq8suy57iccvqr.streamlit.app)

To redeploy or fork:

1. Push the repository to GitHub.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io).
3. Create a new application.
4. Select repository and branch.
5. Set:

```text
Main file: app.py
```

6. Deploy.

---

# Technical Stack

### Analytics

* Python
* Pandas
* NumPy

### Visualization

* Plotly
* Matplotlib

### Dashboard

* Streamlit

### Workflow

* Jupyter Notebooks
* Reproducible Data Pipelines

---

# Repository Structure

```text
carbon-budget-tracker/

├── assets/
├── raw_data/
├── processed_data/
├── notebooks/
├── src/
├── app.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

# Example Outputs

* Global Carbon Debt Map
* Carbon Debt Leaderboard
* Country Overshoot Profiles
* Fair-Share Allocation Analysis
* Policy Gap Assessment
* Carbon Budget Benchmark Explorer
* Drawdown Obligation Scenarios

---

# Future Development

* Additional allocation methodologies
* Sector-level debt accounting
* Regional equity assessments
* Expanded scenario modeling
* Integration of climate technology pathways
* Carbon-removal strategy evaluation

---

# Author

**Nisha Verma, PhD**

Sustainability Analytics • Climate Policy • Data Science

Berlin, Germany

---

# License

MIT License
