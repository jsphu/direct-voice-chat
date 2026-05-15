@echo off
setlocal enabledelayedexpansion

echo --- P2P Voice Chat: Windows Setup ^& Run ---

:: 1. Check for Python
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b 1
)

:: 2. Virtual Environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

:: 3. Install Requirements
echo Installing/Updating Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

:: 4. Run Application
echo Launching application...
python main.py %*

if %ERRORLEVEL% neq 0 (
    echo.
    echo Application exited with an error.
    pause
)
