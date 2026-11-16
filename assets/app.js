/* LLM 學習 Wiki — 網站邏輯
 * 讀取 wiki/pages.json → 渲染側欄；依 hash 路由載入 Markdown；
 * 把 [[slug]] / [[slug|文字]] 轉成連結；計算反向連結；全文搜尋。
 * 一般新增內容不需要修改這個檔案（見 CLAUDE.md）。
 */
(() => {
  const WIKI = "wiki/";
  const TYPE_LABEL = { concept: "概念", source: "來源" };
  const state = { pages: [], bySlug: new Map(), text: new Map(), backlinks: new Map() };

  const $ = (sel) => document.querySelector(sel);
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  async function fetchText(path) {
    if (state.text.has(path)) return state.text.get(path);
    const res = await fetch(WIKI + path, { cache: "no-cache" });
    if (!res.ok) throw new Error(`${res.status} ${path}`);
    const t = await res.text();
    state.text.set(path, t);
    return t;
  }

  /* ---------- wiki links ---------- */
  const LINK_RE = /\[\[([a-z0-9-]+)(?:\|([^\]]+))?\]\]/g;

  // 只處理程式碼區塊以外的文字
  function mapOutsideCode(md, fn) {
    return md.split(/(```[\s\S]*?```|`[^`\n]*`)/g)
      .map((part, i) => (i % 2 ? part : fn(part)))
      .join("");
  }

  function linkify(md) {
    return mapOutsideCode(md, (s) => s.replace(LINK_RE, (_, slug, label) => {
      const page = state.bySlug.get(slug) || (slug === "home" || slug === "log" ? { title: slug === "home" ? "首頁" : "維護紀錄" } : null);
      const text = esc(label || (page ? page.title : slug));
      return page
        ? `<a class="wikilink" href="#/${slug}">${text}</a>`
        : `<span class="wikilink broken" title="尚未建立的頁面：${esc(slug)}">${text}</span>`;
    }));
  }

  function linksIn(md) {
    const out = new Set();
    mapOutsideCode(md, (s) => { for (const m of s.matchAll(LINK_RE)) out.add(m[1]); return s; });
    return out;
  }

  async function buildBacklinks() {
    await Promise.all(state.pages.map(async (p) => {
      try {
        const md = await fetchText(p.path);
        for (const target of linksIn(md)) {
          if (target === p.slug) continue;
          if (!state.backlinks.has(target)) state.backlinks.set(target, new Set());
          state.backlinks.get(target).add(p.slug);
        }
      } catch (e) { console.warn("無法讀取", p.path, e); }
    }));
  }

  /* ---------- sidebar ---------- */
  function renderNav(query = "") {
    const q = query.trim().toLowerCase();
    const match = (p) => !q ||
      [p.title, p.summary, p.slug, ...(p.tags || [])].join(" ").toLowerCase().includes(q) ||
      (state.text.get(p.path) || "").toLowerCase().includes(q);

    let html = q ? "" : `
      <ul>
        <li><a href="#/home" data-slug="home">首頁</a></li>
        <li><a href="#/log" data-slug="log">維護紀錄</a></li>
      </ul>`;

    for (const type of Object.keys(TYPE_LABEL)) {
      const list = state.pages.filter((p) => p.type === type && match(p));
      html += `<h2>${TYPE_LABEL[type]} <span class="count">${list.length}</span></h2>`;
      html += list.length
        ? `<ul>${list.map((p) => `<li><a href="#/${p.slug}" data-slug="${p.slug}">${esc(p.title)}</a></li>`).join("")}</ul>`
        : `<p class="empty">沒有符合的頁面</p>`;
    }
    $("#nav").innerHTML = html;
    markActive();
  }

  function markActive() {
    const slug = currentSlug();
    document.querySelectorAll("#nav a").forEach((a) =>
      a.classList.toggle("active", a.dataset.slug === slug));
  }

  /* ---------- views ---------- */
  const currentSlug = () => decodeURIComponent(location.hash.replace(/^#\/?/, "")) || "home";

  function card(p) {
    return `<a class="card" href="#/${p.slug}">
      <h3>${esc(p.title)}</h3>
      <p>${esc(p.summary || "")}</p>
      <div class="tags">${(p.tags || []).map((t) => `<span class="tag">${esc(t)}</span>`).join("")}</div>
    </a>`;
  }

  async function viewHome() {
    const md = await fetchText("home.md");
    const concepts = state.pages.filter((p) => p.type === "concept");
    const sources = state.pages.filter((p) => p.type === "source");
    const links = [...state.backlinks.values()].reduce((n, s) => n + s.size, 0);
    const latest = state.pages.map((p) => p.updated).sort().pop() || "—";
    return `<article class="article">
      ${marked.parse(linkify(md))}
      <div class="stats">
        <div class="stat"><b>${concepts.length}</b><span>概念頁</span></div>
        <div class="stat"><b>${sources.length}</b><span>來源頁</span></div>
        <div class="stat"><b>${links}</b><span>頁面間連結</span></div>
        <div class="stat"><b class="date">${esc(latest)}</b><span>最後更新</span></div>
      </div>
      <h2>概念</h2><div class="cards">${concepts.map(card).join("")}</div>
      <h2>來源</h2><div class="cards">${sources.map(card).join("")}</div>
    </article>`;
  }

  async function viewPage(slug) {
    if (slug === "log") {
      return `<article class="article">${marked.parse(linkify(await fetchText("log.md")))}</article>`;
    }
    const p = state.bySlug.get(slug);
    if (!p) {
      return `<article class="article"><h1>找不到頁面</h1>
        <p>wiki 中還沒有 <code>${esc(slug)}</code> 這一頁。<a href="#/home">回首頁</a></p></article>`;
    }
    const md = await fetchText(p.path);
    let html = marked.parse(linkify(md));
    const meta = `<div class="meta">
      <span class="type-badge">${TYPE_LABEL[p.type] || p.type}</span>
      ${(p.tags || []).map((t) => `<span class="tag">${esc(t)}</span>`).join("")}
      <span>· 更新於 ${esc(p.updated || "—")}</span>
    </div>`;
    // 把 meta 放在 h1 後面
    html = html.replace(/(<\/h1>)/, `$1${meta}`);

    const back = [...(state.backlinks.get(slug) || [])]
      .map((s) => state.bySlug.get(s)).filter(Boolean)
      .sort((a, b) => a.title.localeCompare(b.title, "zh-Hant"));
    const backHtml = `<section class="backlinks"><h2>反向連結 · 哪些頁面提到這裡</h2>${
      back.length
        ? `<ul>${back.map((b) => `<li><a class="wikilink" href="#/${b.slug}">${esc(b.title)}</a> <span class="muted">（${TYPE_LABEL[b.type]}）</span></li>`).join("")}</ul>`
        : `<p class="muted">目前沒有其他頁面連到這裡。</p>`
    }</section>`;
    return `<article class="article">${html}${backHtml}</article>`;
  }

  async function route() {
    const slug = currentSlug();
    const main = $("#content");
    try {
      main.innerHTML = slug === "home" ? await viewHome() : await viewPage(slug);
      const h1 = main.querySelector("h1");
      document.title = (slug === "home" || !h1 ? "" : h1.textContent + " · ") + "LLM 學習 Wiki";
    } catch (e) {
      main.innerHTML = `<article class="article"><h1>載入失敗</h1>
        <p>${esc(e.message)}</p>
        <p class="muted">若是直接開啟本機檔案，請改用 <code>python -m http.server</code> 預覽。</p></article>`;
    }
    window.scrollTo(0, 0);
    markActive();
    closeMenu();
  }

  /* ---------- mobile menu ---------- */
  function closeMenu() {
    $("#sidebar").classList.remove("open");
    $("#menuBtn").setAttribute("aria-expanded", "false");
  }
  $("#menuBtn").addEventListener("click", () => {
    const open = $("#sidebar").classList.toggle("open");
    $("#menuBtn").setAttribute("aria-expanded", String(open));
  });

  /* ---------- boot ---------- */
  async function init() {
    try {
      const res = await fetch(WIKI + "pages.json", { cache: "no-cache" });
      state.pages = await res.json();
    } catch (e) {
      $("#content").innerHTML = `<article class="article"><h1>讀不到 wiki/pages.json</h1>
        <p class="muted">請用 <code>python -m http.server</code> 在專案根目錄啟動後再開啟。</p></article>`;
      return;
    }
    state.pages.sort((a, b) => a.title.localeCompare(b.title, "zh-Hant"));
    state.pages.forEach((p) => state.bySlug.set(p.slug, p));
    marked.setOptions({ gfm: true });
    renderNav();
    await buildBacklinks();
    $("#search").addEventListener("input", (e) => renderNav(e.target.value));
    window.addEventListener("hashchange", route);
    route();
  }
  init();
})();
