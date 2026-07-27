#!/usr/bin/env python3
"""
convert.py — 语雀 MD → 技术文档风格 HTML 一键转换工具

用法:
    python scripts/convert.py --dir <md_source_dir>
    python scripts/convert.py --file <single_md_path>

输出: articles/<slug>.html（明文源文件，供 scan-articles.py 扫描）
图片: 外部 CDN 图片自动下载到 image/ 目录
"""

import os
import re
import sys
import argparse
import urllib.request
import hashlib
from pathlib import Path
from datetime import datetime

# ─── 路径配置 ───────────────────────────────────────────

PROJECT_ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARTICLES_DIR = PROJECT_ROOT / "articles"
IMAGE_DIR = PROJECT_ROOT / "image"

# ─── CSS 内联（来自风格规范 v2.0） ──────────────────────

CSS = r"""
    :root {
      --bg:           #f5f4f1;
      --surface:      #ffffff;
      --border:       rgba(0,0,0,0.08);
      --border-med:   rgba(0,0,0,0.15);
      --canvas-bg:    #ececec;
      --code-bg:      #f0f0f0;
      --text:         #1c1b19;
      --text-sec:     #555350;
      --text-hint:    #8c8883;
      --accent:       #16599e;
      --accent-light: #e3eef9;
      --teal:         #0d6751;
      --teal-light:   #dff3ec;
      --coral:        #913719;
      --coral-light:  #f9e9e2;
      --amber:        #7d4908;
      --amber-light:  #f9ecd6;
      --purple:       #4e44b0;
      --purple-light: #eceafc;
      --green:        #36650f;
      --green-light:  #e9f2db;
      --sidebar-w:       260px;
      --sidebar-bg:      #111827;
      --sidebar-text:    #9ca3af;
      --sidebar-active:  #2dd4bf;
      --sidebar-hover:   #1f2937;
      --sidebar-heading: #6b7280;
      --radius:    8px;
      --radius-lg: 12px;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.75;
      font-size: 14px;
    }
    .sidebar {
      position: fixed; left: 0; top: 0;
      width: var(--sidebar-w); height: 100vh;
      background: var(--sidebar-bg);
      overflow-y: auto; z-index: 100;
      padding: 28px 0 40px;
    }
    .sidebar-title {
      padding: 0 24px 16px;
      font-size: 13px; font-weight: 500;
      color: var(--sidebar-heading);
      letter-spacing: 0.06em; text-transform: uppercase;
    }
    .sidebar-nav { list-style: none; }
    .sidebar-nav a {
      display: block; padding: 7px 24px;
      font-size: 13px; color: var(--sidebar-text);
      text-decoration: none;
      transition: color 0.15s, background 0.15s;
      border-left: 3px solid transparent;
      line-height: 1.5;
    }
    .sidebar-nav a:hover { color: #e5e7eb; background: var(--sidebar-hover); }
    .sidebar-nav a.active { color: var(--sidebar-active); border-left-color: var(--sidebar-active); background: rgba(45,212,191,0.06); }
    .sidebar-nav .sub a { padding-left: 44px; font-size: 12px; color: #6b7280; }
    .sidebar-home {
      display: block; padding: 8px 24px; margin-top: 24px;
      font-size: 13px; color: var(--sidebar-text);
      text-decoration: none;
      transition: color 0.15s, background 0.15s;
      border-top: 1px solid rgba(255,255,255,0.08);
    }
    .sidebar-home:hover { color: var(--sidebar-active); background: var(--sidebar-hover); }
    .sidebar { scrollbar-width: thin; scrollbar-color: #374151 transparent; }
    .sidebar::-webkit-scrollbar { width: 4px; }
    .sidebar::-webkit-scrollbar-track { background: transparent; }
    .sidebar::-webkit-scrollbar-thumb { background: #374151; border-radius: 2px; }
    .main-wrap { margin-left: var(--sidebar-w); flex: 1; min-width: 0; }
    .page-header { padding: 48px 28px 40px; text-align: center; }
    .page-header h1 { font-size: 24px; font-weight: 500; margin-bottom: 12px; }
    .page-header p { font-size: 13px; color: var(--text-hint); }
    .content { max-width: 900px; margin: 0 auto; padding: 0 28px 80px; }
    .chapter {
      background: var(--surface);
      border: 0.5px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 36px 40px;
      margin-bottom: 28px;
      scroll-margin-top: 24px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .chapter-num {
      font-size: 11px; font-weight: 500;
      color: var(--text-hint);
      letter-spacing: 0.1em; text-transform: uppercase;
      margin-bottom: 6px;
    }
    .chapter-title {
      font-size: 19px; font-weight: 500;
      margin-bottom: 14px;
      padding-bottom: 14px;
      border-bottom: 0.5px solid var(--border);
    }
    h3 { font-size: 15px; font-weight: 500; margin: 24px 0 12px; }
    h4 { font-size: 14px; font-weight: 500; color: var(--text-sec); margin: 18px 0 10px; }
    p { margin-bottom: 12px; }
    ul, ol { margin-bottom: 14px; padding-left: 28px; }
    li { margin: 6px 0; }
    table {
      width: 100%; border-collapse: separate; border-spacing: 0;
      margin: 16px 0; font-size: 13px;
      border: 0.5px solid var(--border);
      border-radius: var(--radius); overflow: hidden;
    }
    thead th {
      background: #f0f0f0;
      font-weight: 500; padding: 10px 14px;
      text-align: left; font-size: 12px;
      border-bottom: 0.5px solid var(--border);
    }
    tbody td { padding: 9px 14px; border-bottom: 0.5px solid var(--border); vertical-align: top; }
    tbody tr:nth-child(even) { background: #fafafa; }
    tbody tr:last-child td { border-bottom: none; }
    .info-box { border-radius: 0 6px 6px 0; padding: 12px 16px; margin: 14px 0; font-size: 13px; }
    .info-box         { background: var(--accent-light); border-left: 3px solid var(--accent); color: var(--accent); }
    .info-box.teal    { background: var(--teal-light);   border-left: 3px solid var(--teal);   color: var(--teal); }
    .info-box.coral   { background: var(--coral-light);  border-left: 3px solid var(--coral);  color: var(--coral); }
    .info-box.warn    { background: #fff5eb;             border-left: 3px solid #e07b30;       color: #8b4a0e; }
    .info-box.purple  { background: var(--purple-light); border-left: 3px solid var(--purple); color: var(--purple); }
    .info-box.green   { background: var(--green-light);  border-left: 3px solid var(--green);  color: var(--green); }
    code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-family: "SF Mono", "Fira Code", "Consolas", monospace; font-size: 12px; }
    pre { background: #f0f0f0; border-radius: var(--radius); padding: 14px 18px; overflow-x: auto; margin: 14px 0; font-size: 12px; line-height: 1.6; }
    pre code { background: none; padding: 0; }
    .flow-box {
      background: #f8f7f5;
      border: 0.5px solid var(--border);
      border-radius: var(--radius);
      padding: 20px 24px;
      margin: 16px 0;
      font-family: "SF Mono", "Fira Code", "Consolas", monospace;
      font-size: 13px; line-height: 1.8; white-space: pre-line;
    }
    .flow-box .arrow { color: var(--teal); font-weight: 500; }
    .tag { display: inline-block; border-radius: 4px; font-size: 11px; font-weight: 500; padding: 2px 8px; margin-right: 4px; }
    .tag         { background: var(--accent-light); color: var(--accent); }
    .tag.teal    { background: var(--teal-light);   color: var(--teal); }
    .tag.coral   { background: var(--coral-light);  color: var(--coral); }
    .tag.amber   { background: var(--amber-light);  color: var(--amber); }
    .tag.purple  { background: var(--purple-light); color: var(--purple); }
    .tag.green   { background: var(--green-light);  color: var(--green); }
    blockquote { border-left: 3px solid var(--border-med); padding: 8px 16px; margin: 14px 0; color: var(--text-sec); font-size: 13px; background: #fafaf8; border-radius: 0 6px 6px 0; }
    @media (max-width: 768px) {
      .sidebar { display: none; }
      .main-wrap { margin-left: 0; }
      .content { padding: 20px 16px 60px; }
      .chapter { padding: 24px 20px; }
    }
"""

