#!/bin/bash
# ============================================================
# upload.sh - 整站批量上传脚本 (macOS / Linux)
#
# 前置条件：
#   1. 已安装 ossutil (https://help.aliyun.com/zh/oss/developer-reference/install-ossutil)
#   2. 已配置 AccessKey (ossutil config)
#
# 使用方法：
#   chmod +x upload.sh   # 首次赋予执行权限
#   ./upload.sh          # 执行上传
#
# 说明：
#   - 递归上传本地 article-site/ 下所有文件至 OSS Bucket 根目录
#   - --update 参数：仅当本地文件比线上新时覆盖，节省时间
#   - --delete 参数：删除 OSS 上存在但本地已不存在的文件（可选，当前注释掉）
# ============================================================

# ---- 配置区：按需修改 ----
BUCKET_NAME="your-bucket-name"
OSS_ENDPOINT="oss-cn-hangzhou.aliyuncs.com"
LOCAL_DIR="../"

# ---- 上传命令 ----
# 如需启用"删除线上多余文件"功能，取消下面 --delete 的注释
# 注意：--delete 会删除 OSS 上有但本地没有的文件，首次使用请先不加 --delete 运行一次

ossutil cp \
  "$LOCAL_DIR" \
  "oss://$BUCKET_NAME/" \
  --recursive \
  --update \
  --endpoint "$OSS_ENDPOINT" \
  --exclude ".gitkeep" \
  --exclude "upload-tools/*"

# --delete \   # 如需清理线上多余文件，取消本行和上行注释

# ---- 完成提示 ----
if [ $? -eq 0 ]; then
  echo ""
  echo "上传完成！"
  echo "OSS 地址: http://$BUCKET_NAME.$OSS_ENDPOINT"
  echo "CDN 地址: https://your-domain.com (需自行配置)"
else
  echo ""
  echo "上传失败，请检查配置和网络连接。"
  exit 1
fi
