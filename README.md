# GlucoTwin — Patient-Specific Glucose-Excursion Forecasting

**Digital Twin Challenge 2026 — Happiest Health**

> **Submission status:** This package includes a synthetic-data demonstration pipeline and supporting documents. It does **not** establish clinical performance or clinical validation. The primary public dataset plan is ShanghaiT2DM; do not claim it was used unless you actually download it and run the documented experiments.

## Team details

- **Team leader:** Manas Girdhar — BIT Mesra
- **Team member:** Moulvi Gufran — GMC Vizianagaram
- **College / incubator:** Team members are from separate institutions: BIT Mesra and GMC Vizianagaram.
- **Registered team roster:** Verify that both names and roles match the Unstop registration exactly.
- **Project title:** GlucoTwin — A patient-specific digital twin for short-horizon glucose-excursion forecasting.

## Problem statement

Historical clinical records give a baseline view of a person’s health, while continuous glucose monitoring (CGM) shows how glucose changes over time. A clinician-facing digital twin should combine these streams into an updating patient state and estimate a clearly defined future event.

GlucoTwin is a scoped proof-of-concept for adults with Type 2 diabetes. The target event is a new above-range glucose excursion within the next 60 minutes: for windows where current CGM is at or below 180 mg/dL, the label is positive if any of the next four 15-minute CGM measurements exceeds 180 mg/dL. The threshold is a monitoring reference, not a diagnosis or emergency classification.

## Healthcare use case

A clinician or diabetes-care team can inspect the patient’s baseline clinical profile, recent CGM trajectory, recorded meal/medication events, the 60-minute forecast, input freshness, model version, and prior predictions. The tool is for research demonstration only: it does not diagnose, prescribe, recommend insulin doses, or replace clinical judgment.

## Data plan and evidence status

### Primary public dataset selected for research evaluation: ShanghaiT2DM
- Dataset paper: https://www.nature.com/articles/s41597-023-01940-7
- Figshare collection: https://figshare.com/collections/Diabetes_Datasets_ShanghaiT1DM_and_ShanghaiT2DM/6310860
- The published dataset includes 100 people with Type 2 diabetes, CGM sampled every 15 minutes, and patient-level clinical/laboratory, medication and dietary records.
- The Figshare record lists CC BY 4.0; cite the source and retain attribution. Review the source terms before redistributing data.
- **Do not claim the ShanghaiT2DM data were used in measured results until the dataset has actually been downloaded, inspected, and evaluated.**
- **Population limitation:** this cohort is from China and does not establish performance for Indian patients.

### Optional independent exploratory dataset: CGMacros
- Paper: https://www.nature.com/articles/s41597-025-05851-7
- PhysioNet: https://physionet.org/content/cgmacros/1.0.0/
- Includes CGM, Fitbit heart rate/activity, meals, and baseline clinical measurements from 45 participants, including 14 with Type 2 diabetes. Use only as a separate exploratory evaluation; never join patient identities across datasets.

## Technical stack

- Python 3.10+
- pandas / NumPy
- scikit-learn (synthetic-demo model and evaluation)
- Streamlit (interactive synthetic demo dashboard)
- joblib (local model artifact)
- pytest (basic tests)

## AI/ML model or framework details

The repository provides:
1. A **synthetic demonstration generator** for paired baseline clinical features, 15-minute CGM trajectories, and meal events.
2. A time-window feature builder using the previous 16 CGM readings (4 hours), rolling summary features, baseline clinical features, and recent-meal context.
3. A patient-level train/test split to avoid placing windows from the same synthetic person in both sets.
4. A scikit-learn HistGradientBoostingClassifier and a simple current-glucose threshold baseline.
5. Evaluation metrics: AUROC, AUPRC, sensitivity, specificity, Brier score, and false alerts per patient-day where defined.
6. A Streamlit dashboard that advances a synthetic patient state and re-runs the forecast.

**Important:** metrics produced from generated synthetic data are software smoke-test results only. They are not evidence of clinical accuracy and must not be presented as such. For the challenge's strongest evidence, add a separate real-data evaluation on ShanghaiT2DM, preserve patient-level separation, and compare static-only, CGM-only, and fused models.

