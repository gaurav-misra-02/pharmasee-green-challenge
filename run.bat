@echo off
REM PharmaSee Medicine Scanner - Quick Start Script for Windows

echo ================================================
echo    PharmaSee - Medicine Scanner
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python found
python --version

REM Check if virtual environment exists
if not exist "venv\" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist "venv\Lib\site-packages\cv2\" (
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
    echo Dependencies installed
)

REM Check if config file exists
if not exist "config\config.json" (
    echo.
    echo ERROR: config\config.json not found
    echo Please copy config\config.example.json to config\config.json
    echo and add your OpenAI API key
    pause
    exit /b 1
)

REM Check if API key is set
findstr /C:"\"api_key\": \"\"" config\config.json >nul 2>&1
if not errorlevel 1 (
    echo.
    echo WARNING: OpenAI API key not set in config\config.json
    echo Please add your API key before running
    pause
    exit /b 1
)

echo.
echo Configuration loaded
echo.
echo ================================================
echo Starting PharmaSee...
echo ================================================
echo.

REM Run the application
cd src
python medicine_scanner.py

REM Deactivate virtual environment when done
cd ..
call venv\Scripts\deactivate.bat

pause


