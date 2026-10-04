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

Write-Host "`n1. Creating Indexes..." -ForegroundColor Green
& $PythonExe -m final.cli indexes

Write-Host "`n2. Running Explain executionStats benchmarks..." -ForegroundColor Green
& $PythonExe -m final.cli explain

Write-Host "`n3. Running Full Materialized View Refresh..." -ForegroundColor Green
& $PythonExe -m final.cli refresh-full

Write-Host "`n4. Running Aggregation Report: sales_by_city..." -ForegroundColor Green
& $PythonExe -m final.cli report sales_by_city

Write-Host "`n5. Running Aggregation Report: top_products..." -ForegroundColor Green
& $PythonExe -m final.cli report top_products
