@echo off
chcp 65001 >nul
echo ================================
echo  一键部署到 GitHub Pages
echo ================================
echo.

cd /d "%~dp0"

REM 初始化 Git 仓库
if not exist ".git" (
  git init
)

REM 添加所有文件
git add -A

REM 提交
git commit -m "update site"

REM 设置远程仓库
git remote remove origin 2>nul
git remote add origin https://github.com/zh1020102833/zh1020102833.github.io.git

REM 推送到 GitHub
git push -f origin main

echo.
echo ================================
if %errorlevel% equ 0 (
  echo 部署成功！等待 2 分钟后访问：
  echo https://zh1020102833.github.io/
) else (
  echo 部署失败，请检查网络和权限。
  pause
  exit /b 1
)
pause
