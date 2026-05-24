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
          id: 'eeg-signal-chain',
          title: 'EEG 硬件信号链设计笔记',
          date: '2026-05-22',
          summary: '脑电图EEG硬件信号链的完整设计笔记，涵盖前端采集、滤波、ADC选型及噪声优化。',
          file: 'articles/eeg-signal-chain.html'
        },
        {
          id: 'hardware-intro',
          title: '硬件设计入门基础',
          date: '2026-05-22',
          summary: '介绍硬件设计的基本流程和常用工具。',
          file: 'articles/hardware-intro.html'
        },
        {
          id: 'highpass-filter_20260524_151223_322',
          title: '一阶高通滤波器与零点分析',
          date: '2026-05-24',
          summary: '一阶RC高通滤波器的电路结构、传递函数推导、零极点分析与波特图解读',
          file: 'articles/highpass-filter_20260524_151223_322.html'
        },
        {
          id: 'passive-highpass-filter',
          title: '无源高通滤波器的传递函数',
          date: '2026-05-24',
          summary: '以一阶RC与二阶LC高通滤波器为研究对象，推导复频域传递函数，系统分析极点/零点与伯德图特性，涵盖品质因数Q对频率响应的影响及工程选型考量。',
          file: 'articles/passive-highpass-filter.html'
        },
        {
          id: 'signal-conditioning',
          title: '信号调理核心原理',
          date: '2026-05-22',
          summary: '深入讲解信号调理的核心原理，包括放大、滤波、隔离与线性化等关键技术。',
          file: 'articles/signal-conditioning.html'
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
        {
          id: 'high-speed-analog-debug',
          title: '高速模拟电路调试案例',
          date: '2026-05-22',
          summary: '高速模拟电路调试的实战案例合集，涵盖振荡、串扰、电源噪声等常见问题的排查方法。',
          file: 'articles/high-speed-analog-debug.html'
        },
        {
          id: 'high-speed-mixed-signal',
          title: '高速模数混合电路应用笔记',
          date: '2026-05-22',
          summary: '高速模数混合电路设计的应用笔记，涉及PCB布局、接地策略和信号完整性。',
          file: 'articles/high-speed-mixed-signal.html'
        },
        {
          id: 'transmission-line-and-return-current',
          title: '传输线与返回电流',
          date: '2026-05-23',
          summary: '信号完整性入门系列第一讲：传输线定义、返回电流规律、特征阻抗与分布参数基础。',
          file: 'articles/transmission-line-and-return-current.html'
        }
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
        {
          id: 'eda-tools',
          title: '常用 EDA 工具介绍',
          date: '2026-05-22',
          summary: '整理主流 EDA 工具的功能特点与选型建议。',
          file: 'articles/eda-tools.html'
        }
      ]
    },
    {
      name: '随笔',
      articles: [
        {
          id: 'hello-world',
          title: 'Hello World - 我的第一篇博客',
          date: '2026-05-22',
          summary: '这是网站的第一篇文章，欢迎阅读。',
          file: 'articles/hello-world.html'
        },
        {
          id: 'web-dev-basics',
          title: '前端开发基础：HTML 核心标签',
          date: '2026-05-22',
          summary: '整理前端开发中最常用的 HTML 标签及其语义化用法。',
          file: 'articles/web-dev-basics.html'
        },
        {
          id: 'writing-tips',
          title: '如何写出清晰的技术文章',
          date: '2026-05-22',
          summary: '分享技术写作的经验与技巧。',
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
