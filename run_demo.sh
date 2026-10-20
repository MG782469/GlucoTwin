#!/usr/bin/env bash
set -e
python -m src.train
streamlit run src/app.py
