# 上传工具使用说明

## 前置安装

### 1. 安装 ossutil

**macOS** (使用 Homebrew)：
```bash
brew install ossutil
```

**Linux**：
```bash
curl -o ossutil https://gosspublic.alicdn.com/ossutil/1.7.18/ossutil-linux-amd64
chmod +x ossutil
sudo mv ossutil /usr/local/bin/
```

**Windows**：
下载地址：https://gosspublic.alicdn.com/ossutil/1.7.18/ossutil-win-amd64.zip
解压后将 `ossutil.exe` 放到任意目录，将该目录添加到系统 PATH 环境变量。

> 最新版下载地址请参考阿里云官方文档：
> https://help.aliyun.com/zh/oss/developer-reference/install-ossutil

### 2. 配置 AccessKey

```bash
ossutil config
```

按提示输入：
- `AccessKey ID`：在阿里云 RAM 控制台创建
- `AccessKey Secret`：对应的密钥
- `Endpoint`：例如 `oss-cn-hangzhou.aliyuncs.com`（填你的 Bucket 所在地域）

> **安全提醒**：AccessKey 请妥善保管，切勿提交到 Git 仓库或公开分享。

## 使用方式

### macOS / Linux
```bash
cd upload-tools
chmod +x upload.sh
./upload.sh
```

### Windows
双击 `upload.bat` 或在命令行执行：
```cmd
cd upload-tools
upload.bat
```

## 常用 ossutil 命令

```bash
# 上传单个文件
ossutil cp local-file.txt oss://bucket-name/path/ --endpoint oss-cn-hangzhou.aliyuncs.com

# 下载单个文件
ossutil cp oss://bucket-name/path/file.txt ./local-dir/ --endpoint oss-cn-hangzhou.aliyuncs.com

# 查看文件列表
ossutil ls oss://bucket-name/ --endpoint oss-cn-hangzhou.aliyuncs.com

# 删除文件
ossutil rm oss://bucket-name/old-file.html --endpoint oss-cn-hangzhou.aliyuncs.com

# 递归删除目录
ossutil rm oss://bucket-name/old-folder/ --recursive --endpoint oss-cn-hangzhou.aliyuncs.com
```

## 安全提醒

1. 不要将 AccessKey 写在脚本中
2. 建议使用 RAM 子账户，仅授予 OSS 读写权限
3. 在 `upload.sh` / `upload.bat` 的配置区填写 Bucket 名称即可，不要写密钥
