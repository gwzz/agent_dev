@echo off
REM Development script to run the FastAPI service with auto-reload

echo Installing dependencies...
pip install -e .

echo Starting FastAPI server in development mode...
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload