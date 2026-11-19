@echo off
title Employee Payroll Management System
echo ===================================================================
echo Starting Employee Payroll Management System...
echo ===================================================================

:: Start default web browser after 1 second
start "" cmd /c "timeout /t 1 /nobreak >nul & start http://127.0.0.1:5000"

:: Check for the primary Python installation
if exist "C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
    "C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" run.py
) else (
    python run.py
)

pause
