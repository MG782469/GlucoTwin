"""Synthetic-only GlucoTwin data generator. Not clinical evidence."""
from __future__ import annotations
import numpy as np
import pandas as pd

STATIC_COLS = ["age", "bmi", "hba1c", "diabetes_duration_years", "on_glucose_lowering_medication"]
LAG_COLS = [f"cgm_lag_{i}" for i in range(16)]
DYNAMIC_COLS = ["cgm_mean_4h", "cgm_std_4h", "cgm_slope_4h", "meal_recent_4h"]
FEATURE_COLS = STATIC_COLS + LAG_COLS + DYNAMIC_COLS

def generate_patient_series(patient_idx: int, seed: int = 42, days: int = 5):
    """Return one fully synthetic patient profile, CGM series, and meal event flags."""
    rng = np.random.default_rng(seed + patient_idx * 17)
    age = int(rng.integers(28, 82))
    bmi = float(np.round(rng.normal(30, 5), 1))
    hba1c = float(np.round(np.clip(rng.normal(8.0, 1.15), 6.1, 11.8), 1))
    duration = float(np.round(rng.uniform(1, 24), 1))
    med = int(rng.random() < 0.68)
    n = days * 96  # 15-minute samples
    base = 98 + max(0, hba1c - 6.2) * 11 + max(0, bmi - 24) * 0.55 - med * 10
    values = np.zeros(n, dtype=float)
    meals = np.zeros(n, dtype=int)
    values[0] = np.clip(base + rng.normal(0, 9), 65, 190)
    # Meal events are placed near usual meal periods with patient-specific variation.
    for day in range(days):
        for hour in (7, 12, 18):
            pos = day * 96 + int(np.clip(hour + rng.integers(-1, 2), 0, 23) * 4)
            meals[pos] = 1
    for t in range(1, n):
        # Smooth reversion toward patient baseline.
        delta = 0.18 * (base - values[t-1]) + rng.normal(0, 7)
        # A meal produces a decaying excursion over subsequent 15-minute readings.
        for lag in range(0, min(16, t)):
            if meals[t-lag]:
                delta += (16 if not med else 12) * np.exp(-lag / 5.5)
        # Mild day/night variation.
        hour = (t % 96) / 4
        delta += 3 * np.sin((hour - 5) * np.pi / 12)
        values[t] = np.clip(values[t-1] + delta, 50, 340)
    profile = {
        "patient_id": f"SYN-{patient_idx:03d}",
        "age": age, "bmi": bmi, "hba1c": hba1c,
        "diabetes_duration_years": duration,
        "on_glucose_lowering_medication": med,
    }
    return profile, values, meals

def build_synthetic_windows(n_patients: int = 100, days: int = 5, seed: int = 42) -> pd.DataFrame:
    """Build past-only 4-hour windows with a next-hour threshold-crossing label."""
    rows = []
    for pidx in range(n_patients):
        profile, cgm, meals = generate_patient_series(pidx, seed=seed, days=days)
        for t in range(15, len(cgm) - 4):
            current = float(cgm[t])
            # Define a *new* crossing only when current glucose is not already above range.
            if current > 180:
                continue
            # Past-only input window includes the current reading and 15 previous readings.
            hist = cgm[t-15:t+1]
            future = cgm[t+1:t+5]
            label = int(np.any(future > 180))
            x = {k: profile[k] for k in STATIC_COLS}
            x.update({f"cgm_lag_{i}": float(hist[-1-i]) for i in range(16)})
            x["cgm_mean_4h"] = float(np.mean(hist))
            x["cgm_std_4h"] = float(np.std(hist))
            x["cgm_slope_4h"] = float((hist[-1] - hist[0]) / 15.0)
            x["meal_recent_4h"] = int(np.any(meals[max(0, t-15):t+1] == 1))
            x["patient_id"] = profile["patient_id"]
            x["time_idx"] = t
            x["current_glucose"] = current
            x["label"] = label
            rows.append(x)
    return pd.DataFrame(rows)

def generate_demo_patient(patient_idx: int = 7, seed: int = 42, days: int = 5):
    """Convenience wrapper for app display."""
    profile, cgm, meals = generate_patient_series(patient_idx, seed=seed, days=days)
    return profile, cgm, meals
