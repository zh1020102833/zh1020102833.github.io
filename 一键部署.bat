@echo off
cd /d "%~dp0"

echo ========================================
echo   Hardware Tech Notes - One-click Deploy
echo ========================================
echo.

echo [1/3] Scanning articles, updating index...
python scripts/scan-articles.py
if %errorlevel% neq 0 (
    echo Scan failed, check article format
    pause
    exit /b
)
echo Scan complete

echo.
echo [2/3] Committing to Git...
set /p msg="Enter commit message (Enter for default): "
if "%msg%"=="" set msg=add/update article

git add -A
git commit -m "%msg%"

echo.
echo [3/3] Pushing to GitHub...
git push

echo.
echo ========================================
echo   Done! Wait 1 min then refresh
echo   https://zh1020102833.github.io
echo ========================================
pause