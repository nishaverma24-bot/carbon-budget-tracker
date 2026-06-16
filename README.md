# BudgetTracker – IPCC AR6 Analytics Engine

Self-hosted carbon budget dashboard (replacement for the hosted Next.js version).

## Run locally

```bash
cd Carbon-budget-dashboard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501`.

## Deploy on Streamlit Community Cloud (free)

1. Push this folder to a **public** GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** → choose your repo, branch `main`, main file `app.py`.
4. Deploy. The app reads CSVs from `processed_data/` automatically.

## Pages

Narrative flow: **responsibility → overshoot → policy gap → future risk**

1. **Executive Dashboard** – global carbon debt state, top debtors, climate warning
2. **Country Explorer** – deep country profiles (Germany-style metrics, debt curve, overshoot timeline)
3. **Carbon Debt Rankings** – top debtors, creditors, regional totals, Carbon Justice Score
4. **Policy Gap Analysis** – overshoot year vs net-zero pledge gap
5. **AI Scenario Explorer** – AI growth impact on overshoot timing and debt
6. **Overshoot Drivers** – structural drivers behind overshoot
7. **Global Benchmarks** – IPCC AR6 remaining budgets

## Data

Place processed CSVs in `processed_data/`:

| File | Purpose |
|------|---------|
| `tracker_summary.csv` | Country-level debt and overshoot |
| `clean_carbon_panel.csv` | Annual emissions time series |
| `project_debt_scenarios.csv` | Future debt scenarios |
| `ar6_adjusted_budgets.csv` | Global benchmark budgets |
| `step2_overshoot_drivers.csv` | Driver tags and renewables (optional) |
