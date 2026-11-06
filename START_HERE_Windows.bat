@echo off
title KEBAL
cd /d "%~dp0"
echo ============================================
echo    KEBAL - starting up...
echo ============================================
echo.

REM ---- 1. Find Python -------------------------------------------------
set "PY="
py -3 --version >nul 2>&1
if %errorlevel%==0 (
    set "PY=py -3"
    goto found
)
python --version >nul 2>&1
if %errorlevel%==0 (
    set "PY=python"
    goto found
)
echo [X] Python is not installed (or not on PATH).
echo.
echo     1. Download Python from python.org (opening it now)
echo     2. During install, TICK the box "Add python.exe to PATH"
echo     3. Then double-click this file again.
start "" https://www.python.org/downloads/
pause
exit /b 1

:found
echo [OK] Found Python:
%PY% --version
echo.

REM ---- 2. First run only: create a private environment and install ----
if exist ".venv\installed.ok" goto run
echo First run: installing what the app needs (2-5 minutes, needs internet)...
%PY% -m venv .venv
if errorlevel 1 (
    echo [X] Could not create the environment. Try reinstalling Python from python.org.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [X] Install failed. Check your internet connection and try again.
    pause
    exit /b 1
)
echo ok> ".venv\installed.ok"

:run
echo.
echo [OK] Opening KEBAL in your browser...
echo      Keep this window OPEN while using the app. Close it to stop the app.
echo.
".venv\Scripts\python.exe" -m streamlit run app.py
pause
