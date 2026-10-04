$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$env:PYTHONPATH = (Join-Path $PSScriptRoot 'src')

# Auto-detect Python interpreter (use .venv if present)
$PythonExe = 'python'
if (Test-Path '..\.venv\Scripts\python.exe') {
    $PythonExe = (Resolve-Path '..\.venv\Scripts\python.exe').Path
} elseif (Test-Path '.\.venv\Scripts\python.exe') {
    $PythonExe = (Resolve-Path '.\.venv\Scripts\python.exe').Path
}

Write-Host "Using Python: $PythonExe" -ForegroundColor Cyan
Write-Host "Installing/Verifying requirements..." -ForegroundColor Yellow
& $PythonExe -m pip install -r .\requirements.txt --quiet

Write-Host "Starting Unified FastAPI Server on http://127.0.0.1:8000 ..." -ForegroundColor Green
Write-Host "Swagger Docs: http://127.0.0.1:8000/docs" -ForegroundColor Green
& $PythonExe -m uvicorn final.api:app --app-dir .\src --host 127.0.0.1 --port 8000
