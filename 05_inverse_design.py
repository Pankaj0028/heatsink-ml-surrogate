"""
Inverse design: minimum airflow needed to keep Tj <= limit, for a range of TDP and TIM grades.
Uses the physics model with a root finder (brentq).  Answers "how much fan do I need?"
"""
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from heat_sink_model import heat_sink_design

TJ_MAX = 85.0
tdps = np.linspace(30, 250, 45)
plt.figure(figsize=(7, 4.5))
for k in (1, 4, 8, 12):
    vmin = []
    for q in tdps:
        f = lambda v: heat_sink_design(TDP=q, V_air=v, k_tim=k)["T_j"] - TJ_MAX
        if f(15) > 0: vmin.append(np.nan)          # infeasible even at 15 m/s
        elif f(0.5) <= 0: vmin.append(0.5)
        else: vmin.append(brentq(f, 0.5, 15))
    plt.plot(tdps, vmin, label=f"k_tim={k} W/mK")
    ok = [q for q, v in zip(tdps, vmin) if not np.isnan(v)]
    print(f"k_tim={k:2d}: feasible up to ~{max(ok):.0f} W at 15 m/s for Tj<={TJ_MAX} C")
plt.xlabel("TDP (W)"); plt.ylabel("Min airflow (m/s)"); plt.title(f"Airflow needed for Tj <= {TJ_MAX:.0f} C")
plt.grid(alpha=.3); plt.legend(); plt.tight_layout(); plt.savefig("results/inverse_design.png", dpi=130)
