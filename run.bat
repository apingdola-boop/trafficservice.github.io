@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo Starting Flask App...
echo Open http://localhost:5000 in your browser
python app.py
pause






