# 🌍 Carbon Budget Tracker  
**From Fair Shares to Carbon Debt: Why Countries Overshoot the Paris Agreement**

<p align="center">
  <img src="assets/CO2_Budget_Tracker.png" width="750">
</p>


---
# Carbon Budget Tracker

## From Fair Shares to Carbon Debt: Quantifying National Responsibility and Policy Gaps under the Paris Agreement

![Carbon Budget Tracker Dashboard](assets/dashboard_overview.png)

### Climate Justice Analytics Platform

The Carbon Budget Tracker is a Python-based climate analytics platform that quantifies national fair-share carbon budgets, carbon debt, overshoot timing, and policy gaps under Paris Agreement temperature targets.

By combining historical emissions, population dynamics, equity-based allocation methods, and future policy scenarios, the framework evaluates whether countries are operating within their fair share of the remaining global carbon budget.

The project moves beyond conventional emissions accounting by introducing **carbon debt** as an operational measure of historical responsibility. Carbon debt represents the cumulative emissions a country has produced beyond its allocated share of the remaining global carbon budget.

This framework provides a transparent and reproducible approach for evaluating climate equity, policy credibility, and future mitigation obligations.

> "Equity is at the heart of climate justice: the atmosphere is finite, and so is the remaining carbon budget."

---

## Why This Matters

The Paris Agreement establishes a finite global carbon budget consistent with limiting warming to 1.5°C or 2°C. While emissions inventories reveal who emits carbon today, they do not answer a critical equity question:

**How much of the remaining carbon budget should each country be entitled to use?**

This project addresses that gap by translating global climate targets into country-level fair-share budgets and measuring the consequences of overshoot.

The framework enables researchers, policymakers, and sustainability practitioners to explore:

* Which countries have already exceeded their fair share?
* How large is the resulting carbon debt?
* When did overshoot occur?
* What future mitigation or carbon removal obligations arise?
* How do alternative policy pathways influence climate equity outcomes?

---

## Research Question

**To what extent have countries exceeded their fair-share share of the remaining global carbon budget, and what carbon debt and future drawdown obligations does this create under Paris-aligned pathways?**

---

## Research Contribution

The project operationalizes the concept of **carbon debt** by integrating:

* Fair-share budget allocation
* Historical responsibility
* Overshoot timing
* Future drawdown obligations
* Policy pathway assessment

into a unified analytical framework.

By linking climate equity principles with transparent computational methods, the framework provides a reproducible approach for evaluating national responsibility under Paris Agreement targets.

---

## Key Findings

Preliminary analyses indicate that:

* Many industrialized economies have already exhausted their fair-share share of the Paris carbon budget.
* Historical emissions generate substantial carbon debt disparities across countries and regions.
* Current climate pledges reduce but often do not eliminate overshoot.
* Delayed mitigation significantly increases future drawdown obligations.
* Allocation methodology strongly influences responsibility distributions and policy outcomes.

---

## Key Features

### Fair-Share Budget Allocation

Allocate Paris-aligned carbon budgets using equal per-capita and Ability-to-Pay methodologies.

### Carbon Debt Assessment

Quantify cumulative overshoot relative to allocated carbon budgets.

### Overshoot Year Analysis

Identify when countries exhaust their fair-share allocation under different pathways.

### Policy Gap Evaluation

Compare current policy trajectories against Paris-compatible scenarios.

### Drawdown Obligations

Translate carbon debt into per-capita negative emissions requirements.

### Interactive Visualizations

Explore carbon debt, overshoot timing, regional disparities, and future scenarios through interactive dashboards.

---

## Data Sources

| Dataset                 | Content                                             | Source                      |
| ----------------------- | --------------------------------------------------- | --------------------------- |
| OWID CO₂ Dataset        | Historical emissions, population, energy indicators | Our World in Data           |
| IPCC AR6 Carbon Budgets | Remaining global carbon budgets                     | IPCC Working Group I (2021) |
| UNFCCC NDC Registry     | National climate pledges                            | UNFCCC                      |
| World Bank Open Data    | GDP and development indicators                      | World Bank                  |

---

## Methodology

### 1. Fair-Share Allocation

Remaining global carbon budgets from IPCC AR6 are allocated using:

* Equal per-capita allocation
* Ability-to-Pay weighted allocation

### 2. Carbon Debt Calculation

Historical fossil-fuel and industrial CO₂ emissions are compared against allocated fair-share budgets.

Carbon Debt = Historical Emissions − Fair-Share Budget

### 3. Overshoot Analysis

Overshoot years are estimated for countries and regions under multiple decarbonization pathways.

### 4. Scenario Harmonization

Future pathways integrate:

* Current Policies (CurPol)
* Current Pledges (NDCs)
* Ambitious Decarbonization Scenarios

### 5. Drawdown Obligations

Carbon debt is translated into per-capita negative-emissions requirements between 2025 and 2100.

---

## Technical Stack

### Core Analytics

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

## Repository Structure

```text
carbon-budget-tracker/

├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_fair_share_allocation.ipynb
│   ├── 04_carbon_debt_calculation.ipynb
│   ├── 05_scenario_analysis.ipynb
│   └── 06_visualization.ipynb
│
├── visuals/
│
├── scripts/
│
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

## Example Outputs

* Global Carbon Debt Map
* Overshoot Year Rankings
* Regional Fair-Share Comparisons
* Drawdown Obligation Analysis
* Scenario Comparison Dashboards
* Policy Gap Assessments

---

## Installation

```bash
git clone https://github.com/nishaverma24-bot/carbon-budget-tracker.git

cd carbon-budget-tracker

python -m venv .venv

source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

pip install -r requirements.txt

streamlit run streamlit_app.py
```

---

## Future Development

Planned extensions include:

* AI-driven electricity demand scenarios
* Climate-policy credibility assessment
* Enhanced regional equity metrics
* Additional allocation methodologies
* Expanded dashboard interactivity

---

## Author

**Nisha Verma, PhD**

Sustainability Analytics | Climate Policy | Data Science

Berlin, Germany

---

## License

This project is released under the MIT License.
