"""
Extra validation:
 A) Hyper-parameter tuning (GridSearchCV) of Gradient Boosting, final models saved to models/
 B) Fresh-data test: 1000 NEW random points evaluated with the physics code (never seen in training)
 C) Extrapolation test: train on V<=8 m/s, test on V>8 (shows where surrogates break)
"""
import numpy as np, pandas as pd, joblib, os, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from heat_sink_model import heat_sink_design

os.makedirs("models", exist_ok=True)
df = pd.read_csv("data/heatsink_dataset.csv")
F = ["TDP_W", "V_air_mps", "k_tim_WmK"]; T = ["R_total_C_per_W", "T_junction_C"]
def m(y, p): return dict(MAE=mean_absolute_error(y, p), RMSE=np.sqrt(mean_squared_error(y, p)), R2=r2_score(y, p))
def pf(X):
    X = X.copy(); X["V_m13"] = X.V_air_mps ** (-1/3); X["inv_k"] = 1 / X.k_tim_WmK; return X

# A) tuning + save
grid = {"n_estimators": [200, 400], "max_depth": [2, 3], "learning_rate": [0.05, 0.1]}
best = {}
for t in T:
    gs = GridSearchCV(GradientBoostingRegressor(random_state=0), grid, cv=3, scoring="r2", n_jobs=-1).fit(df[F], df[t])
    best[t] = gs.best_estimator_
    print(t, "best params:", gs.best_params_, "CV R2 = %.5f" % gs.best_score_)
    joblib.dump(best[t], f"models/gb_{t}.joblib")

# B) fresh physics points
rng = np.random.default_rng(123)
fresh = pd.DataFrame({"TDP_W": rng.uniform(30, 250, 1000), "V_air_mps": rng.uniform(.5, 15, 1000), "k_tim_WmK": rng.uniform(1, 12, 1000)})
truth = pd.DataFrame([heat_sink_design(TDP=a, V_air=b, k_tim=c) for a, b, c in fresh.values])
rows = []
for t, col in zip(T, ["R_total", "T_j"]):
    rows.append(dict(Test="fresh points", Target=t, Model="GB tuned", **m(truth[col], best[t].predict(fresh))))
print(pd.DataFrame(rows).round(5).to_string(index=False))

# C) extrapolation: train V<=8, test V>8
tr, te = df[df.V_air_mps <= 8], df[df.V_air_mps > 8]
ext = []
for t in T:
    for name, mk, feat in [("Random Forest", lambda: RandomForestRegressor(300, random_state=0, n_jobs=-1), lambda X: X),
                           ("Gradient Boosting", lambda: GradientBoostingRegressor(n_estimators=400, random_state=0), lambda X: X),
                           ("Linear + physics features", LinearRegression, pf)]:
        mdl = mk().fit(feat(tr[F]), tr[t])
        ext.append(dict(Test="extrapolation V>8", Target=t, Model=name, **m(te[t], mdl.predict(feat(te[F])))))
ext = pd.DataFrame(ext); print(ext.round(5).to_string(index=False))
pd.concat([pd.DataFrame(rows), ext]).to_csv("results/validation.csv", index=False)
