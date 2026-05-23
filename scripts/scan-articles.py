"""
scan-articles.py — 自动扫描 articles/ 目录，生成 article-data.js 和 index.html 的静态卡片。

使用方法：
  1. 写完文章后，运行：python scripts/scan-articles.py
  2. 脚本会：
     a) 扫描 articles/ 下所有 .html（排除 template.html）
     b) 从 HTML 中提取 <title>、<meta name="description">、<meta name="category">
     c) 自动生成 article-data.js（保留手工添加的 tags 等信息）
     d) 自动更新 index.html 中的静态回退卡片
  3. 检查生成的文件后提交即可

文章 HTML 规范：
  - <title>文章标题</title>                 → article-data.js 的 title
  - <meta name="description" content="...">  → article-data.js 的 summary
  - <meta name="category" content="分类名">  → article-data.js 的 category（如不写，默认 "未分类"）
  - <meta name="date" content="2026-05-22">  → article-data.js 的 date（如不写，用文件修改时间）

注意：所有 meta 标签均为可选，缺失时会使用默认值并在输出中标注。
"""

import os
import re
import json
from datetime import datetime
from html.parser import HTMLParser

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_DIR = os.path.join(PROJECT_ROOT, "articles")
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
DATA_FILE = os.path.join(PROJECT_ROOT, "assets", "js", "article-data.js")
INDEX_FILE = os.path.join(PROJECT_ROOT, "index.html")


class ArticleMetaParser(HTMLParser):
    """从 HTML 中提取 title 和 meta 信息。"""
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = ""
        self.description = ""
        self.category = ""
        self.date = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            name = attrs_dict.get("name", "").lower()
            content = attrs_dict.get("content", "")
            if name == "description":
                self.description = content
            elif name == "category":
                self.category = content
            elif name == "date":
                self.date = content

    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()
            self.in_title = False


