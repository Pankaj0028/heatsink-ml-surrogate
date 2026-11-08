# Task 3 – AI Use Case Evaluation  
**Engineering software platform (thermal / XThermal context)**

Suggests **5 AI features**. For each: problem solved, data required, AI type, and how to validate.

---

## 1. AI-assisted input validation & missing-parameter detection

**Problem it solves**  
Users often leave gaps (missing TIM thickness, inconsistent units, TDP outside sink capability). Bad inputs waste engineer time and produce silent wrong results.

**Data required**  
- Schema of required/optional fields per calculation type  
- Historical valid/invalid job logs (ranges, units, failure reasons)  
- Catalog of default materials / TIM grades  

**AI type**  
Combination: **rules + ML** (anomaly / range scoring) + light **GenAI** for plain-language explanations (“k_tim=0.05 looks like W/m·K mistyped as paste thickness”).

**How to validate**  
- Confusion matrix on labeled past jobs (false-accept / false-reject rates)  
- A/B: % of calculations that complete without rework  
- Expert review of flagged vs accepted edge cases  

---

## 2. ML surrogate for fast thermal prediction (what Task 1 builds)

**Problem it solves**  
Full analytical sweeps, CFD, or nested design loops are too slow for interactive “what-if” exploration. Engineers need sub-second estimates of `R_total` and `Tj`.

**Data required**  
- Parameter sweeps from trusted physics models (this project) and later CFD / lab measurements  
- Geometry, airflow, TIM, power, ambient metadata  

**AI type**  
**Classical ML** (Gradient Boosting / RF) with optional **physics-informed features**; later physics-aware / hybrid models.

**How to validate**  
- MAE / RMSE / R² vs held-out physics points (as in `results/ml_accuracy.csv`)  
- Fresh-point and extrapolation tests (`results/validation.csv`)  
- Hybrid check: ML predicts `R_total`, then `Tj = Tamb + TDP·R` vs direct physics  
- Acceptance gates: e.g. |ΔTj| < 1 °C inside training envelope  

---

## 3. Thermal design recommendations (inverse / constrained design)

**Problem it solves**  
Engineers ask “what minimum airflow / TIM / fin count keeps Tj ≤ 85 °C?” Trial-and-error is slow; inverse design turns the surrogate into a recommendation tool.

**Data required**  
- Trained surrogate + physics fallback  
- Constraint library (Tj limit, max fan speed, max pressure drop, cost/weight caps)  
- Feasible component catalog (fans, TIMs, sink SKUs)  

**AI type**  
**ML surrogate + optimization / workflow AI** (search over V, k_tim, catalog SKUs); GenAI only for explaining the recommendation in context.

**How to validate**  
- Re-evaluate recommended designs with the physics model (and CFD spot-checks)  
- Compare to known feasible/infeasible cases (e.g. 250 W not feasible within 15 m/s for this sink)  
- Track recommendation acceptance rate by thermal engineers  

---

## 4. Knowledge retrieval from engineering documents (RAG)

**Problem it solves**  
Specs, TIM datasheets, correlation validity ranges, and past project reports are scattered. Engineers need fast, cited answers instead of hunting PDFs.

**Data required**  
- Indexed corpus: datasheets, internal SOPs, past reports, correlation notes  
- Chunking metadata (doc type, revision, material family)  
- Access-control tags  

**AI type**  
**GenAI + RAG** (retrieval-augmented generation); not a standalone LLM guessing numbers.

**How to validate**  
- Golden Q&A set with expected citations  
- Measure faithfulness (answer grounded in retrieved chunks) and citation accuracy  
- Human thermal-SME review before production use for safety-critical guidance  

---

## 5. Result summarization & automated report generation

**Problem it solves**  
After a sweep or optimization, stakeholders need a short narrative: assumptions, key Tj/R numbers, risks, and recommended next action — not raw CSVs.

**Data required**  
- Structured run outputs (tables, plots, sensitivity ranks)  
- Report templates (customer vs internal)  
- Optional: past approved report language for tone/style  

**AI type**  
**GenAI + workflow AI** (template fill → LLM narrative → human approve). Numbers must come from the calculation engine, not from the LLM.

**How to validate**  
- Checklist: every number in the narrative matches source tables  
- Reviewer edit distance / approval time  
- Spot audits for hallucinated claims or missing limitations  

---

## Priority suggestion for a thermal product

| Priority | Feature | Why first |
|---|---|---|
| 1 | Surrogate + limit check | Immediate interactive value; Task 1 already demos this |
| 2 | Input validation | Cuts support load and bad runs |
| 3 | Inverse recommendations | Turns prediction into design decisions |
| 4 | Report generation | Speeds delivery once results are trusted |
| 5 | RAG over docs | High leverage once corpus is curated |

**Safety principle:** ML/GenAI may propose; **physics (or CFD/test) remains the source of truth** for acceptance-critical numbers.
