# Carbon Budget Tracker

## From Fair Shares to Carbon Debt: Quantifying National Responsibility and Policy Gaps under the Paris Agreement

![Dashboard Preview](assets/CO2_Budget_Tracker.png)

**Climate Justice Analytics Platform**

The Carbon Budget Tracker is a Python-based interactive platform that quantifies national fair-share carbon budgets, carbon debt, overshoot timing, and policy gaps under Paris Agreement temperature targets.

By integrating historical emissions data, equity-based allocation methods, and future policy scenarios, the framework evaluates whether countries are operating within their fair share of the remaining global carbon budget and identifies where overshoot has already occurred.

The project moves beyond conventional emissions accounting by introducing **carbon debt** as a measurable indicator of historical responsibility. Carbon debt represents the cumulative emissions a country has produced beyond its allocated share of the remaining global carbon budget.

> *"Equity is at the heart of climate justice: the atmosphere is finite, and so is the remaining carbon budget."*

---

## Run the Dashboard

```bash
cd Carbon-budget-dashboard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501`.

### Deploy on Streamlit Community Cloud (free)

1. Push this folder to a **public** GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** → choose your repo, branch `main`, main file `app.py`.
4. Deploy. The app reads CSVs from `processed_data/` automatically.

### Dashboard Pages

Narrative flow: **responsibility → overshoot → policy gap → future risk**

1. **Executive Dashboard** – global carbon debt state, top debtors, climate warning
2. **Country Explorer** – deep country profiles (metrics, debt curve, overshoot timeline)
3. **Carbon Debt Rankings** – top debtors, creditors, regional totals, Carbon Justice Score
4. **Policy Gap Analysis** – overshoot year vs net-zero pledge gap
5. **AI Scenario Explorer** – AI growth impact on overshoot timing and debt
6. **Overshoot Drivers** – structural drivers behind overshoot
7. **Global Benchmarks** – IPCC AR6 remaining budgets

### Dashboard Data Files

Place processed CSVs in `processed_data/`:

| File | Purpose |
|------|---------|
| `tracker_summary.csv` | Country-level debt and overshoot |
| `clean_carbon_panel.csv` | Annual emissions time series |
| `project_debt_scenarios.csv` | Future debt scenarios |
| `ar6_adjusted_budgets.csv` | Global benchmark budgets |
| `step2_overshoot_drivers.csv` | Driver tags and renewables (optional) |

---

## Why This Matters

The Paris Agreement establishes a finite global carbon budget consistent with limiting warming to 1.5°C and well below 2°C.

While emissions inventories reveal who emits carbon today, they do not answer a critical equity question:

### How much of the remaining carbon budget should each country be entitled to use?

This project addresses that gap by translating global climate targets into country-level fair-share budgets and measuring the consequences of overshoot.

The framework enables researchers, policymakers, and sustainability practitioners to explore:

* Which countries have already exceeded their fair share?
* How large is the resulting carbon debt?
* When did overshoot occur?
* What future mitigation or carbon-removal obligations arise?
* How do alternative policy pathways influence climate equity outcomes?

---

## Research Question

**To what extent have countries exceeded their fair-share share of the remaining global carbon budget, and what carbon debt and future drawdown obligations does this create under Paris-aligned pathways?**

---

## Research Contribution

The Carbon Budget Tracker operationalizes the concept of **carbon debt** by integrating:

* Fair-share allocation
* Historical responsibility
* Overshoot timing
* Future drawdown obligations
* Policy pathway assessment

into a unified analytical framework.

While emissions inventories report who emits carbon, they do not assess whether countries remain within their equitable share of the remaining global carbon budget. This project addresses that gap by providing a transparent and reproducible methodology for evaluating climate equity, historical responsibility, and policy credibility under Paris Agreement temperature targets.

The framework can be used to compare alternative allocation approaches, assess overshoot dynamics, and quantify the scale of future mitigation and carbon-removal obligations required to restore alignment with global climate goals.

---

## Key Findings

Preliminary analysis suggests that:

* Many industrialized economies have already exhausted their fair-share share of the remaining Paris-aligned carbon budget.
* Carbon debt varies substantially across countries and regions.
* Current climate pledges reduce but often do not eliminate overshoot.
* Delayed mitigation significantly increases future drawdown obligations.
* Alternative allocation methodologies can materially alter responsibility distributions.

---

## Key Features

### Fair-Share Budget Allocation

Allocate Paris-aligned carbon budgets using:

* Equal per-capita allocation
* Ability-to-Pay (ATP) weighted allocation

### Carbon Debt Assessment

Quantify cumulative overshoot relative to allocated carbon budgets.

### Overshoot Year Analysis

Identify when countries exhaust their fair-share allocation under different pathways.

### Policy Gap Evaluation

Compare current policy trajectories against Paris-compatible scenarios.

### Drawdown Obligations

Translate carbon debt into per-capita negative-emissions requirements.

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

**Carbon Debt = Historical Emissions − Fair-Share Budget**

Historical fossil-fuel and industrial CO₂ emissions are compared against allocated fair-share budgets.

### 3. Overshoot Analysis

Overshoot years are estimated for countries and regions under multiple decarbonization pathways.

### 4. Scenario Modeling

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

├── processed_data/
├── raw_data/
├── notebook/
├── assets/
├── app.py
├── requirements.txt
└── README.md
```

---

## Example Outputs

* Global Carbon Debt Choropleth Map
* Overshoot Year Rankings
* Fair-Share vs Historical Emissions Comparisons
* Regional Carbon Debt Analysis
* Drawdown Obligation Assessment
* Policy Gap Evaluation

---

## Future Development

* Expanded equity allocation methodologies
* Additional regional and sectoral analyses
* Enhanced dashboard interactivity
* Policy credibility assessment modules
* Integration of future technology-demand scenarios

---

## Author

**Nisha Verma, PhD**

*Sustainability Analytics | Climate Policy | Data Science*

Berlin, Germany

---

## License

MIT License
