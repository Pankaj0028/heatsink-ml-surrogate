"""
Task 1c: ML surrogate models for R_total and T_junction.
Models  : Linear Regression (baseline)  |  Random Forest  |  Gradient Boosting  |  Neural net (MLP)
Metrics : MAE, RMSE, R2 on a held-out 20% test set + 5-fold CV R2.
Also trains a "physics-informed features" variant (log V, 1/k_tim, TDP*1/k, ...) that
shows how feature engineering closes the gap for simple models.
"""
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.compose import TransformedTargetRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = pd.read_csv("data/heatsink_dataset.csv")
FEATS = ["TDP_W", "V_air_mps", "k_tim_WmK"]
TARGETS = ["R_total_C_per_W", "T_junction_C"]

def phys_feats(X):
    X = X.copy()
    X["logV"] = np.log(X["V_air_mps"])
    X["inv_k"] = 1.0 / X["k_tim_WmK"]
    X["V_m13"] = X["V_air_mps"] ** (-1 / 3)   # h ~ V^(1/3) in laminar regime
    return X

models = {
    "Linear Regression": lambda: make_pipeline(StandardScaler(), LinearRegression()),
    "Random Forest": lambda: RandomForestRegressor(n_estimators=300, random_state=0, n_jobs=-1),
    "Gradient Boosting": lambda: GradientBoostingRegressor(n_estimators=400, max_depth=3, learning_rate=0.05, random_state=0),
    "Neural Net (MLP)": lambda: TransformedTargetRegressor(make_pipeline(StandardScaler(), MLPRegressor(hidden_layer_sizes=(64, 64), max_iter=3000, random_state=0)), transformer=StandardScaler()),
}

results = []
preds = {}
for target in TARGETS:
    Xtr, Xte, ytr, yte = train_test_split(df[FEATS], df[target], test_size=0.2, random_state=42)
    for name, mk in models.items():
        for variant in ("raw features", "physics features"):
            if variant == "physics features" and name not in ("Linear Regression", "Gradient Boosting"):
                continue
            a, b = (Xtr, Xte) if variant == "raw features" else (phys_feats(Xtr), phys_feats(Xte))
            m = mk().fit(a, ytr)
            p = m.predict(b)
            cv = cross_val_score(mk(), a, ytr, cv=5, scoring="r2").mean()
            results.append(dict(Target=target, Model=name, Features=variant,
                                MAE=mean_absolute_error(yte, p),
                                RMSE=np.sqrt(mean_squared_error(yte, p)),
                                R2=r2_score(yte, p), CV_R2=cv))
            if variant == "raw features":
                preds[(target, name)] = (yte.values, p)

res = pd.DataFrame(results)
res.to_csv("results/ml_accuracy.csv", index=False)
pd.set_option("display.width", 200)
print(res.round(5).to_string(index=False))

# predicted-vs-actual plots
fig, ax = plt.subplots(2, 4, figsize=(18, 8))
for i, t in enumerate(TARGETS):
    for j, n in enumerate(models):
        y, p = preds[(t, n)]
        ax[i, j].scatter(y, p, s=5, alpha=.5)
        ax[i, j].plot([y.min(), y.max()], [y.min(), y.max()], "r--")
        ax[i, j].set_title(f"{n}\n{t}"); ax[i, j].set_xlabel("Actual"); ax[i, j].set_ylabel("Predicted")
plt.tight_layout(); plt.savefig("results/pred_vs_actual.png", dpi=130)
