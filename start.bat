@echo off

REM Check if venv folder exists
IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Check if requirements are installed (we're using psutil as an example)
python -c "import psutil" 2> NUL
IF ERRORLEVEL 1 (
    echo Installing requirements...
    pip install -r requirements.txt
)

REM Start the app
python app.py

REM Deactivate the virtual environment when the app stops
call venv\Scripts\deactivate.bat
