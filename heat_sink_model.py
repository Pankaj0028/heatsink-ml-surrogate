"""
heat_sink_model.py
Refactored version of the provided Heat_Sink_calculation.py.
The physics is UNCHANGED; it is wrapped in a function so it can be called
thousands of times with different TDP / air velocity / k_tim values.

Two modes:
  mode="script"    -> exactly what the provided .py does (R_jc = 0.2, no base conduction term)
  mode="reference" -> follows the PDF report (R_jc = 0.1, adds R_cond = t_base/(k_Al*A_die))
"""
import numpy as np

# ---------------- Fixed design inputs (from the provided script) ----------------
FIXED = dict(
    L_die=0.0525, W_die=0.045,          # m
    T_ambient=25.0,                      # C
    L=90e-3, W=116e-3, H=27e-3,          # heat sink, m
    Fin_Thickness=0.8e-3, N_fins=60, Base_Thickness=2.5e-3,
    t_tim=0.1e-3,                        # m
    k_Al=167.0,                          # W/mK (Al 6061-T6, used only in "reference" mode)
    # air @ 25 C
    k_air=0.0262, nu_air=1.57e-5, Pr_air=0.71,
)


def heat_sink_design(TDP=150.0, V_air=1.0, k_tim=4.0, mode="script", verbose=False, **override):
    p = {**FIXED, **override}
    R_jc = 0.2 if mode == "script" else 0.1

    # fin spacing
    s_f = (p["W"] - p["N_fins"] * p["Fin_Thickness"]) / (p["N_fins"] - 1)

    # Reynolds & Nusselt (laminar Sieder-Tate-type / turbulent Dittus-Boelter)
    Re = V_air * s_f / p["nu_air"]
    if Re < 2300:
        Nu = 1.86 * ((Re * p["Pr_air"] * (2 * s_f) / p["L"]) ** (1 / 3))
    else:
        Nu = 0.023 * (Re ** 0.8) * (p["Pr_air"] ** 0.3)

    h = Nu * p["k_air"] / (2 * s_f)

    # areas
    h_fin = p["H"] - p["Base_Thickness"]
    A_fin = p["N_fins"] * (2 * h_fin * p["L"]) + s_f * p["L"]
    A_base_conv = p["L"] * p["W"] - p["Fin_Thickness"] * p["N_fins"] * p["L"]
    A_total = A_fin + A_base_conv

    R_conv = 1.0 / (h * A_total)
    A_die = p["L_die"] * p["W_die"]
    R_tim = p["t_tim"] / (k_tim * A_die)
    R_cond = p["Base_Thickness"] / (p["k_Al"] * A_die) if mode == "reference" else 0.0

    R_total = R_jc + R_tim + R_cond + R_conv
    T_j = p["T_ambient"] + TDP * R_total

    out = dict(Re=Re, Nu=Nu, h=h, R_conv=R_conv, R_tim=R_tim, R_cond=R_cond,
               R_total=R_total, T_j=T_j)
    if verbose:
        for k, v in out.items():
            print(f"{k:8s} = {v:.6g}")
    return out


if __name__ == "__main__":
    print("--- script mode (matches provided code) ---")
    heat_sink_design(verbose=True)
    print("--- reference mode (matches PDF steps) ---")
    heat_sink_design(mode="reference", verbose=True)