# ─── 中文数字映射 ────────────────────────────────────────

CN_NUMS = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
           "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十"]

def cn_num(n):
    """1 → 一, 2 → 二, ..."""
    if 1 <= n <= len(CN_NUMS):
        return CN_NUMS[n - 1]
    return str(n)

# ─── YAML 头部解析 ───────────────────────────────────────

def parse_front_matter(text):
    """解析 MD 文件头部的 YAML front matter，返回 (meta_dict, body_text)。"""
    meta = {}
    body = text
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    if m:
        yaml_str = m.group(1)
        body = text[m.end():]
        for line in yaml_str.strip().split('\n'):
            line = line.strip()
            if ':' in line:
                key, _, val = line.partition(':')
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if val:
                    meta[key] = val
    return meta, body

# ─── 图片下载 ────────────────────────────────────────────

def download_image(url, article_slug, image_counter):
    """下载外部图片到 image/ 目录，返回本地相对路径。"""
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    # 从 URL 猜测扩展名
    parsed = urllib.parse.urlparse(url)
    ext = os.path.splitext(parsed.path)[1].lower()
    if ext not in ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'):
        ext = '.jpg'

    # 命名: 文章slug_N.ext
    local_name = f"{article_slug}_{image_counter:02d}{ext}"
    local_path = IMAGE_DIR / local_name

    if not local_path.exists():
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            with open(local_path, 'wb') as f:
                f.write(data)
            print(f"  [下载] {url} → {local_name}")
        except Exception as e:
            print(f"  [警告] 下载失败 {url}: {e}")
            return url  # 保留原始 URL

    return f"../image/{local_name}"

