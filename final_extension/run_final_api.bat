@echo off
set PYTHONPATH=%~dp0src
set PYTHON_EXE=..\.venv\Scripts\python.exe

if not exist "%PYTHON_EXE%" (
    set PYTHON_EXE=python
)

echo ========================================================
echo Starting Al-Razi Final Extension FastAPI Server
echo Using: %PYTHON_EXE%
echo URL: http://127.0.0.1:8000
echo Swagger Docs: http://127.0.0.1:8000/docs
echo ========================================================

"%PYTHON_EXE%" -m uvicorn final.api:app --app-dir "%~dp0src" --host 127.0.0.1 --port 8000
pause
