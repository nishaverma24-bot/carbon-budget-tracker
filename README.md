# 🌍 Carbon Budget Tracker  
**From Fair Shares to Carbon Debt: Why Countries Overshoot the Paris Agreement**

<center>
<img src="Data Analytics-Final Project/Picks/CO2_Budget_Tracker.png" width="750">
</center>

---

## Introduction  

The **Carbon Budget Tracker** is a Python + Streamlit dashboard that quantifies **countries’ fair-share CO₂ budgets**, **carbon overshoot (debt)**, and **policy gaps** under different decarbonization scenarios.  

Using data from **IPCC AR6**, **Our World in Data**, and **UNFCCC pledges**, the project visualizes how national trajectories align—or diverge—from the Paris Agreement’s 1.5 °C pathway.  

It translates global climate equity into measurable numbers:  
how much carbon a country *could* emit (its fair share),  
how much it *has* emitted (historical responsibility),  
and how much it *owes* back to the planet (its carbon debt).  

---

## “Equity is the heart of climate justice — the atmosphere is finite, and so is our time.”  

An interactive dashboard showing national overshoot timelines, carbon debt accumulation, and fair-share comparisons across regions.

---

## Goals of the Analysis  

- Allocate **fair-share carbon budgets** across countries and regions  
- Compute **carbon overshoot and debt** based on historical emissions  
- Quantify the **year of overshoot** for each country under multiple scenarios (Baseline, NDC, Ambitious)  
- Translate overshoot into **drawdown obligations** (per-capita negative emissions needs)  
- Visualize **AI-induced emission increase risks** and fairness implications  

---

## Research Question  

How can we measure whether each country is staying within its **fair share of the global carbon budget**, and what happens when it overshoots?  

Does technological acceleration (AI, industrial growth) risk deepening carbon inequality — or can ambitious climate policies close the overshoot gap?  

---

## Dataset Overview  

| Dataset | Description | Source |
|----------|--------------|---------|
| **OWID CO₂ Data** | Historical CO₂ emissions, energy, and population | Our World in Data |
| **IPCC AR6 Budgets** | Remaining global carbon budgets for 1.5 °C and 2 °C | IPCC WG I AR6 (2021) |
| **UNFCCC NDCs** | Nationally Determined Contributions (pledges) | UNFCCC Database |
| **World Bank GDP** | GDP per capita (used for ability-to-pay scaling) | World Bank Open Data |

---

## Key Indicators  

| Indicator | Meaning |
|------------|----------|
| `co2_ffi` | CO₂ emissions from fossil fuels + industry (MtCO₂/yr) |
| `population` | National population |
| `budget_fairshare` | Allocated fair-share budget (MtCO₂) |
| `overshoot_year` | Year when fair-share budget is exhausted |
| `carbon_debt` | Excess emissions beyond fair-share (MtCO₂) |
| `drawdown_per_capita` | Negative emissions needed (tCO₂/person) |
| `scenario` | Policy trajectory (Baseline / NDC / Ambitious / AI) |

---

## Methodology  

1. **Fair-Share Allocation** — Equal per-capita distribution of IPCC AR6 budgets  
2. **Carbon Debt Computation** — Subtract historical CO₂ (1990–2022) from allocated share  
3. **Alternative Allocation** — Weighting by **Ability-to-Pay (ATP)** using cumulative GDP  
4. **Scenario Harmonization** — Align IPCC WG III pathways (CurPol vs CurPledge) with 2022 data  
5. **Drawdown Obligation** — Translate carbon debt into required negative emissions (2025–2100)  
6. **Visualization** — Choropleths, bubble plots, overshoot timelines, and AI impact panels  

---

## ⚙️ Tools & Libraries  

- **Python:**  Pandas, NumPy, Matplotlib, Plotly, Streamlit, Pathlib  
- **Jupyter Notebook:**  Workflow Steps (01 – 22)  
- **Data Processing:**  Grouping, normalization, per-capita allocation, scenario joins  
- **Visualization:**  Plotly subplots, choropleths, multi-panel charts  

---

## 📂 Repository Structure  

| Folder | Description |
|---------|-------------|
| `/data/` | Raw & processed datasets (OWID, IPCC, UNFCCC) |
| `/notebooks/` | Step-wise analysis and scenario generation (01–22) |
| `/visuals/` | Saved charts and multi-panel figures |
| `/scripts/` | Helper functions for budget allocation and visuals |
| `requirements.txt` | Python dependencies |
| `streamlit_app.py` | Interactive dashboard entry point |

---

## Getting Started  

```bash
# Clone the repository
git clone https://github.com/nishaverma24-bot/carbon-budget-tracker.git
cd carbon-budget-tracker

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # (Windows: .venv\Scripts\activate)

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter or Streamlit
jupyter lab
# or
streamlit run streamlit_app.py
🌐 Data Sources and Citation
Our World in Data – CO₂ Emissions Dataset
IPCC AR6 – Working Group I (2021)
UNFCCC – NDC Registry
World Bank Open Data
🧮 Main Notebook
📓 carbon_budget_tracker_analysis.ipynb
Runs the full workflow — data ingestion, fair-share computation, scenario modeling, and multi-panel visualization.
📈 Example Visualizations
🌍 Global CO₂ emissions vs remaining budgets
💰 Fair-share and carbon debt per country
📆 Overshoot year by region and scenario
🤖 AI impact on future emission trajectories

Project by Nisha Verma | Python + Streamlit Dashboard
📍 Berlin | 2025