# ─── Markdown 正文转换 ───────────────────────────────────

INFO_BOX_KEYWORDS = {
    "关键认知": "teal",
    "类比理解": "teal",
    "核心结论": "teal",
    "关键问题": "coral",
    "常见错误": "coral",
    "致命陷阱": "coral",
    "注意": "warn",
    "经验": "warn",
    "调试建议": "warn",
    "延伸": "purple",
    "超纲": "purple",
    "进阶": "purple",
    "建议": "green",
    "技巧": "green",
    "推荐": "green",
}

def detect_info_box(line):
    """检测 > **关键词**：格式，返回 (box_class, label, content) 或 None。"""
    # 匹配: > **关键词**：正文
    m = re.match(r'^>\s*\*\*(.+?)\*\*\s*[：:]\s*(.*)', line)
    if m:
        keyword = m.group(1).strip()
        content = m.group(2).strip()
        for kw, cls in INFO_BOX_KEYWORDS.items():
            if kw in keyword:
                return cls, keyword, content
        # 默认蓝色
        return "", keyword, content
    return None

def convert_body(body, article_slug):
    """
    将 MD 正文转为 HTML 片段。
    返回 (sidebar_entries, html_body_contents, image_counter)
    sidebar_entries: [(label, anchor, is_sub), ...]
    """
    lines = body.split('\n')
    output = []
    sidebar = []
    chapter_idx = 0
    in_code_block = False
    code_buf = []
    in_table = False
    table_buf = []
    in_list = False
    list_buf = []
    list_ordered = False
    image_counter = [0]
    chapter_open = False   # 当前是否有未闭合的 chapter section

    def close_chapter():
        nonlocal chapter_open
        if chapter_open:
            output.append('</section>')
            chapter_open = False

    def flush_paragraph(buf):
        text = ' '.join(buf).strip()
        if text:
            output.append(f"<p>{text}</p>")
        buf.clear()

    def flush_code_block():
        code_text = '\n'.join(code_buf)
        code_text = code_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        output.append(f"<pre><code>{code_text}</code></pre>")
        code_buf.clear()

    def flush_table():
        nonlocal in_table
        if not table_buf:
            return
        has_sep = len(table_buf) > 1 and re.match(r'^\|[\s\-:|]+\|', table_buf[1])
        header_row = table_buf[0]
        data_start = 2 if has_sep else 1
        headers = [c.strip() for c in header_row.strip('|').split('|')]
        output.append("<table>")
        output.append("<thead><tr>")
        for h in headers:
            output.append(f"<th>{h}</th>")
        output.append("</tr></thead>")
        output.append("<tbody>")
        for row in table_buf[data_start:]:
            cells = [c.strip() for c in row.strip('|').split('|')]
            output.append("<tr>")
            for c in cells:
                output.append(f"<td>{c}</td>")
            output.append("</tr>")
        output.append("</tbody></table>")
        table_buf.clear()
        in_table = False

    def flush_list():
        nonlocal in_list
        if not list_buf:
            return
        tag = "ol" if list_ordered else "ul"
        output.append(f"<{tag}>")
        for item in list_buf:
            output.append(f"<li>{item}</li>")
        output.append(f"</{tag}>")
        list_buf.clear()
        in_list = False

    def strip_chapter_prefix(title_text):
        """去除章节标题中已有的 '第X章' 前缀，返回纯标题。"""
        m = re.match(r'^第[一二三四五六七八九十百千\d]+章\s*[.、]?\s*', title_text)
        if m:
            return title_text[m.end():].strip()
        return title_text

    para_buf = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # 代码块边界
        if line.strip().startswith('```'):
            flush_paragraph(para_buf)
            flush_table()
            flush_list()
            if in_code_block:
                flush_code_block()
                in_code_block = False
            else:
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            code_buf.append(line)
            i += 1
            continue

        # 表格检测
        if line.strip().startswith('|') and line.strip().endswith('|'):
            flush_paragraph(para_buf)
            flush_list()
            in_table = True
            table_buf.append(line)
            i += 1
            continue

        if in_table:
            if line.strip() == '' or not (line.strip().startswith('|')):
                flush_table()
            else:
                table_buf.append(line)
                i += 1
                continue

        # 空行
        if line.strip() == '':
            flush_paragraph(para_buf)
            flush_table()
            flush_list()
            i += 1
            continue

        # H1 跳过（YAML 头部已处理 title）
        if line.startswith('# ') and chapter_idx == 0:
            flush_paragraph(para_buf)
            flush_table()
            flush_list()
            i += 1
            continue

        # H2: 章节标题
        if line.startswith('## '):
            close_chapter()
            flush_paragraph(para_buf)
            flush_table()
            flush_list()
            chapter_idx += 1
            raw_title = line[3:].strip()
            pure_title = strip_chapter_prefix(raw_title)
            ch_num = cn_num(chapter_idx)
            anchor = f"ch{chapter_idx}"
            sidebar.append((f"第{ch_num}章 {pure_title}", anchor, False))
            output.append(f'<section class="chapter" id="{anchor}">')
            output.append(f'<div class="chapter-num">第{ch_num}章</div>')
            output.append(f'<h2 class="chapter-title">{pure_title}</h2>')
            chapter_open = True
            i += 1
            continue

        # H3: 小节
        if line.startswith('### '):
            flush_paragraph(para_buf)
            flush_table()
            flush_list()
            title_text = line[4:].strip()
            m_sub = re.match(r'^(\d+)\.(\d+)\s+(.*)', title_text)
            if m_sub:
                ch, sec, rest = m_sub.groups()
                anchor = f"ch{ch}-s{sec}"
                label = f"{ch}.{sec} {rest}"
            else:
                anchor = f"sec-{chapter_idx}-{len([s for s in sidebar if not s[2]])}"
                label = title_text
            sidebar.append((label, anchor, True))
            output.append(f'<h3 id="{anchor}">{title_text}</h3>')
            i += 1
            continue

        # H4: 子小节
        if line.startswith('#### '):
            flush_paragraph(para_buf)
            flush_table()
            flush_list()
            title_text = line[5:].strip()
            m_subsub = re.match(r'^(\d+)\.(\d+)\.(\d+)\s+(.*)', title_text)
            if m_subsub:
                ch, sec, sub, rest = m_subsub.groups()
                anchor = f"ch{ch}-s{sec}-s{sub}"
            else:
                anchor = f"sub-{chapter_idx}-{len([s for s in sidebar if s[2]])}"
            sidebar.append((title_text, anchor, True))
            output.append(f'<h4 id="{anchor}">{title_text}</h4>')
            i += 1
            continue

        # 引用块 → info-box 或 blockquote
        if line.startswith('> '):
            flush_paragraph(para_buf)
            flush_table()
            flush_list()
            box = detect_info_box(line)
            if box:
                cls, keyword, content = box
                cls_suffix = f" {cls}" if cls else ""
                output.append(f'<div class="info-box{cls_suffix}"><strong>{keyword}</strong>：{content}</div>')
            else:
                quote_lines = [line[2:].strip()]
                j = i + 1
                while j < len(lines) and lines[j].startswith('> '):
                    quote_lines.append(lines[j][2:].strip())
                    j += 1
                i = j - 1
                output.append(f"<blockquote>{'<br>'.join(quote_lines)}</blockquote>")
            i += 1
            continue

        # 无序列表项: - item 或 * item
        list_match = re.match(r'^(\s*)([-*])\s+(.*)', line)
        if list_match:
            flush_paragraph(para_buf)
            flush_table()
            indent, marker, item_text = list_match.groups()
            if not in_list:
                in_list = True
                list_ordered = False
            list_buf.append(item_text)
            i += 1
            continue

        # 有序列表项: 1. item
        ol_match = re.match(r'^(\s*)(\d+)\.\s+(.*)', line)
        if ol_match:
            flush_paragraph(para_buf)
            flush_table()
            _, _, item_text = ol_match.groups()
            if not in_list:
                in_list = True
                list_ordered = True
            list_buf.append(item_text)
            i += 1
            continue

        # 图片
        img_m = re.match(r'!\[.*?\]\((.+?)\)', line.strip())
        if img_m:
            flush_paragraph(para_buf)
            flush_table()
            flush_list()
            src = img_m.group(1).strip()
            if src.startswith('http://') or src.startswith('https://'):
                image_counter[0] += 1
                src = download_image(src, article_slug, image_counter[0])
            output.append(f'<p><img src="{src}" alt="" style="max-width:100%"></p>')
            i += 1
            continue

        # 普通段落
        para_buf.append(line)
        i += 1

    # 收尾
    flush_paragraph(para_buf)
    flush_table()
    flush_list()
    if in_code_block:
        flush_code_block()
    close_chapter()

    return sidebar, output, image_counter[0]

