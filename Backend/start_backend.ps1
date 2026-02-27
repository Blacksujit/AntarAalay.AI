# Start AntarAalay Backend with Flux AI Engine
Write-Host "Starting AntarAalay Backend with Flux AI Engine..."

# Set environment variables
$env:HF_TOKEN="test_token_for_testing"
$env:AI_ENGINE="flux_working"

Write-Host "Environment variables set:"
Write-Host "HF_TOKEN=$env:HF_TOKEN"
Write-Host "AI_ENGINE=$env:AI_ENGINE"
Write-Host ""

Write-Host "Starting backend server on http://127.0.0.1:8000"
python -m uvicorn main:app --reload --port 8000
