@echo off
chcp 65001
title Gongmyung Auto Register
echo [Gongmyung] Registering Daemon to Startup (Auto Mode)...
echo This will make Gongmyung run automatically when Windows starts.
echo.

:: 파이썬 경로 확인
set PYTHON_EXE=python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [Error] Python not found. Please install Python first.
    pause
    exit /b
)

:: 데몬 스크립트 경로
set DAEMON_SCRIPT=%~dp0Gongmyung_Library\Code_AI\Gongmyung_Daemon.py

:: 시작프로그램 폴더에 바로가기 생성 (VBScript 활용)
set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set SHORTCUT_PATH=%STARTUP_DIR%\Gongmyung_Daemon.lnk

echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%SHORTCUT_PATH%" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%PYTHON_EXE%" >> CreateShortcut.vbs
echo oLink.Arguments = """%DAEMON_SCRIPT%""" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%~dp0" >> CreateShortcut.vbs
echo oLink.Description = "Gongmyung System Resonance Daemon" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

cscript /nologo CreateShortcut.vbs
del CreateShortcut.vbs

echo.
echo [Success] Gongmyung Daemon has been registered to Startup.
echo.
pause