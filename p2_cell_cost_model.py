"""
Project 2: Cell cost ($/kWh) model with scrap, utility and throughput levers
Stack: SQL (SQLite), Python (cost model + Monte Carlo), Power BI export
Data: illustrative BOM and plant inputs (replace with your own sourced assumptions)
"""
import sqlite3, os
import numpy as np, pandas as pd

OUT = os.environ.get("OUT", "p2_out"); os.makedirs(OUT, exist_ok=True)

# ---------- 1. Inputs (per kWh of cell output, illustrative) ----------
bom = pd.DataFrame({
    "item":        ["cathode_active", "anode_active", "electrolyte", "separator", "copper_foil", "aluminium_foil", "other"],
    "qty_per_kwh": [1.90, 1.05, 0.95, 9.0, 0.75, 0.40, 1.0],       # kg (separator in m2)
    "unit_cost":   [20.0, 9.5, 8.0, 0.75, 9.0, 4.2, 6.0],           # USD per unit
    "scrap_stage": ["coating", "coating", "assembly", "assembly", "coating", "coating", "assembly"]})
scrap = pd.DataFrame({"stage": ["coating", "assembly", "formation"], "scrap_rate": [0.0237, 0.0049, 0.0065]})
plant = {"energy_kwh_per_kwh_cell": 38.0, "power_cost_usd_kwh": 0.09,
         "labour_usd_per_kwh": 4.5, "depn_usd_per_kwh_at_base": 11.0, "base_util": 0.70}

con = sqlite3.connect(":memory:")
bom.to_sql("bom", con, index=False); scrap.to_sql("scrap", con, index=False)

# ---------- 2. SQL: material cost incl. scrap loss by item ----------
sql = """
SELECT b.item,
       b.qty_per_kwh * b.unit_cost                            AS gross_cost,
       b.qty_per_kwh * b.unit_cost * COALESCE(s.scrap_rate,0) AS scrap_loss,
       b.qty_per_kwh * b.unit_cost * (1 + COALESCE(s.scrap_rate,0)) AS cost_with_scrap
FROM bom b LEFT JOIN scrap s ON b.scrap_stage = s.stage
ORDER BY cost_with_scrap DESC
"""
mat = pd.read_sql(sql, con)

def cost_per_kwh(cathode_price=20.0, coating_scrap=0.0237, util=0.70, energy_saving=0.0):
    m = mat.copy()
    m.loc[m.item == "cathode_active", "gross_cost"] = 1.90 * cathode_price
    coat_items = bom.loc[bom.scrap_stage == "coating", "item"]
    rate = np.where(m.item.isin(coat_items), coating_scrap,
                    np.where(m.item.isin(bom.loc[bom.scrap_stage == "assembly", "item"]), 0.0049, 0))
    material = (m.gross_cost * (1 + rate)).sum()
    form_loss = material * 0.0065
    energy = plant["energy_kwh_per_kwh_cell"] * (1 - energy_saving) * plant["power_cost_usd_kwh"]
    depn = plant["depn_usd_per_kwh_at_base"] * plant["base_util"] / util   # fixed cost spreads over output
    return material + form_loss + energy + plant["labour_usd_per_kwh"] + depn

base = cost_per_kwh()

# ---------- 3. Lever analysis ----------
levers = {
    "Coating scrap 2.37% -> 1.2%":      cost_per_kwh(coating_scrap=0.012),
    "Utilisation 70% -> 80%":           cost_per_kwh(util=0.80),
    "Drying/formation energy -15%":     cost_per_kwh(energy_saving=0.15),
    "Cathode price -5%":                cost_per_kwh(cathode_price=19.0),
}
lev = pd.DataFrame({"lever": list(levers), "cost_usd_kwh": list(levers.values())})
lev["saving_usd_kwh"] = base - lev.cost_usd_kwh
lev["saving_pct"] = lev.saving_usd_kwh / base * 100
lev = lev.sort_values("saving_usd_kwh", ascending=False).round(3)
combined = cost_per_kwh(cathode_price=19.0, coating_scrap=0.012, util=0.80, energy_saving=0.15)

# ---------- 4. Monte Carlo on uncertain inputs (cathode price, scrap, utilisation) ----------
rng = np.random.default_rng(7)
N = 5000
sims = np.array([cost_per_kwh(cathode_price=rng.normal(20, 3), coating_scrap=max(rng.normal(.0237, .006), .005),
                              util=np.clip(rng.normal(.70, .06), .5, .95)) for _ in range(N)])
p10, p50, p90 = np.percentile(sims, [10, 50, 90])
# share of variance by driver (one-at-a-time swing)
swing = pd.Series({
    "cathode_price (17-23)": cost_per_kwh(cathode_price=23) - cost_per_kwh(cathode_price=17),
    "coating_scrap (1.5-3.5%)": cost_per_kwh(coating_scrap=.035) - cost_per_kwh(coating_scrap=.015),
    "utilisation (60-80%)": cost_per_kwh(util=.60) - cost_per_kwh(util=.80)}).abs().sort_values(ascending=False)

mat.round(3).to_csv(f"{OUT}/material_cost.csv", index=False)
lev.to_csv(f"{OUT}/levers.csv", index=False)
pd.DataFrame({"sim_cost_usd_kwh": sims}).to_csv(f"{OUT}/monte_carlo.csv", index=False)

print(f"Baseline cost: ${base:.2f}/kWh")
print(mat.round(2).to_string(index=False))
print("\nLevers:\n", lev.to_string(index=False))
print(f"\nCombined levers: ${combined:.2f}/kWh  (saving ${base-combined:.2f}, {(base-combined)/base*100:.1f}%)")
print(f"Monte Carlo P10/P50/P90: ${p10:.1f} / ${p50:.1f} / ${p90:.1f}")
print("Swing by driver (USD/kWh):\n", swing.round(2))
print(f"Annual saving at 8 GWh output: ${(base-combined)*8e6/1e6:.1f}M")