## Run the synthetic demo

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python -m src.train
streamlit run src/app.py
```

The app labels all simulated values and probabilities as synthetic. It does not require a live CGM device.

## Architecture diagram and presentation

- Architecture diagram: [`docs/GlucoTwin_Architecture_Diagram.pdf`](docs/GlucoTwin_Architecture_Diagram.pdf)
- Presentation (PowerPoint): [`docs/GlucoTwin_Digital_Twin_Challenge_2026.pptx`](docs/GlucoTwin_Digital_Twin_Challenge_2026.pptx)
- Presentation (PDF): [`docs/GlucoTwin_Digital_Twin_Challenge_2026.pdf`](docs/GlucoTwin_Digital_Twin_Challenge_2026.pdf)
- Research and compliance pack: [`docs/GlucoTwin_Research_and_Compliance_Pack.docx`](docs/GlucoTwin_Research_and_Compliance_Pack.docx)
- Demo video script: [`docs/GlucoTwin_20_Minute_Demo_Script.docx`](docs/GlucoTwin_20_Minute_Demo_Script.docx)

## 15–20 minute demo video

**Required action before submission:** record the walkthrough, upload it to YouTube as **Unlisted**, and replace the placeholder below with the working link. The screenshot of the submission form says “15–20 minute Demo Video”; the previously reviewed challenge listing appeared to say a minimum of 20 minutes. To meet both interpretations, aim for exactly 20:00 and re-check the current portal instructions.

- **Unlisted YouTube video:** `[ADD VIDEO URL AFTER UPLOAD]`
- **Duration:** `[ADD FINAL RUNTIME]`
- **Checked in logged-out browser:** `[YES/NO]`

Do not claim the public dataset model or a live device connection is running unless you demonstrate it.

## Public repository checklist

Before submitting, ensure this repository is **Public** and every link works without additional permissions.

- [x] Team details — names included; confirm exact registered roster.
- [x] College/incubator information — **placeholder remains; must be completed**.
- [x] Project title.
- [x] Problem statement.
- [x] Healthcare use case.
- [x] Technical stack.
- [x] AI/ML model or framework details.
- [ ] 15–20 minute demo video uploaded as Unlisted YouTube and linked above.
- [x] Open-source licence details (see below).
- [x] Architecture diagram in PDF format.
- [x] Presentation in PPT/PDF format.
- [ ] All files and links public and tested without additional permissions.
- [ ] Replace any placeholder fields and confirm that claims match the working implementation.

## Open-source licence details

- **Code:** MIT License, see [`LICENSE`](LICENSE).
- **Dataset:** ShanghaiT2DM source record lists CC BY 4.0; that licence applies to the dataset under its own terms, not automatically to this repository's code.
- Keep source attribution in [`CITATION.md`](CITATION.md). Do not upload private information, access tokens, or unnecessary raw patient data.

## Limitations and safety

- Research prototype, not a clinically validated medical device.
- No diagnosis, medication advice, insulin-dose advice, or autonomous action.
- Synthetic-demo metrics are not clinical evidence.
- The primary research cohort is small and from China; no Indian-population validation is claimed.
- Missing or stale input should lead to a warning/abstention rather than a confident prediction.
- External and prospective validation, clinical workflow assessment, ethics/data approvals, and applicable regulatory review would be required before clinical use.

## References

1. Zhao Q et al. *Chinese diabetes datasets for data-driven machine learning.* Scientific Data (2023). https://www.nature.com/articles/s41597-023-01940-7
2. ShanghaiT1DM / ShanghaiT2DM collection. Figshare. https://figshare.com/collections/Diabetes_Datasets_ShanghaiT1DM_and_ShanghaiT2DM/6310860
3. Das A et al. *CGMacros.* Scientific Data (2025). https://www.nature.com/articles/s41597-025-05851-7
4. CGMacros dataset. PhysioNet. https://physionet.org/content/cgmacros/1.0.0/
5. Thomsen HB et al. *Racial disparities in continuous glucose monitoring-based 60-min glucose predictions among people with type 1 diabetes.* PLOS Digital Health (2025). https://journals.plos.org/digitalhealth/article?id=10.1371/journal.pdig.0000918
6. Happiest Health Digital Twin Challenge 2026. https://unstop.com/hackathons/crp-digital-twin-challenge-2026-happiest-health-1757873
