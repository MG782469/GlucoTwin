import numpy as np
from src.synthetic_data import generate_patient_series, build_synthetic_windows, FEATURE_COLS

def test_synthetic_patient_series_shape():
    profile, cgm, meals = generate_patient_series(0, seed=42, days=2)
    assert profile["patient_id"] == "SYN-000"
    assert len(cgm) == 2 * 96
    assert len(meals) == len(cgm)
    assert np.isfinite(cgm).all()

def test_windows_have_expected_features_and_labels():
    df = build_synthetic_windows(n_patients=3, days=2, seed=1)
    assert set(FEATURE_COLS).issubset(df.columns)
    assert set(df["label"].unique()).issubset({0,1})
    assert (df["current_glucose"] <= 180).all()
    assert df["patient_id"].nunique() == 3