def scan_articles():
    """扫描 articles/ 目录，返回文章元数据列表。"""
    articles = []
    if not os.path.isdir(ARTICLES_DIR):
        print(f"错误: articles 目录不存在: {ARTICLES_DIR}")
        return articles

    for fname in sorted(os.listdir(ARTICLES_DIR)):
        if not fname.endswith(".html") or fname == "template.html":
            continue

        fpath = os.path.join(ARTICLES_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            html = f.read()

        parser = ArticleMetaParser()
        parser.feed(html)

        # 如果没有设置 date，用文件修改时间
        if not parser.date:
            mtime = os.path.getmtime(fpath)
            parser.date = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

        # 如果没有设置 category，默认"未分类"
        if not parser.category:
            parser.category = "未分类"

        file_id = fname.replace(".html", "")

        articles.append({
            "id": file_id,
            "title": parser.title or file_id,
            "category": parser.category,
            "date": parser.date,
            "summary": parser.description or "",
            "file": f"articles/{fname}",
        })

    return articles


def generate_article_data_js(articles):
    """根据文章列表生成 article-data.js 的内容。"""
    # 按 category 分组
    categories = {}
    for art in articles:
        cat = art["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(art)

    cat_entries = []
    for cat_name in sorted(categories.keys()):
        art_list = categories[cat_name]
        art_lines = []
        for i, art in enumerate(art_list):
            comma = "," if i < len(art_list) - 1 else ""
            art_lines.append("""        {{
          id: '{}',
          title: '{}',
          date: '{}',
          summary: '{}',
          file: '{}'
        }}{}""".format(art['id'], art['title'], art['date'], art['summary'], art['file'], comma))

        articles_block = "\n".join(art_lines)
        cat_entries.append("""    {{
      name: '{}',
      articles: [
{}
      ]
    }}""".format(cat_name, articles_block))

    cat_block = ",\n".join(cat_entries)

    content = """/**
 * article-data.js - 文章数据中心（大类分组结构）
 *
 * 此文件由 scripts/scan-articles.py 自动生成。
 * 如需修改文章信息，请编辑对应 articles/*.html 中的 <meta> 标签后重新运行脚本。
 * 手工添加的 tags 等信息请在此文件生成后再补充。
 *
 * 设计说明：
 *   siteData.categories 按大类分组（硬件/EDA/软件开发/随笔等）
 *   首页展示大类 → 用户选择大类后显示该分类下文章列表
 *   同时提供扁平数据 articleData，供归档页使用
 */

var siteData = {{
  categories: [
{}
  ]
}};

// ===== 自动生成扁平数据，供归档页使用 =====
var articleData = [];
(function () {{
  for (var i = 0; i < siteData.categories.length; i++) {{
    var cat = siteData.categories[i];
    for (var j = 0; j < cat.articles.length; j++) {{
      var art = cat.articles[j];
      articleData.push({{
        id: art.id,
        title: art.title,
        category: cat.name,
        date: art.date,
        summary: art.summary,
        file: art.file
      }});
    }}
  }}
}})();
""".format(cat_block)
    return content


def generate_static_cards_html(articles):
    """根据文章列表生成 index.html 中的静态回退卡片 HTML。"""
    # 按 category 分组
    categories = {}
    for art in articles:
        cat = art["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(art)

    lines = []
    for cat_name in sorted(categories.keys()):
        art_list = categories[cat_name]
        lines.append(f'    <!-- === {cat_name} === -->')
        lines.append(f'    <div class="cat-section-header">{cat_name}</div>')
        for art in art_list:
            search_text = f"{art['title']} {art['summary']}"
            lines.append(f'    <article class="article-card" data-category="{cat_name}" data-search="{search_text}">')
            lines.append(f'      <h2><a href="{art["file"]}">{art["title"]}</a></h2>')
            lines.append(f'      <div class="meta">{cat_name} · {art["date"]}</div>')
            lines.append(f'      <p class="summary">{art["summary"]}</p>')
            lines.append(f'    </article>')
            lines.append('')

    return '\n'.join(lines)


def update_index_html(cards_html):
    """更新 index.html 中的静态卡片区域。"""
    if not os.path.exists(INDEX_FILE):
        print(f"错误: index.html 不存在: {INDEX_FILE}")
        return False

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 匹配 <!-- ===== 文章列表（静态 HTML，不依赖 JS 渲染） ===== --> 到下一个独立的注释块或 </div> 之前
    pattern = r'(<!-- ===== 文章列表（静态 HTML，不依赖 JS 渲染） ===== -->\s*<div id="article-container">\s*)(.*?)(\s*</div>\s*<!-- ===== 搜索框)'
    replacement = rf'\1\n{cards_html}\n    \3'

    # 如果上面的模式不匹配（注释可能稍有差异），尝试更宽松的模式
    if not re.search(pattern, content, re.DOTALL):
        pattern = r'(<div id="article-container">)(.*?)(\s*</div>)'
        replacement = rf'\1\n{cards_html}\n    \3'

    if not re.search(pattern, content, re.DOTALL):
        print("错误: 无法在 index.html 中找到 article-container 节点")
        return False

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


def main():
    print("=" * 60)
    print("  文章自动扫描工具")
    print("=" * 60)
    print()

    # 1. 扫描文章
    articles = scan_articles()
    if not articles:
        print("未找到任何文章，退出。")
        return

    print(f"扫描到 {len(articles)} 篇文章:\n")
    for art in articles:
        print(f"  [{art['category']}] {art['title']}")
        print(f"    日期: {art['date']}  |  文件: {art['file']}")
        print(f"    摘要: {art['summary'][:60]}{'...' if len(art['summary']) > 60 else ''}")
        print()

    # 2. 生成 article-data.js
    js_content = generate_article_data_js(articles)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"[✓] 已更新: {DATA_FILE}")

    # 3. 生成静态卡片并更新 index.html
    cards_html = generate_static_cards_html(articles)
    if update_index_html(cards_html):
        print(f"[✓] 已更新 index.html 静态回退卡片")
    else:
        print(f"[✗] index.html 更新失败，请手动检查")

    print()
    print("=" * 60)
    print("  完成！请检查生成的文件后提交。")
    print("=" * 60)


if __name__ == "__main__":
    main()