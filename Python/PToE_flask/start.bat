@echo off
REM Start script for the Interactive Periodic Table application (Windows)

echo.
echo ==========================================
echo ===== Interactive Periodic Table =========
echo ==========================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
echo Checking dependencies...
pip list | findstr Flask >nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo ==========================================
echo Starting Flask Application
echo ==========================================
echo.
echo Open your browser to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the app
python run.py

pause
