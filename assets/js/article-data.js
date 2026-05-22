/**
 * article-data.js - 文章数据中心（大类分组结构）
 *
 * 设计说明：
 *   siteData.categories 按大类分组（硬件/EDA/软件开发/随笔等）
 *   首页展示大类 → 用户选择大类后显示该分类下文章列表
 *   同时提供扁平数据 articleData，供归档页使用
 *
 * 新增文章步骤：
 *   1. 在 articles/ 目录下创建 HTML 文件
 *   2. 在下方对应大类的 articles 数组中添加新条目
 *   3. 保存并重新上传即可
 *
 * 新增大类步骤：
 *   1. 在 siteData.categories 中添加新分组
 *   2. 首页自动显示新大类按钮
 */

var siteData = {
  categories: [
    // ===== 硬件 =====
    {
      name: '硬件',
      articles: [
        {
          id: 'hardware-intro',
          title: '硬件设计入门基础',
          date: '2026-05-22',
          summary: '介绍硬件设计的基本流程和常用工具，适合电子工程师入门参考。',
          file: 'articles/hardware-intro.html'
        }
      ]
    },

    // ===== EDA =====
    {
      name: 'EDA',
      articles: [
        {
          id: 'eda-tools',
          title: '常用 EDA 工具介绍',
          date: '2026-05-22',
          summary: '整理主流 EDA 工具的功能特点与选型建议，涵盖 Altium、KiCad 等。',
          file: 'articles/eda-tools.html'
        }
      ]
    },

    // ===== 软件开发 =====
    {
      name: '软件开发',
      articles: [
        {
          id: 'web-dev-basics',
          title: '前端开发基础：HTML 核心标签',
          date: '2026-05-22',
          summary: '整理前端开发中最常用的 HTML 标签及其语义化用法，适合初学者参考。',
          file: 'articles/web-dev-basics.html'
        }
      ]
    },

    // ===== 随笔 =====
    {
      name: '随笔',
      articles: [
        {
          id: 'hello-world',
          title: 'Hello World - 我的第一篇博客',
          date: '2026-05-22',
          summary: '网站的第一篇文章，介绍了搭建本静态博客的初衷和使用方式。',
          file: 'articles/hello-world.html'
        },
        {
          id: 'writing-tips',
          title: '如何写出清晰的技术文章',
          date: '2026-05-22',
          summary: '分享技术写作的经验与技巧，包括结构组织、语言表达和读者视角等方面的建议。',
          file: 'articles/writing-tips.html'
        }
      ]
    }
  ]
};

// ===== 自动生成扁平数据，供归档页使用 =====
var articleData = [];
(function () {
  for (var i = 0; i < siteData.categories.length; i++) {
    var cat = siteData.categories[i];
    for (var j = 0; j < cat.articles.length; j++) {
      var art = cat.articles[j];
      articleData.push({
        id: art.id,
        title: art.title,
        category: cat.name,
        date: art.date,
        summary: art.summary,
        file: art.file
      });
    }
  }
})();

// ===== 新增文章模板（复制到对应大类的 articles 数组中） =====
// {
//   id: 'your-article-id',
//   title: '文章标题',
//   date: '2026-05-22',
//   summary: '文章简介，显示在首页卡片上',
//   file: 'articles/your-article-file.html'
// }
