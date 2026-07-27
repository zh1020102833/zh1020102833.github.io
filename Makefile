# ============================================================
#  article-site 自动化构建 Makefile
#  用法:
#    make DIR=子目录名    → 一键：转换 → 扫描 → push
#    make convert DIR=xx  → 仅转换 MD
#    make scan            → 仅扫描生成 article-data.js
#    make push            → 仅 git commit + push
#
#  前提: 需要 Git for Windows 自带的 mingw32-make 或 GNU make
# ============================================================

# ── 路径配置（按你的实际路径修改） ────────────────────────
PROJECT_DIR  := C:/Users/ahs/Desktop/Project/article-site
SCRIPTS_DIR  := $(PROJECT_DIR)/scripts
ARTICLES_DIR := $(PROJECT_DIR)/articles
IMAGE_DIR    := $(PROJECT_DIR)/image
DRAFTS_BASE  := C:/Users/ahs/.qclaw/workspace/yuque_export

# ── 默认目标 ──────────────────────────────────────────────
.PHONY: all convert scan push clean status help

all: convert scan push
	@echo.
	@echo 全流程完成！

# ── 步骤 1: MD → HTML ─────────────────────────────────────
convert:
ifeq ($(DIR),)
	@echo 错误: 请指定 DIR 参数，例如 make DIR=dac
	@exit 1
endif
	@echo [1/3] 转换 MD → HTML...
	python $(SCRIPTS_DIR)/convert.py --dir "$(DRAFTS_BASE)/$(DIR)" --output "$(ARTICLES_DIR)" --images "$(IMAGE_DIR)"

# ── 步骤 2: 扫描生成 article-data.js ─────────────────────
scan:
	@echo [2/3] 扫描文章，生成 article-data.js...
	cd /d $(PROJECT_DIR) && python scripts/scan-articles.py

# ── 步骤 3: git push ──────────────────────────────────────
push:
	@echo [3/3] 提交并推送...
	cd /d $(PROJECT_DIR) && git add -A && git commit -m "update site" && git push origin main

# ── 辅助 ──────────────────────────────────────────────────
clean:
	@echo 清理临时文件...

status:
	cd /d $(PROJECT_DIR) && git status

help:
	@echo.
	@echo  article-site Makefile 用法:
	@echo  ============================================
	@echo  make DIR=子目录名    一键全流程（推荐）
	@echo  make convert DIR=xx  仅 MD → HTML
	@echo  make scan            仅扫描更新索引
	@echo  make push            仅 git push
	@echo  make status          查看 git 状态
	@echo.
	@echo  示例:
	@echo  make DIR=dac          转换 yuque_export/dac/ 下所有 MD
	@echo  make convert DIR=amp  仅转换 amp 目录
	@echo.
