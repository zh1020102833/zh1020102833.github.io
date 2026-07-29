/**
 * article-data.js - 文章数据中心（大类分组结构）
 *
 * 此文件由 scripts/scan-articles.py 自动生成。
 * 如需修改文章信息，请编辑对应 articles/*.html 中的 <meta> 标签后重新运行脚本。
 * 手工添加的 tags 等信息请在此文件生成后再补充。
 *
 * 设计说明：
 *   siteData.categories 按大类分组（硬件 / 高速信号 / EDA / 嵌入式 / FPGA / EMC / 控制理论 / 电机 / 随笔）
 *   首页展示大类 → 用户选择大类后显示该分类下文章列表
 *   同时提供扁平数据 articleData，供归档页使用
 */

var siteData = {
  categories: [
    {
      name: '硬件',
      articles: [
        {
          id: 'euler-to-transfer-function',
          title: '从欧拉公式到传递函数：信号处理的数学链路',
          date: '2026-06-19',
          summary: '从欧拉公式出发，串联复数阻抗、拉普拉斯变换、传递函数到Bode图，结合全通相移器实例，建立完整的信号处理数学链路。',
          file: 'articles/euler-to-transfer-function.html'
        },
        {
          id: 'virtual-short-virtual-open-limitations',
          title: '虚短与虚断 · 原理及应用局限性',
          date: '2026-06-22',
          summary: '从负反馈数学模型出发，推导虚短虚断的成立条件与误差界限，分析开环增益、反馈深度对近似精度的影响，揭示应用局限性。',
          file: 'articles/virtual-short-virtual-open-limitations.html'
        }
      ]
    },
    {
      name: '嵌入式',
      articles: [

      ]
    },
    {
      name: 'FPGA',
      articles: [

      ]
    },
    {
      name: '高速信号',
      articles: [

      ]
    },
    {
      name: 'EMC',
      articles: [

      ]
    },
    {
      name: '控制理论',
      articles: [

      ]
    },
    {
      name: '电机',
      articles: [

      ]
    },
    {
      name: 'EDA',
      articles: [

      ]
    },
    {
      name: '随笔',
      articles: [
        {
          id: '语雀文章转换工作流规范',
          title: '和',
          date: '2026-07-27',
          summary: '定义 MD 转 HTML 的目录约定、YAML 头部格式、转换规则与自动化流程',
          file: 'articles/语雀文章转换工作流规范.html'
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
