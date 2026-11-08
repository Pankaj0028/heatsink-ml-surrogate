"""
Task 1a/1b: parameter sweep -> data/heatsink_dataset.csv
Sampling: Latin Hypercube (space-filling, far fewer points than a full grid)
          + the 4 corners of the box, so extremes are always present.
Ranges  : TDP 30-250 W | V_air 0.5-15 m/s | k_tim 1-12 W/mK
"""
import numpy as np, pandas as pd
from scipy.stats import qmc
from heat_sink_model import heat_sink_design

N = 3000
SEED = 42
lo = np.array([30.0, 0.5, 1.0])
hi = np.array([250.0, 15.0, 12.0])

X = qmc.LatinHypercube(d=3, seed=SEED).random(N)
X = qmc.scale(X, lo, hi)
# add all 8 corners of the design space
corners = np.array([[a, b, c] for a in (lo[0], hi[0]) for b in (lo[1], hi[1]) for c in (lo[2], hi[2])])
X = np.vstack([X, corners])

rows = []
for tdp, v, k in X:
    r = heat_sink_design(TDP=tdp, V_air=v, k_tim=k, mode="script")
    rows.append(dict(TDP_W=tdp, V_air_mps=v, k_tim_WmK=k, **r))

df = pd.DataFrame(rows).rename(columns={"R_total": "R_total_C_per_W", "T_j": "T_junction_C"})
df.to_csv("data/heatsink_dataset.csv", index=False)
print(df.shape); print(df.describe().T[["min", "max", "mean"]])
