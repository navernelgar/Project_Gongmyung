@echo off
chcp 65001
echo [Gongmyung] Installing dependencies for System Tray Icon...
echo.

:: 파이썬 경로 확인
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [Error] Python not found. Please install Python first.
    pause
    exit /b
)

:: 필수 라이브러리 설치
echo Installing pystray and pillow...
pip install pystray pillow

if %errorlevel% neq 0 (
    echo.
    echo [Error] Failed to install dependencies.
    echo Please check your internet connection.
    pause
    exit /b
)

echo.
echo [Success] Dependencies installed.
echo Now you can see the Gongmyung Icon in your system tray!
echo.
pause