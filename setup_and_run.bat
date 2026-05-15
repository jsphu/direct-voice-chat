@echo off
setlocal enabledelayedexpansion

echo --- P2P Voice Chat: Windows Setup ^& Run ---

:: 1. Check for Python
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python not found. Attempting to install via winget...
    where winget >nul 2>nul
    if %ERRORLEVEL% eq 0 (
        echo Installing Python 3...
        winget install --id Python.Python.3 --source winget --silent --accept-package-agreements --accept-source-agreements
        echo.
        echo Python has been installed. 
        echo IMPORTANT: You MUST close this terminal and open a NEW one for the changes to take effect.
        echo After opening a new terminal, run your command again.
        pause
        exit /b 1
    ) else (
        echo Error: Python is not installed and 'winget' was not found. 
        echo Please install Python manually from https://www.python.org/downloads/
        pause
        exit /b 1
    )
)

:: 2. Check for Pip
python -m pip --version >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Pip not found. Attempting to bootstrap pip...
    python -m ensurepip --default-pip
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
