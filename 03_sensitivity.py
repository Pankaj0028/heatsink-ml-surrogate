"""
Task 1d: correlation + sensitivity analysis.
 1) Pearson & Spearman correlation matrix
 2) Standardised regression coefficients (importance of each input, same units)
 3) Random-forest permutation importance
 4) One-at-a-time elasticity around the nominal point (TDP=150, V=1, k=4) = %change output / %change input
"""
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from heat_sink_model import heat_sink_design

df = pd.read_csv("data/heatsink_dataset.csv")
F = ["TDP_W", "V_air_mps", "k_tim_WmK"]; T = ["R_total_C_per_W", "T_junction_C"]

pear = df[F + T].corr(method="pearson").loc[F, T]
spear = df[F + T].corr(method="spearman").loc[F, T]
print("Pearson\n", pear.round(3), "\n\nSpearman\n", spear.round(3))

z = (df[F + T] - df[F + T].mean()) / df[F + T].std()
src = pd.DataFrame({t: LinearRegression().fit(z[F], z[t]).coef_ for t in T}, index=F)
print("\nStandardised regression coefficients\n", src.round(3))

pi = {}
for t in T:
    rf = RandomForestRegressor(300, random_state=0, n_jobs=-1).fit(df[F], df[t])
    pi[t] = permutation_importance(rf, df[F], df[t], n_repeats=10, random_state=0).importances_mean
pi = pd.DataFrame(pi, index=F); pi = pi / pi.sum()
print("\nPermutation importance (normalised)\n", pi.round(3))

base = dict(TDP=150.0, V_air=1.0, k_tim=4.0)
rows = []
for key, name in zip(["TDP", "V_air", "k_tim"], F):
    out = {}
    for d in (-0.01, 0.01):
        kw = {**base, key: base[key] * (1 + d)}
        r = heat_sink_design(**kw); out[d] = (r["R_total"], r["T_j"])
    n = heat_sink_design(**base)
    rows.append(dict(Parameter=name,
        Elasticity_R=((out[.01][0] - out[-.01][0]) / n["R_total"]) / 0.02,
        Elasticity_Tj=((out[.01][1] - out[-.01][1]) / n["T_j"]) / 0.02))
el = pd.DataFrame(rows).set_index("Parameter"); print("\nElasticities at nominal point\n", el.round(4))

with pd.ExcelWriter("results/sensitivity.xlsx") as w:
    pear.to_excel(w, sheet_name="pearson"); spear.to_excel(w, sheet_name="spearman"); src.to_excel(w, sheet_name="std_coeff")
    pi.to_excel(w, sheet_name="perm_importance"); el.to_excel(w, sheet_name="elasticity")

fig, ax = plt.subplots(1, 3, figsize=(16, 4.5))
for a, (d, t) in zip(ax, [(pear, "Pearson correlation"), (src, "Standardised regression coeff."), (pi, "Permutation importance")]):
    d.plot.bar(ax=a, rot=15); a.set_title(t); a.axhline(0, c="k", lw=.5)
plt.tight_layout(); plt.savefig("results/sensitivity.png", dpi=130)

# design-space plots
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
s = ax[0].scatter(df.V_air_mps, df.R_total_C_per_W, c=df.k_tim_WmK, s=6); plt.colorbar(s, ax=ax[0], label="k_tim")
ax[0].set_xlabel("V (m/s)"); ax[0].set_ylabel("R_total (C/W)"); ax[0].set_title("R_total vs airflow")
s = ax[1].scatter(df.TDP_W, df.T_junction_C, c=df.V_air_mps, s=6); plt.colorbar(s, ax=ax[1], label="V (m/s)")
ax[1].set_xlabel("TDP (W)"); ax[1].set_ylabel("Tj (C)"); ax[1].set_title("Junction temp vs TDP")
plt.tight_layout(); plt.savefig("results/design_space.png", dpi=130)
