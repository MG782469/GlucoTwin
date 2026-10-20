@echo off
python -m src.train
streamlit run src/app.py
