@echo off
chcp 65001
title Gongmyung Manual Mode
echo [Gongmyung] Starting Daemon in Manual Mode (Eco)...
echo This will run only while this window is open.
echo.

:: 파이썬 경로 확인
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [Error] Python not found. Please install Python first.
    pause
    exit /b
)

set DAEMON_SCRIPT=%~dp0Gongmyung_Library\Code_AI\Gongmyung_Daemon.py
python "%DAEMON_SCRIPT%"
pause