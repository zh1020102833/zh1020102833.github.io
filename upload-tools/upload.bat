@echo off
REM ============================================================
REM upload.bat - 整站批量上传脚本 (Windows)
REM
REM 前置条件：
REM   1. 已安装 ossutil (https://help.aliyun.com/zh/oss/developer-reference/install-ossutil)
REM   2. 已配置 AccessKey (ossutil config)
REM
REM 使用方法：
REM   双击 upload.bat 或 在命令行执行 upload.bat
REM
REM 说明：
REM   - 递归上传本地 article-site\ 下所有文件至 OSS Bucket 根目录
REM   --update 参数：仅当本地文件比线上新时覆盖
REM ============================================================

REM ---- 配置区：按需修改 ----
SET BUCKET_NAME=your-bucket-name
SET OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
SET LOCAL_DIR=..\

REM ---- 上传命令 ----
ossutil cp ^
  "%LOCAL_DIR%" ^
  "oss://%BUCKET_NAME%/" ^
  --recursive ^
  --update ^
  --endpoint "%OSS_ENDPOINT%" ^
  --exclude ".gitkeep" ^
  --exclude "upload-tools/*"

REM ---- 完成提示 ----
IF %ERRORLEVEL% EQU 0 (
  echo.
  echo 上传完成！
  echo OSS 地址: http://%BUCKET_NAME%.%OSS_ENDPOINT%
  echo CDN 地址: https://your-domain.com (需自行配置)
) ELSE (
  echo.
  echo 上传失败，请检查配置和网络连接。
  pause
  exit /b 1
)

pause
