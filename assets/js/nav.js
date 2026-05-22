/**
 * nav.js - 全站通用顶部导航栏
 *
 * 功能：
 *   - 在所有页面自动生成统一顶部导航栏
 *   - 当前页面匹配的菜单项自动高亮
 *   - 移动端自动折叠为汉堡菜单
 *
 * 使用方法：
 *   在所有页面 </body> 前引入: <script src="assets/js/nav.js"></script>
 *   注意：nav.js 必须放在所有 HTML 内容之后、</body> 之前
 *
 * 修改导航菜单：
 *   编辑下方 navLinks 数组即可，格式：
 *     { label: '菜单显示文字', path: '链接地址', match: ['匹配路径1', '匹配路径2'] }
 *   match 数组用于判断当前页是否高亮，通常填该页面对应的 path 即可
 *
 * 修改站点标题：
 *   编辑下方 SITE_TITLE 变量
 */

(function () {
  // ===== 配置区（按需修改） =====
  var SITE_TITLE = '我的文章';       // 导航栏左侧站点名称
  var SITE_LOGO_LINK = '/index.html'; // 点击站点名称跳转的地址

  var navLinks = [
    { label: '首页', path: '/index.html', match: ['/index.html', '/'] },
    { label: '归档', path: '/pages/archive.html', match: ['/pages/archive.html'] },
    { label: '关于', path: '/pages/about.html', match: ['/pages/about.html'] }
  ];

  // ===== 渲染逻辑（无需修改） =====
  // 等 DOM 就绪后再执行
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', buildNav);
  } else {
    buildNav();
  }

  function buildNav() {
    // 防止重复插入
    if (document.querySelector('.site-nav')) return;

    var currentPath = window.location.pathname;

    function isActive(link) {
      for (var i = 0; i < link.match.length; i++) {
        var p = link.match[i];
        if (currentPath === p || currentPath.endsWith(p)) return true;
      }
      return false;
    }

    var navEl = document.createElement('nav');
    navEl.className = 'site-nav';

    var linksHtml = '';
    for (var i = 0; i < navLinks.length; i++) {
      var link = navLinks[i];
      var activeClass = isActive(link) ? ' active' : '';
      linksHtml +=
        '<li><a href="' + link.path + '" class="' + activeClass + '">' + link.label + '</a></li>';
    }

    navEl.innerHTML =
      '<div class="nav-inner">' +
      '<a href="' + SITE_LOGO_LINK + '" class="nav-logo">' + SITE_TITLE + '</a>' +
      '<button class="nav-toggle" aria-label="切换菜单">&#9776;</button>' +
      '<ul class="nav-links">' + linksHtml + '</ul>' +
      '</div>';

    document.body.insertBefore(navEl, document.body.firstChild);

    // ---- 移动端汉堡菜单切换 ----
    var toggleBtn = navEl.querySelector('.nav-toggle');
    var navLinksEl = navEl.querySelector('.nav-links');
    if (toggleBtn && navLinksEl) {
      toggleBtn.addEventListener('click', function () {
        navLinksEl.classList.toggle('open');
      });
    }
  }
})();
