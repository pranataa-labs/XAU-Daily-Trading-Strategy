@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Institutional Execution Engine - XAU/USD Daily Strategy
python sinyal_xau_daily.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to fetch live market feeds.
    echo Please verify internet connectivity.
    pause
    exit /b
)
echo.
pause >nul
