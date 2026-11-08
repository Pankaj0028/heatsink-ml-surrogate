"""Fast surrogate prediction:  python predict.py 150 1 4   (TDP W, V m/s, k_tim W/mK)"""
import sys, joblib, pandas as pd
from heat_sink_model import heat_sink_design
tdp, v, k = map(float, sys.argv[1:4])
x = pd.DataFrame([[tdp, v, k]], columns=["TDP_W", "V_air_mps", "k_tim_WmK"])
R = joblib.load("models/gb_R_total_C_per_W.joblib").predict(x)[0]
Tj = joblib.load("models/gb_T_junction_C.joblib").predict(x)[0]
ph = heat_sink_design(TDP=tdp, V_air=v, k_tim=k)
Tj_h = 25.0 + tdp * R   # physics-structured: ML predicts R_total, Tj = Tamb + TDP*R_total
print(f"Surrogate (direct Tj)  : R_total={R:.4f} C/W  Tj={Tj:.2f} C")
print(f"Surrogate (hybrid  Tj) : Tj={Tj_h:.2f} C")
print(f"Physics   : R_total={ph['R_total']:.4f} C/W  Tj={ph['T_j']:.2f} C")
