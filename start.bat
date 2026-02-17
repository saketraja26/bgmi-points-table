@echo off
echo ========================================
echo AAROHAN BGMI ELIMS - Points Table System
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install dependencies
echo Installing/Updating dependencies...
pip install -q -r requirements.txt
echo.

REM Start Flask application
echo ========================================
echo Starting Flask server...
echo.
echo Open your browser and go to:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause
