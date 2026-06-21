# Carbon Budget Tracker

## Who Owes the Atmosphere?

### Quantifying National Responsibility and Policy Gaps under the Paris Agreement

![Dashboard Preview](assets/dashboard-preview.png)

---

## Overview

The Carbon Budget Tracker is an interactive climate-equity analytics platform that quantifies national fair-share carbon budgets, carbon debt, overshoot timing, and policy gaps under Paris Agreement temperature targets.

The framework translates global carbon budgets into country-level allocations and evaluates whether countries remain within their equitable share of the remaining atmospheric commons. By integrating historical responsibility, equity allocation methods, and future policy pathways, the platform provides a transparent approach for assessing climate responsibility and carbon budget overshoot.

---

## The Central Question

The Paris Agreement establishes a finite remaining carbon budget consistent with limiting warming to 1.5°C and well below 2°C.

Yet one fundamental question remains largely unanswered:

### How much of the remaining carbon budget should each country be entitled to use?

The Carbon Budget Tracker addresses this question by translating global climate targets into country-level fair-share allocations and measuring the consequences when those limits are exceeded.

---

## Key Findings

* 51 countries have already exhausted their fair-share carbon budget.
* The United States has accumulated the largest carbon debt (136 Gt CO₂).
* India remains the largest net carbon creditor (151 Gt CO₂).
* Current climate pledges often reduce but do not eliminate overshoot.
* Historical emissions remain the dominant determinant of present-day carbon debt.
* At current emission rates, the remaining 1.5°C carbon budget may be exhausted within a decade.

---

## Research Outputs

### Interactive Dashboard

Explore the live application:

https://carbon-budget-tracker-ko3xfkqxqq8suy57iccvqr.streamlit.app

### Research Paper

**From Fair Shares to Carbon Debt: Quantifying National Responsibility and Policy Gaps under the Paris Agreement**

The accompanying paper details the conceptual framework, methodology, carbon debt calculations, overshoot analysis, and policy implications underlying the dashboard.

---

## Why This Matters

Most climate dashboards focus on annual emissions, carbon intensity, or net-zero commitments.

The Carbon Budget Tracker focuses on a different dimension of climate accountability:

* Fair-share carbon budgets
* Historical responsibility
* Carbon debt
* Overshoot timing
* Policy gaps
* Future drawdown obligations

By integrating these dimensions into a single framework, the project provides an equity-based perspective on climate responsibility that is often absent from conventional emissions reporting.

---

## Novel Contribution

The project introduces carbon debt as a measurable indicator of climate responsibility.

Carbon debt represents the cumulative emissions a country has produced beyond its allocated share of the remaining global carbon budget.

Rather than asking only who emits carbon today, the framework asks:

* Who has already consumed more than their fair share?
* When did overshoot occur?
* How large is the resulting carbon debt?
* What future mitigation obligations arise from that overshoot?

This approach links climate science, equity principles, and policy evaluation within a single analytical framework.

---

## Dashboard Architecture

The platform follows a narrative flow:

**Responsibility → Overshoot → Policy Gap → Future Risk**

### Executive Dashboard

Global overview of carbon debt, overshoot status, and remaining carbon budgets.

### Country Explorer

Interactive country profiles including fair-share budgets, carbon debt, overshoot timing, and policy gaps.

### Carbon Debt Rankings

Global rankings of carbon debtors and carbon creditors.

### Policy Gap Analysis

Comparison between overshoot timing and national climate commitments.

### AI Scenario Explorer

Future overshoot trajectories under alternative economic and technology-demand scenarios.

### Overshoot Drivers

Analysis of structural factors associated with national overshoot patterns.

### Global Benchmarks

Comparison against IPCC AR6 carbon budget thresholds.

---

## Methodology

The framework combines six analytical components:

### 1. Fair-Share Allocation

Remaining global carbon budgets are allocated using:

* Equal per-capita allocation
* Ability-to-Pay (ATP) weighted allocation

### 2. Carbon Debt Calculation

**Carbon Debt = Historical Emissions − Fair-Share Budget**

Historical fossil-fuel and industrial CO₂ emissions are compared against allocated fair-share budgets.

### 3. Overshoot Analysis

Overshoot years are estimated for countries and regions under multiple decarbonization pathways.

### 4. Policy Gap Assessment

National climate commitments are compared against estimated overshoot timelines.

### 5. Scenario Modelling

Future pathways incorporate:

* Current Policies (CurPol)
* Nationally Determined Contributions (NDCs)
* Paris-aligned mitigation pathways

### 6. Drawdown Obligations

Carbon debt is translated into future negative-emissions requirements between 2025 and 2100.

---

## Results Snapshot

| Indicator                           | Finding       |
| ----------------------------------- | ------------- |
| Largest Carbon Debtor               | United States |
| Largest Carbon Creditor             | India         |
| Countries in Overshoot              | 51            |
| Countries Within Budget             | 27            |
| Remaining 1.5°C Budget              | 362 Gt CO₂    |
| Time Remaining at Current Emissions | ~9 Years      |

---

## Data Sources

| Dataset                           | Purpose                                          |
| --------------------------------- | ------------------------------------------------ |
| IPCC AR6 Carbon Budgets           | Remaining global carbon budgets                  |
| Global Carbon Budget              | Historical emissions and carbon-cycle assessment |
| Our World in Data CO₂ Dataset     | Historical emissions and population data         |
| UNFCCC NDC Registry               | National climate commitments                     |
| World Bank Development Indicators | Economic and development indicators              |

---

## Technical Stack

### Analytics

* Python
* Pandas
* NumPy

### Visualisation

* Plotly
* Matplotlib

### Dashboard

* Streamlit

### Workflow

* Jupyter Notebooks
* Reproducible Data Pipelines

---

## Future Development

Planned extensions include:

* Additional allocation methodologies
* Sector-level carbon debt accounting
* Regional equity assessments
* Expanded scenario modelling
* Carbon-removal pathway analysis
* Climate technology integration

---

## Author

**Nisha Verma, PhD**

Sustainability Analytics • Climate Policy • Data Science

Berlin, Germany

---

## License

MIT License


