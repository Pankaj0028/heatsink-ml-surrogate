"""Runs the whole pipeline: dataset -> ML -> sensitivity -> validation -> inverse design."""
import subprocess, sys

SCRIPTS = [
    "01_generate_dataset.py",
    "02_ml_surrogate.py",
    "03_sensitivity.py",
    "04_validation_and_tuning.py",
    "05_inverse_design.py",
]

for s in SCRIPTS:
    print(f"\n===== {s} =====")
    subprocess.run([sys.executable, s], check=True)

print("\nDone. Outputs in data/, results/, models/")
print("Optional demo: streamlit run app.py")
print("Optional CLI:  python predict.py 150 1 4")
