"""Demo web app:  streamlit run app.py"""
import streamlit as st, joblib, pandas as pd
from heat_sink_model import heat_sink_design
st.set_page_config(page_title="Heat-sink surrogate demo")
st.title("Heat-sink thermal calculator + ML surrogate")
tdp = st.slider("TDP (W)", 30, 250, 150)
v = st.slider("Air velocity (m/s)", 0.5, 15.0, 1.0, 0.1)
k = st.slider("TIM conductivity (W/m·K)", 1.0, 12.0, 4.0, 0.5)
tj_lim = st.number_input("Junction temperature limit (°C)", value=85.0)
x = pd.DataFrame([[tdp, v, k]], columns=["TDP_W", "V_air_mps", "k_tim_WmK"])
R = joblib.load("models/gb_R_total_C_per_W.joblib").predict(x)[0]
Tj = 25.0 + tdp * R  # hybrid: ML predicts R_total, Tj = Tamb + TDP*R_total (more accurate than direct Tj model)
ph = heat_sink_design(TDP=tdp, V_air=v, k_tim=k)
c1, c2 = st.columns(2)
c1.metric("Surrogate Tj, hybrid (°C)", f"{Tj:.1f}"); c1.metric("Surrogate R_total (°C/W)", f"{R:.4f}")
c2.metric("Physics Tj (°C)", f"{ph['T_j']:.1f}"); c2.metric("Physics R_total (°C/W)", f"{ph['R_total']:.4f}")
st.caption(f"Reynolds number {ph['Re']:.0f} (laminar), h = {ph['h']:.1f} W/m²K")
(st.success if ph["T_j"] <= tj_lim else st.error)(
    "Within limit" if ph["T_j"] <= tj_lim else "Exceeds junction temperature limit — increase airflow or improve TIM")
