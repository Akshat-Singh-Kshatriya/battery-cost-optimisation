
# Battery Cell Cost Optimisation Model

## Project Overview
A data-driven cost engineering project focused on estimating lithium-ion battery cell manufacturing costs, identifying major cost drivers and evaluating cost reduction opportunities through scenario analysis and Monte Carlo simulation.

The model integrates material consumption, production scrap, energy consumption, labour and depreciation to estimate manufacturing costs per kWh.

## Objectives
- Develop a bottom-up battery cell manufacturing cost model.
- Identify major contributors to battery production costs.
- Evaluate manufacturing and procurement cost optimisation opportunities.
- Quantify cost uncertainty under changing market and operational assumptions.

## Tech Stack
- **Programming:** Python
- **Database:** SQL
- **Data Analysis:** Pandas, NumPy
- **Simulation:** Monte Carlo Simulation
- **Visualisation:** Matplotlib, Seaborn
- **Modelling:** Excel

## Cost Model Components

| Component | Cost Driver |
|---|---|
| Cathode materials | Active material procurement price |
| Production scrap | Stage-wise material losses |
| Energy | Manufacturing energy consumption |
| Labour | Production workforce costs |
| Depreciation | Equipment and manufacturing asset costs |

## Methodology

### 1. Data Integration and Cost Estimation
- Used SQL to combine Bill of Materials (BOM) quantities with manufacturing scrap assumptions.
- Processed material consumption and production cost data using Python.
- Incorporated energy, labour and depreciation expenses.
- Calculated baseline manufacturing cost per kWh.

### 2. Cost Driver Analysis
Evaluated four major cost optimisation levers:

- Cathode material price reduction.
- Equipment utilisation improvement from 70% to 80%.
- Coating scrap reduction from 2.37% to 1.2%.
- Drying energy consumption reduction by 15%.

Quantified the impact of individual and combined cost optimisation scenarios.

### 3. Monte Carlo Simulation
- Conducted 5,000 Monte Carlo simulations.
- Introduced uncertainty across key manufacturing cost inputs.
- Estimated P10, P50 and P90 cost distributions.
- Identified high-impact cost drivers to prioritise optimisation opportunities.

## Key Results

| Performance Metric | Result |
|---|---:|
| Baseline manufacturing cost | $97.6/kWh |
| Cathode material cost contribution | 40% |
| Cost optimisation levers evaluated | 4 |
| Potential cost reduction | $4.49/kWh |
| Relative cost reduction | 4.6% |
| Monte Carlo simulations | 5,000 |
| P10 cost estimate | $89.9/kWh |
| P90 cost estimate | $105.1/kWh |
## Business Impact
The project demonstrates how bottom-up cost modelling, scenario analysis and probabilistic simulations can support battery manufacturing cost reduction, procurement decisions and resource allocation.

## Assumptions and Limitations
- BOM quantities, material prices and manufacturing cost inputs are illustrative.
- Cost reduction estimates depend on the assumed production conditions.
- Monte Carlo results represent modelled uncertainty rather than actual supplier or factory cost distributions.
- Annual savings are estimated using an assumed 8 GWh production capacity.

- Include capital expenditure and operating expenditure sensitivity.
- Develop an interactive cost analysis dashboard.