# ─── 行内格式处理 ────────────────────────────────────────

def apply_inline_formatting(text):
    """对文本应用行内格式：**粗体**, `代码`, $math$"""
    # `代码`
    text = re.sub(r'`([^`]+?)`', r'<code>\1</code>', text)
    # **粗体**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # 行内公式 $...$ 保留
    return text

# ─── HTML 页面生成 ────────────────────────────────────────

def build_html(meta, sidebar_entries, body_html, image_counter):
    """构建完整的 HTML 页面。"""
    title = meta.get('title', '未命名')
    category = meta.get('category', '随笔')
    date_str = meta.get('date', datetime.now().strftime('%Y-%m-%d'))
    description = meta.get('description', '')

    # 侧边栏 HTML
    sidebar_html = []
    for label, anchor, is_sub in sidebar_entries:
        if is_sub:
            sidebar_html.append(f'      <li class="sub"><a href="#{anchor}">{label}</a></li>')
        else:
            sidebar_html.append(f'      <li><a href="#{anchor}">{label}</a></li>')

    sidebar_str = '\n'.join(sidebar_html)

    # 正文 HTML 应用内联格式
    formatted_body = []
    for line in body_html:
        # 跳过已经处理过的结构标签（section, table, pre, div 等）
        if line.startswith('<section') or line.startswith('<table') or \
           line.startswith('<pre') or line.startswith('<div') or \
           line.startswith('<blockquote') or line.startswith('<img'):
            formatted_body.append(line)
        elif line.startswith('<h3') or line.startswith('<h4'):
            # 标题中的内联格式
            formatted_body.append(apply_inline_formatting(line))
        elif line.startswith('<p>'):
            formatted_body.append(apply_inline_formatting(line))
        elif line.startswith('<li') or line.startswith('<td') or line.startswith('<th'):
            formatted_body.append(apply_inline_formatting(line))
        elif line.startswith('</section>') or line.startswith('</table>') or \
             line.startswith('</blockquote>') or line.startswith('</thead>') or \
             line.startswith('</tbody>'):
            formatted_body.append(line)
        else:
            formatted_body.append(line)

    body_str = '\n'.join(formatted_body)

    # 类别标签验证
    valid_categories = ["硬件", "嵌入式", "FPGA", "高速信号", "EMC", "控制理论", "电机", "EDA", "随笔"]
    if category not in valid_categories:
        print(f"  [警告] 未知分类 '{category}'，已设为 '随笔'")
        category = "随笔"

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="category" content="{category}">
  <meta name="date" content="{date_str}">
  <meta name="description" content="{description}">
  <meta name="encrypt" content="true">
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\(', '\\)']],
        displayMath: [['$$', '$$']]
      }}
    }};
  </script>
  <script id="MathJax-script" async
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
  </script>
  <style>{CSS}</style>
