# 纯静态个人文章网站 - 完整方案

> 基于 HTML/CSS/JS 构建，部署到阿里云 OSS + CDN

---

## 目录

- [一、整体架构方案](#一整体架构方案)
- [二、开发指南（代码操作）](#二开发指南代码操作)
- [三、上传部署（终端操作）](#三上传部署终端操作)
- [四、OSS + CDN 配置（云平台操作）](#四oss--cdn-配置云平台操作)
- [五、维护与拓展](#五维护与拓展)
- [六、常见问题排查](#六常见问题排查)

---

## 一、整体架构方案

### 1.1 技术选型

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | HTML5 + CSS3 + JavaScript | 纯静态，无框架依赖 |
| 存储 | 阿里云 OSS | 文件存储 + 静态网站托管 |
| 加速 | 阿里云 CDN | 自定义域名 + HTTPS |
| 上传 | ossutil 命令行工具 | 批量递归上传 |

### 1.2 目录结构

```
article-site/
├── index.html                     # 首页：文章导航列表（带分类筛选）
│
├── articles/                      # 文章页面（每篇文章一个 .html 文件）
│   ├── hello-world.html           #   示例文章 1
│   ├── web-dev-basics.html        #   示例文章 2
│   ├── writing-tips.html          #   示例文章 3
│   └── ...                        #   [新增文章在此创建]
│
├── pages/                         # 其他静态页面
│   ├── about.html                 #   关于页面
│   └── archive.html               #   归档页面（自动读取文章数据）
│
├── assets/                        # 静态资源
│   ├── css/
│   │   └── style.css              #   全局样式表
│   ├── js/
│   │   ├── nav.js                 #   导航栏组件（所有页面自动加载）
│   │   ├── article-data.js        #   [核心] 文章数据配置（新增文章需更新此文件）
│   │   └── main.js                #   首页文章列表渲染逻辑
│   └── images/                    #   图片资源
│
├── upload-tools/                  # 上传工具
│   ├── upload.sh                  #   macOS/Linux 上传脚本
│   ├── upload.bat                 #   Windows 上传脚本
│   └── README.md                  #   上传工具安装配置说明
│
├── _docs/                         # 附加文档
│   └── ...                        #   按需存放
│
├── .gitignore
└── README.md                      # 本文件（全站说明文档）
```

### 1.3 文件命名规则

| 类型 | 规则 | 示例 |
|------|------|------|
| 文章文件 | 英文小写 + 连字符，含义清晰 | `hello-world.html` |
| 分类标签 | 中文或英文，保持统一 | `技术`、`随笔` |
| 图片资源 | 类型前缀 + 描述 | `screenshot-homepage.png` |
| CSS/JS | 功能命名 | `nav.js`、`style.css` |

### 1.4 路径编写规范

- **文章内链**：使用相对路径，从当前文件到目标文件
  - 文章 → 首页：`../index.html`
  - 首页 → 文章：`articles/hello-world.html`
- **资源引用**：使用相对路径
  - `assets/css/style.css`
  - `assets/js/nav.js`
- **导航栏链接**：使用根目录相对路径（以 `/` 开头）
  - `/index.html`
  - `/pages/about.html`

### 1.5 需规避的问题

1. 不要使用绝对路径（如 `C:\` 或 `file://`）
2. 不要在 URL 中使用中文或空格
3. 不要在 Git 中提交 AccessKey 等敏感信息
4. 所有文件使用 UTF-8 编码（无 BOM）
5. 确保 HTML 标签正确闭合

---

## 二、开发指南（本地代码操作）

### 2.1 新增一篇文章（3 步完成）

**第 1 步**：在 `articles/` 目录创建 HTML 文件

复制以下模板，保存为 `articles/your-article-name.html`：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- [修改] 文章标题 -->
  <title>你的文章标题</title>
  <!-- [修改] 页面描述，用于 SEO -->
  <meta name="description" content="文章简短描述">
  <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>

  <!-- 导航栏由 nav.js 自动生成 -->

  <div class="main-wrapper">
    <a href="../index.html" class="back-link">&larr; 返回首页</a>

    <article class="article-detail">
      <header class="article-header">
        <!-- [修改] 文章标题 -->
        <h1>你的文章标题</h1>
        <div class="meta">
          <!-- [修改] 分类和时间 -->
          <span>分类：技术</span> &middot;
          <span>2026-05-22</span>
        </div>
      </header>

      <div class="article-body">
        <!-- [修改] 从此处开始写文章内容 -->
        <p>文章内容...</p>

        <h2>章节标题</h2>
        <p>正文内容...</p>

        <h2>代码示例</h2>
        <pre><code>console.log('Hello World');</code></pre>

        <blockquote>引用内容</blockquote>

        <ul>
          <li>列表项 1</li>
          <li>列表项 2</li>
        </ul>
      </div>
    </article>
  </div>

  <footer class="site-footer">
    <p>&copy; 2026 我的文章</p>
  </footer>

  <script src="../assets/js/nav.js"></script>
</body>
</html>
```

**第 2 步**：更新 `assets/js/article-data.js`

在数组末尾添加新条目：

```javascript
{
  id: 'your-article-name',
  title: '你的文章标题',
  category: '分类名',
  date: '2026-05-22',
  summary: '文章简介，显示在首页卡片上',
  file: 'articles/your-article-name.html'
}
```

**第 3 步**：执行上传（见第三章）

### 2.2 修改现有页面

- **修改文章内容**：直接编辑 `articles/` 下对应的 HTML 文件
- **修改样式**：编辑 `assets/css/style.css`，修改颜色、间距等
- **修改导航菜单**：编辑 `assets/js/nav.js` 中的 `navLinks` 数组
- **修改首页标题/描述**：编辑 `index.html`

### 2.3 全局样式变量说明

在 `assets/css/style.css` 中，查找 `#4A90D9` 即可替换主题色：

| 用途 | 默认色值 | 说明 |
|------|----------|------|
| 主题色 / 链接色 | `#4A90D9` | 主导航高亮、按钮、标签 |
| 标题色 | `#1a1a2e` | 文章标题、页面标题 |
| 正文色 | `#333` | 段落文字 |
| 次要文字 | `#777` / `#999` | 日期、摘要描述 |
| 背景色 | `#f5f7fa` | 页面背景 |
| 卡片背景 | `#fff` | 文章卡片、详情页背景 |

### 2.4 本地预览

直接用浏览器打开 HTML 文件即可预览。由于浏览器安全策略，`nav.js` 通过 DOM 操作插入导航栏，本地使用 `file://` 协议时部分功能可能受限，但不影响实际部署效果。

---

## 三、上传部署（终端操作）

### 3.1 安装 ossutil

**macOS**:
```bash
brew install ossutil
```

**Linux**:
```bash
curl -o ossutil https://gosspublic.alicdn.com/ossutil/1.7.18/ossutil-linux-amd64
chmod +x ossutil
sudo mv ossutil /usr/local/bin/
```

**Windows**:
1. 下载 https://gosspublic.alicdn.com/ossutil/1.7.18/ossutil-win-amd64.zip
2. 解压，将 `ossutil.exe` 放到 `C:\ossutil\`
3. 将该目录添加到系统 PATH 环境变量
4. 打开新命令行窗口验证：`ossutil version`

### 3.2 配置 AccessKey

```bash
ossutil config
```

按提示输入（配置一次即可，后续自动复用）：
- **AccessKey ID**: 在阿里云 RAM 用户中创建
- **AccessKey Secret**: 对应的密钥
- **Endpoint**: 如 `oss-cn-hangzhou.aliyuncs.com`

> 安全提醒：建议创建 RAM 子账户，仅授权 OSS 读写权限，不要使用主账号 AccessKey。

### 3.3 修改上传脚本配置

编辑 `upload-tools/upload.sh` 或 `upload-tools/upload.bat`，修改开头的配置项：

```bash
# 修改为你的 Bucket 名称
BUCKET_NAME="your-bucket-name"

# 修改为你的 Bucket 所在地域 Endpoint
OSS_ENDPOINT="oss-cn-hangzhou.aliyuncs.com"
```

### 3.4 执行整站上传

**macOS / Linux**:
```bash
cd article-site/upload-tools
chmod +x upload.sh
./upload.sh
```

**Windows**:
```cmd
cd article-site\upload-tools
upload.bat
```

### 3.5 常用命令速查

```bash
# 上传单个文件
ossutil cp local-file.html oss://my-bucket/ --endpoint oss-cn-hangzhou.aliyuncs.com

# 上传整个目录（增量更新）
ossutil cp ./ oss://my-bucket/ --recursive --update --endpoint oss-cn-hangzhou.aliyuncs.com

# 查看线上文件
ossutil ls oss://my-bucket/ --endpoint oss-cn-hangzhou.aliyuncs.com

# 删除线上文件
ossutil rm oss://my-bucket/old-file.html --endpoint oss-cn-hangzhou.aliyuncs.com

# 删除线上文件夹（递归）
ossutil rm oss://my-bucket/old-folder/ --recursive --endpoint oss-cn-hangzhou.aliyuncs.com

# 从 OSS 下载文件
ossutil cp oss://my-bucket/file.txt ./ --endpoint oss-cn-hangzhou.aliyuncs.com
```

---

## 四、OSS + CDN 配置（云平台网页操作）

### 4.1 OSS 配置步骤

#### 4.1.1 创建 Bucket

1. 登录阿里云 OSS 控制台：https://oss.console.aliyun.com
2. 点击 **创建 Bucket**
3. 填写配置：
   - **Bucket 名称**：例如 `my-article-site`（全局唯一）
   - **地域**：选择离你最近的地域，如 `华东1（杭州）`
   - **存储类型**：标准存储
   - **读写权限**：公共读（后续通过 CDN 访问，此步也可设私有）
   - **版本控制**：关闭
4. 点击 **确定**

#### 4.1.2 配置静态网站托管

1. 进入 Bucket 详情页 → **基础设置** → **静态页面**
2. 开启 **静态网站托管**
3. 配置：
   - **默认首页**：`index.html`
   - **默认 404 页**：`index.html`（或自建 404 页面）
4. 点击 **保存**
5. 记录 OSS 访问域名，格式如：`my-article-site.oss-cn-hangzhou.aliyuncs.com`

#### 4.1.3 配置 Bucket 权限（如果未设公共读）

1. 进入 Bucket 详情页 → **权限管理** → **读写权限**
2. 将 **Bucket ACL** 设置为 **公共读**
3. 也可配置更细粒度的 **Bucket Policy**：

```json
{
  "Version": "1",
  "Statement": [{
    "Effect": "Allow",
    "Principal": ["*"],
    "Action": ["oss:GetObject"],
    "Resource": ["acs:oss:*:*:my-article-site/*"]
  }]
}
```

### 4.2 CDN 配置步骤

#### 4.2.1 添加 CDN 加速域名

1. 登录阿里云 CDN 控制台：https://cdn.console.aliyun.com
2. 点击 **添加域名**
3. 填写配置：
   - **加速域名**：你的自定义域名，如 `blog.yourdomain.com`
   - **业务类型**：图片小文件
   - **源站信息**：
     - **源站类型**：OSS 域名
     - **选择 OSS Bucket**：选择你刚创建的 Bucket
   - **端口**：默认 80/443
4. 点击 **下一步**

#### 4.2.2 HTTPS 证书配置

1. 在 CDN 域名详情页 → **HTTPS 配置**
2. 点击 **免费证书**（阿里云提供免费 DigiCert 证书）
3. 选择 **免费证书（一键配置）**，点击 **申请**
4. 等待证书签发（通常几分钟）
5. 开启 **强制跳转 HTTPS**（将 HTTP 请求自动重定向到 HTTPS）

#### 4.2.3 缓存策略配置

1. 在 CDN 域名详情页 → **缓存配置**
2. 添加缓存规则：

| 目录/文件类型 | 过期时间 | 优先级 |
|--------------|---------|-------|
| `*.html` | 1 小时 | 高 |
| `*.css` | 7 天 | 高 |
| `*.js` | 7 天 | 高 |
| `*.png` / `*.jpg` | 30 天 | 高 |
| `/`（根目录） | 遵循源站 | 低 |

> 说明：HTML 缓存时间设置较短，以便文章更新后快速生效。
> CSS/JS/图片设置较长缓存，提升加载速度。

3. 点击 **确定**

### 4.3 域名解析

#### 4.3.1 添加 CNAME 记录

1. 登录你的域名 DNS 管理控制台（如阿里云云解析、DNSPod 等）
2. 添加解析记录：

| 记录类型 | 主机记录 | 记录值 | TTL |
|---------|---------|--------|-----|
| CNAME | `blog` | CDN 分配的 CNAME 域名（如 `blog.yourdomain.com.w.kunlunsl.com`） | 10 分钟 |

> CDN 的 CNAME 域名在 CDN 控制台的域名详情页可见。

#### 4.3.2 检测解析生效

```bash
# 使用 dig 命令（macOS/Linux）
dig blog.yourdomain.com CNAME

# 使用 nslookup 命令（通用）
nslookup -type=CNAME blog.yourdomain.com

# 使用 ping 命令（Windows）
ping blog.yourdomain.com
```

如果返回的域名包含 `kunlun` 或 `aliyun` 字样，说明解析已生效。

### 4.4 部署验证

#### 方式一：OSS 原生地址验证

```
http://my-article-site.oss-cn-hangzhou.aliyuncs.com/index.html
```

预期：能看到页面正常显示（样式可能缺失，因为路径问题，属于正常现象）。

#### 方式二：CDN 域名验证

```
https://blog.yourdomain.com/index.html
```

预期：页面完整显示，浏览器地址栏显示 HTTPS 锁图标。

#### 验证检查清单

- [ ] 首页正常打开，文章列表显示
- [ ] 点击分类筛选按钮能正确过滤
- [ ] 点击文章卡片跳转到详细页面
- [ ] 导航栏菜单能正确跳转，当前页高亮
- [ ] 归档页正常显示所有文章
- [ ] 关于页面正常打开
- [ ] 浏览器地址栏显示 HTTPS 锁图标
- [ ] 移动端布局正常

---

## 五、维护与拓展

### 5.1 日常维护指南

| 操作 | 步骤 |
|------|------|
| **新增文章** | 1) 在 `articles/` 创建 HTML；2) 更新 `article-data.js`；3) 运行上传脚本 |
| **修改文章** | 1) 编辑对应 HTML 文件；2) 运行上传脚本 |
| **更新样式** | 1) 编辑 `style.css`；2) 运行上传脚本 |
| **修改导航栏菜单** | 1) 编辑 `nav.js` 中的 `navLinks` 数组；2) 运行上传脚本 |
| **删除文章** | 1) 删除 `articles/` 对应 HTML；2) 从 `article-data.js` 删除条目；3) 运行上传脚本 |
| **更换头像/图片** | 1) 放入 `assets/images/`；2) 在 HTML 中引用；3) 运行上传脚本 |

### 5.2 最简上传操作（日常更新）

```bash
# 1. 进入项目目录
cd article-site

# 2. 修改代码（新增/编辑文章）

# 3. 执行上传
cd upload-tools
./upload.sh   # Mac/Linux
# 或 upload.bat  # Windows
```

### 5.3 新增独立页面

1. 在 `pages/` 目录创建 HTML 文件（参考 `about.html`）
2. 在 `assets/js/nav.js` 的 `navLinks` 中添加菜单项：
   ```javascript
   { label: '新页面', path: '/pages/new-page.html', match: ['/pages/new-page.html'] }
   ```
3. 运行上传脚本

### 5.4 新增栏目分类

1. 写文章时在 `article-data.js` 的 `category` 字段填上新分类名
2. 首页的分类筛选按钮会自动出现该分类

### 5.5 二级导航 / 子菜单

如需二级导航，在 `nav.js` 中扩展 HTML 结构：
```javascript
// 定义一个"分类"下拉菜单项
var navHtml = '...' +
  '<li class="nav-dropdown">' +
  '<a href="#">分类</a>' +
  '<ul class="dropdown-menu">' +
  '  <li><a href="/index.html?cat=技术">技术</a></li>' +
  '  <li><a href="/index.html?cat=随笔">随笔</a></li>' +
  '</ul>' +
  '</li>';
```

然后在 `main.js` 中添加 URL 参数解析逻辑（已预留接口）。

### 5.6 优化建议

#### 性能优化

| 措施 | 说明 |
|------|------|
| 图片压缩 | 使用 TinyPNG 等工具压缩图片后再上传 |
| CSS/JS 合并 | 目前已在同一文件中，无需额外合并 |
| CDN 缓存 | 按上述缓存策略配置即可 |
| 懒加载 | 图片较多时添加 `loading="lazy"` 属性 |

#### 成本优化

| 措施 | 说明 |
|------|------|
| OSS 生命周期 | 设置自动删除 90 天前的历史版本（如果开启版本控制） |
| CDN 流量包 | 购买 CDN 流量包，比按量付费便宜 |
| OSS 存储类型 | 长期不更新的文件转为低频存储 |
| 监控报警 | 设置 OSS 账单报警，避免异常流量导致高额费用 |

---

## 六、常见问题排查

### 6.1 访问 403 Forbidden

**可能原因 1**：Bucket 权限未设置为公共读
- 解决：OSS 控制台 → Bucket → 权限管理 → 读写权限 → 公共读

**可能原因 2**：CDN 回源配置不对
- 解决：检查 CDN 源站是否指向正确的 OSS Bucket

**可能原因 3**：OSS Policy 限制
- 解决：检查 Bucket Policy 是否拒绝了特定 IP 或 Referer

### 6.2 访问 404 Not Found

**可能原因 1**：文件未上传
- 解决：运行上传脚本，确认文件已上传到 OSS

**可能原因 2**：路径错误
- 解决：检查链接中的路径大小写、文件名是否和实际一致

**可能原因 3**：静态托管未配置
- 解决：确认 OSS 静态网站托管已开启，默认首页设为 `index.html`

### 6.3 样式加载异常（页面无样式）

**可能原因 1**：CSS 路径问题
- 解决：检查 HTML 中 `<link>` 标签的 `href` 路径是否正确

**可能原因 2**：缓存问题
- 解决：在 CDN 控制台刷新缓存（CDN → 刷新预热 → 刷新 `https://blog.yourdomain.com/assets/css/style.css`）

### 6.4 HTTPS 证书相关

**可能原因**：证书未配置或已过期
- 解决：CDN 控制台 → HTTPS 配置 → 免费证书 → 申请/续签

### 6.5 域名解析未生效

**排查方法**：
```bash
# 检查 CNAME 解析
nslookup -type=CNAME blog.yourdomain.com

# 检查访问是否到达 CDN
curl -I https://blog.yourdomain.com
# 响应头中应包含 x-cache 等 CDN 相关信息
```

### 6.6 文章更新后线上未变化

**可能原因**：CDN 缓存
- 解决：
  1. CDN 控制台 → 刷新预热
  2. 刷新 `https://blog.yourdomain.com/articles/xxx.html`
  3. 或使用 **目录刷新** 刷新整个目录

---

## 附录：文件对照表

| 文件 | 作用 | 是否需要频繁修改 |
|------|------|----------------|
| `index.html` | 首页布局 | 极少 |
| `assets/css/style.css` | 全局样式 | 极少 |
| `assets/js/nav.js` | 导航栏 | 修改菜单时 |
| `assets/js/article-data.js` | 文章数据 | **每次新增/删除文章时修改** |
| `assets/js/main.js` | 首页渲染逻辑 | 极少 |
| `articles/*.html` | 文章内容 | **每次写新文章时创建** |
| `pages/about.html` | 关于页面 | 极少 |
| `upload-tools/upload.sh` | 上传脚本 | 配置一次，后续不变 |
| `upload-tools/upload.bat` | 上传脚本(Windows) | 配置一次，后续不变 |

---

> 最后更新：2026-05-22
