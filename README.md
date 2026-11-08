# Heat-Sink Surrogate Model Project (Expert Thermal / XThermal assessment, Task 1)

**Repo:** https://github.com/Pankaj0028/heatsink-ml-surrogate

## Software
| Need | Use |
|---|---|
| Python 3.10+ | python.org or Anaconda |
| Editor / notebook | VS Code (with Python + Jupyter extensions) or Jupyter Lab / Google Colab (free) |
| Libraries | `pip install -r requirements.txt` |
| Version control / portfolio link | Git + GitHub (assessment allows a GitHub link) |
| Report | Word / Google Docs -> export PDF |

## Run
```
pip install -r requirements.txt
python run_all.py
```

## Pipeline
1. `heat_sink_model.py`   – provided script wrapped in a function (same physics). `mode="script"` = provided code, `mode="reference"` = PDF steps (R_jc=0.1 + base conduction).
2. `01_generate_dataset.py` – 3000 Latin-Hypercube samples + 8 corners over TDP 30-250 W, V 0.5-15 m/s, k_tim 1-12 W/mK -> `data/heatsink_dataset.csv`
3. `02_ml_surrogate.py`     – Linear Regression, Random Forest, Gradient Boosting, MLP; MAE/RMSE/R2 + 5-fold CV -> `results/ml_accuracy.csv`, `results/pred_vs_actual.png`
4. `03_sensitivity.py`     – Pearson/Spearman, standardised coefficients, permutation importance, elasticities -> `results/sensitivity.*`, `results/design_space.png`
5. `04_extras.py` – tuned Gradient Boosting, extrapolation test (train V<=10, test V>10), inverse design (min airflow for Tj limit); saves `models/`
6. `app.py` – Streamlit demo: `streamlit run app.py` (physics vs surrogate, limit check)
7. `Heatsink_Surrogate_Notebook.ipynb` – notebook version of the pipeline (deliverable a)
8. `report_template.md`    – skeleton for the concise summary report (deliverable f)

## Notes you should be able to explain in an interview
* In this model R_total does NOT depend on TDP (resistances are constants), so T_j = T_amb + TDP*R_total is just linear in TDP. TDP only matters for T_j.
* Re is 37-1100 over the whole sweep, so flow is always laminar (<2300); h ~ V^(1/3), hence diminishing returns from more airflow.
* Provided script gives R_total = 0.3692 C/W, Tj = 80.38 C; the Excel reference in the PDF says 0.3730 / 80.96 C (~1% apart), and the PDF's own formulas (R_jc=0.1 + R_cond) give 0.2755 C/W. Mention this discrepancy in your assumptions/limitations.
* Surrogates trained on an analytical model only reproduce that model – the real value is the workflow; with CFD/test data the same pipeline applies.

## Extra findings
* Extrapolation: tree models (RF/GB) fall apart on R_total outside the training range (R² ~0.4-0.45 for V 10-15 m/s), while a linear model on physics features stays exact. Good argument for physics-informed AI.
* Inverse design (k_tim=4, Tj<=85 C): 150 W needs ~0.6 m/s, 200 W ~5.6 m/s, 250 W cannot be met within 15 m/s with this heat sink.

## Add-ons
* `HeatSink_Project_Notebook.ipynb` – executed notebook running the full pipeline (deliverable a, notebook form).
* `04_validation_and_tuning.py` – tuned Gradient Boosting (saved in `models/`), 1000 fresh physics points, extrapolation test -> `results/validation.csv`.
* `05_inverse_design.py` – minimum airflow to keep Tj <= 85 C vs TDP and TIM grade -> `results/inverse_design.png`.
* `predict.py` – `python predict.py 150 1 4` compares surrogate vs physics.
* `app.py` – demo web app: `streamlit run app.py` (pip install streamlit).

## Extra findings
* Fresh-data test: tuned GB R2 = 0.9994 (R_total), 0.9995 (Tj).
* Direct Tj model can be ~1.6 C off at low airflow (nominal point); the hybrid (ML predicts R_total, then Tj = Tamb + TDP*R_total) is within ~0.1 C. Physics-structured outputs beat black-box outputs.
* Extrapolation (train V<=8, test V>8): tree models fail on R_total (R2 < 0), while a linear model with physics features (V^-1/3, 1/k) stays exact. Good example of why physics-aware AI matters.
