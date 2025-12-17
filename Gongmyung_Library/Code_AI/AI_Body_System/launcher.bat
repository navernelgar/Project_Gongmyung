@echo off
title Gongmyung AI Body System
:: 콘솔 창 크기 및 색상 설정 (선택 사항)
mode con: cols=100 lines=30
color 0A

echo ========================================================
echo        Gongmyung AI Body System Launcher
echo ========================================================
echo.
echo [System] Initializing...
echo [System] Target: D:\Project_Gongmyung\Gongmyung_Library\Code_AI\AI_Body_System\main.py
echo.

:: 프로젝트 디렉토리로 이동
cd /d "D:\Project_Gongmyung\Gongmyung_Library\Code_AI\AI_Body_System"

:: Python 스크립트 실행
python main.py

:: 종료 시 대기 (에러 확인용)
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [Error] System crashed or stopped unexpectedly.
    pause
)
