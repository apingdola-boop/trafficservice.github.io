@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo [레거시] 네이버 Flask — NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 설정 후 실행
echo http://localhost:5000
python app.py
pause
