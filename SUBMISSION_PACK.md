# Expert Thermal / XThermal – Assessment Submission Pack

**Project:** Heat-sink parameter sweep + ML surrogate  
**Code root:** this folder  
**Deadline reminder:** 2 days from receipt (per assessment PDF)

---

## Deliverables checklist

| ID | Deliverable | Location |
|---|---|---|
| a | Python / notebook (model + sweep) | `heat_sink_model.py`, `01_generate_dataset.py`, `HeatSink_Project_Notebook.ipynb` |
| b | CSV dataset | `data/heatsink_dataset.csv` |
| c | ML surrogate + accuracy | `02_ml_surrogate.py`, `04_validation_and_tuning.py`, `results/ml_accuracy.csv`, `models/` |
| d | Correlation / sensitivity | `03_sensitivity.py`, `results/sensitivity.png`, `results/sensitivity.xlsx` |
| e | Written Tasks 2–4 | Task 3: `Task3_AI_Use_Cases.md` · **Tasks 2 & 4: write yourself** |
| f | Concise summary report | `report_template.md` → export `Submission_Report.docx` |

**Extras (demo links you can mention):**  
`app.py` (Streamlit), `predict.py`, `05_inverse_design.py`, plots under `results/`

---

## How reviewers can reproduce

```text
pip install -r requirements.txt
python run_all.py
streamlit run app.py
python predict.py 150 1 4
```

---

## Task 2 & Task 4 – your own words

These sections must be written by you (Task 2: *No AI assistance*).  
Suggested empty outline only:

### Task 2 outline (fill yourself)
- Agentic AI  
- Workflow AI  
- AI copilots / assistants  
- Standalone model vs AI in a product workflow  
- Your experience: GenAI, LLMs, RAG, agents, automation, web/product integration  
- Or: how you would learn these if experience is limited  

### Task 4 outline (fill yourself)
- Why Expert Thermal / XThermal  
- What you want to build in AI/ML  
- Interest: ML vs GenAI vs physics-aware AI vs product integration  
- Handling ambiguous requirements  
- Startup pace comfort  
- Growth path on the team  
- Ownership / initiative examples  

---

## Files to attach / share

1. This project folder (or GitHub link once Git is set up)  
2. `Submission_Report.docx` (Task 1 technical summary)  
3. `Task3_AI_Use_Cases.md` (or paste into the same Word doc)  
4. Your Task 2 + Task 4 answers  
5. Optional: screenshots of `streamlit run app.py`
