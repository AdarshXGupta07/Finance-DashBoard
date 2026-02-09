@echo off
echo Personal Finance Dashboard - SQLite Version
echo ===========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ and add it to your PATH
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
python -m pip install pandas sqlalchemy streamlit plotly pillow

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.
echo Starting Streamlit application...
echo The application will open in your default browser
echo.

cd scripts
streamlit run app_sqlite.py

pause
