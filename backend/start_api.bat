@echo off
REM Script to run the FastAPI service

echo Installing dependencies...
pip install -e .

echo Starting FastAPI server...
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000