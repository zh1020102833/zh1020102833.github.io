@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   硬件工程师技术笔记 - 一键部署
echo ========================================
echo.

echo [1/3] 扫描文章，更新索引...
python scripts/scan-articles.py
if %errorlevel% neq 0 (
    echo 扫描失败，请检查文章格式
    pause
    exit /b
)
echo 扫描完成

echo.
echo [2/3] 提交到 Git...
set /p msg="输入更新说明（直接回车用默认）: "
if "%msg%"=="" set msg=新增/更新文章

git add -A
git commit -m "%msg%"

echo.
echo [3/3] 推送到 GitHub...
git push

echo.
echo ========================================
echo   部署完成！等 1 分钟后刷新网页
echo   https://zh1020102833.github.io
echo ========================================
pause