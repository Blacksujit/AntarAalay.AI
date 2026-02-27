@echo off
echo Starting AntarAalay Backend with Flux AI Engine...
set HF_TOKEN=test_token_for_testing
set AI_ENGINE=flux_working
echo Environment variables set:
echo HF_TOKEN=%HF_TOKEN%
echo AI_ENGINE=%AI_ENGINE%
echo.
echo Starting backend server on http://127.0.0.1:8000
python -m uvicorn main:app --reload --port 8000
pause
