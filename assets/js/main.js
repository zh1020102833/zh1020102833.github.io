/**
 * main.js - 首页控制中枢
 *
 * 功能：
 *   1. 大类导航 —— 顶部显示大类按钮（硬件 / 嵌入式 / FPGA / 高速信号 / EMC / 控制理论 / 电机 / EDA / 随笔）
 *      点击切换，仅显示该分类下的文章
 *   2. 文章列表 —— 展示选中大类下的所有文章卡片
 *   3. 站内搜索 —— 实时搜索文章标题、摘要、分类名
 *
 * 数据来源：article-data.js 中的 siteData 全局变量
 */

(function () {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    var container = document.getElementById('article-container');
    var tabBar = document.getElementById('category-tabs');
    var searchInput = document.getElementById('search-input');
    if (!container || !tabBar) return;

    var selectedCat = 'all';       // 当前选中的大类
    var searchKeyword = '';        // 当前搜索关键词

    // ---- 1. 渲染大类导航标签 ----
    function renderTabs() {
      // "全部" 标签
      var allTab = document.createElement('button');
      allTab.textContent = '全部';
      allTab.dataset.cat = 'all';
      if (selectedCat === 'all') allTab.className = 'active';
      tabBar.appendChild(allTab);

      // 各分类标签
      for (var i = 0; i < siteData.categories.length; i++) {
        var cat = siteData.categories[i];
        var btn = document.createElement('button');
        btn.textContent = cat.name;
        btn.dataset.cat = cat.name;
        if (selectedCat === cat.name) btn.className = 'active';
        tabBar.appendChild(btn);
      }
    }

    // ---- 2. 切换大类 ----
    tabBar.addEventListener('click', function (e) {
      if (e.target.tagName !== 'BUTTON') return;
      var cat = e.target.dataset.cat;

      // 更新按钮状态
      var activeBtn = tabBar.querySelector('.active');
      if (activeBtn) activeBtn.className = '';
      e.target.className = 'active';

      selectedCat = cat;
      searchKeyword = '';             // 切换分类时清空搜索
      if (searchInput) searchInput.value = '';
      renderArticles();
    });

    // ---- 3. 搜索功能 ----
    if (searchInput) {
      searchInput.addEventListener('input', function () {
        searchKeyword = this.value.trim().toLowerCase();
        selectedCat = 'all';          // 搜索时重置为"全部"

        // 重置分类标签高亮
        var activeBtn = tabBar.querySelector('.active');
        if (activeBtn) activeBtn.className = '';
        var allTab = tabBar.querySelector('[data-cat="all"]');
        if (allTab) allTab.className = 'active';

        renderArticles();
      });
    }

    // ---- 4. 渲染文章列表 ----
    function renderArticles() {
      container.innerHTML = '';

      // 收集匹配的文章
      var results = [];
      var catList = siteData.categories;

      for (var i = 0; i < catList.length; i++) {
        var cat = catList[i];

        // 如果选了具体大类，跳过不匹配的
        if (selectedCat !== 'all' && cat.name !== selectedCat) continue;

        for (var j = 0; j < cat.articles.length; j++) {
          var art = cat.articles[j];

          // 搜索过滤
          if (searchKeyword) {
            var matchTitle = art.title.toLowerCase().indexOf(searchKeyword) !== -1;
            var matchSummary = art.summary.toLowerCase().indexOf(searchKeyword) !== -1;
            var matchCat = cat.name.toLowerCase().indexOf(searchKeyword) !== -1;
            if (!matchTitle && !matchSummary && !matchCat) continue;
          }

          results.push({
            article: art,
            category: cat.name
          });
        }
      }

      // 空状态
      if (results.length === 0) {
        container.innerHTML =
          '<div class="empty-state"><p>' +
          (searchKeyword ? '未找到匹配 "' + escapeHtml(searchKeyword) + '" 的文章' : '该分类暂无文章') +
          '</p></div>';
        return;
      }

      // 按日期倒序排列
      results.sort(function (a, b) {
        return b.article.date.localeCompare(a.article.date);
      });

      // 渲染卡片
      var currentCat = '';
      for (var i = 0; i < results.length; i++) {
        var item = results[i];
        var art = item.article;

        // 在"全部"视图下，切换分类时显示分类分隔标题
        if (selectedCat === 'all' && !searchKeyword && item.category !== currentCat) {
          currentCat = item.category;
          var sectionHeader = document.createElement('div');
          sectionHeader.className = 'cat-section-header';
          sectionHeader.textContent = currentCat;
          container.appendChild(sectionHeader);
        }

        var card = document.createElement('article');
        card.className = 'article-card';
        card.innerHTML =
          '<h2><a href="' + art.file + '">' + escapeHtml(art.title) + '</a></h2>' +
          '<div class="meta">' + escapeHtml(item.category) + ' &middot; ' + escapeHtml(art.date) + '</div>' +
          '<p class="summary">' + escapeHtml(art.summary) + '</p>';
        container.appendChild(card);
      }
    }

    // ---- 5. 工具函数 ----
    function escapeHtml(str) {
      var d = document.createElement('div');
      d.appendChild(document.createTextNode(str));
      return d.innerHTML;
    }

    // ---- 启动 ----
    renderTabs();
    renderArticles();
  }
})();