</head>
<body>
  <nav class="sidebar">
    <div class="sidebar-title">目录</div>
    <ul class="sidebar-nav">
{sidebar_str}
    </ul>
    <a class="sidebar-home" href="../index.html">← 返回首页</a>
  </nav>

  <div class="main-wrap">
    <header class="page-header">
      <h1>{title}</h1>
      <p>{category} · {date_str}</p>
    </header>

    <div class="content">
{body_str}
    </div>
  </div>
</body>
</html>"""

# ─── 主流程 ───────────────────────────────────────────────

def convert_file(md_path):
    """转换单个 MD 文件。返回 (success, slug)。"""
    print(f"\n处理: {md_path}")

    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    meta, body = parse_front_matter(text)

    slug = os.path.splitext(os.path.basename(md_path))[0]
    # 清理 slug：移除特殊字符，保留字母数字和连字符
    slug = re.sub(r'[^\w\-]', '-', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')

    sidebar, body_html, img_count = convert_body(body, slug)

    html = build_html(meta, sidebar, body_html, img_count)

    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = ARTICLES_DIR / f"{slug}.html"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  → {out_path}")
    print(f"  [{meta.get('category', '随笔')}] {meta.get('title', slug)}"
          f" | {meta.get('date', '?')} | 章节: {len([s for s in sidebar if not s[2]])}")
    return True, slug

def main():
    global ARTICLES_DIR, IMAGE_DIR

    parser = argparse.ArgumentParser(description="语雀 MD → 技术文档风格 HTML 转换器")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--dir', help='MD 源文件目录（批量转换目录下所有 .md）')
    group.add_argument('--file', help='单个 MD 文件路径')
    parser.add_argument('--output', default=str(ARTICLES_DIR), help='HTML 输出目录')
    parser.add_argument('--images', default=str(IMAGE_DIR), help='图片存放目录')
    args = parser.parse_args()

    ARTICLES_DIR = Path(args.output)
    IMAGE_DIR = Path(args.images)

    md_files = []
    if args.file:
        if not os.path.isfile(args.file):
            print(f"错误: 文件不存在 {args.file}")
            sys.exit(1)
        md_files = [os.path.abspath(args.file)]
    else:
        src_dir = Path(args.dir)
        if not src_dir.is_dir():
            print(f"错误: 目录不存在 {src_dir}")
            sys.exit(1)
        md_files = sorted([str(p) for p in src_dir.glob("*.md")])
        if not md_files:
            print(f"目录中未找到 .md 文件: {src_dir}")
            sys.exit(1)

    print("=" * 60)
    print("  MD → HTML 转换器")
    print("=" * 60)

    ok = 0
    fail = 0
    for f in md_files:
        try:
            success, _ = convert_file(f)
            if success:
                ok += 1
            else:
                fail += 1
        except Exception as e:
            print(f"  错误: {e}")
            fail += 1

    print(f"\n{'=' * 60}")
    print(f"  完成: {ok} 成功, {fail} 失败")
    print(f"{'=' * 60}")

    if fail > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
