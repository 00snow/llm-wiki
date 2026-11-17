/* AI 入門講解 Wiki — 網站邏輯
 * 讀 wiki/index.md（目錄）→ 讀每一頁的 frontmatter → 側欄、首頁學習路線、搜尋、反向連結。
 * 一般新增內容不需要修改這個檔案（見 AGENTS.md）。
 */
(() => {
  const WIKI = "wiki/";
  const SECTIONS = { "概念": { type: "concept", dir: "concepts/" }, "來源": { type: "source", dir: "sources/" } };
  const FIXED = { home: "overview.md", log: "log.md", index: "index.md" };
  const FIXED_TITLE = { home: "首頁", log: "維護紀錄", index: "目錄" };
  const state = { pages: [], bySlug: new Map(), raw: new Map(), backlinks: new Map() };

  const $ = (s) => document.querySelector(s);
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const pad = (n) => String(n).padStart(2, "0");

  async function load(path) {
    if (state.raw.has(path)) return state.raw.get(path);
    const res = await fetch(WIKI + path, { cache: "no-cache" });
    if (!res.ok) throw new Error(`${res.status} ${path}`);
    const t = await res.text();
    state.raw.set(path, t);
    return t;
  }

  /* ---------- frontmatter ---------- */
  function splitFrontmatter(text) {
    const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
    if (!m) return { meta: {}, body: text };
    const meta = {};
    for (const line of m[1].split(/\r?\n/)) {
      const kv = line.match(/^(\w+):\s*(.*?)\s*(#.*)?$/);
      if (!kv) continue;
      let v = kv[2];
      if (/^\[.*\]$/.test(v)) v = v.slice(1, -1).split(",").map((x) => x.trim()).filter(Boolean);
      meta[kv[1]] = v;
    }
    return { meta, body: text.slice(m[0].length) };
  }

  /* ---------- index.md ---------- */
  function parseIndex(md) {
    const pages = [];
    let section = null;
    for (const line of md.split(/\r?\n/)) {
      const h = line.match(/^##\s+(.+?)\s*$/);
      if (h) { section = SECTIONS[h[1]] || null; continue; }
      const item = line.match(/^-\s+\[\[([a-z0-9-]+)\]\]\s*[—–-]\s*(.+)$/);
      if (item && section) {
        pages.push({ slug: item[1], summary: item[2].trim(), type: section.type,
          path: section.dir + item[1] + ".md", order: pages.filter((p) => p.type === section.type).length + 1 });
      }
    }
    return pages;
  }

  /* ---------- wiki links ---------- */
  const LINK_RE = /\[\[([a-z0-9-]+)(?:\|([^\]]+))?\]\]/g;
  const outsideCode = (md, fn) => md.split(/(```[\s\S]*?```|`[^`\n]*`)/g).map((p, i) => (i % 2 ? p : fn(p))).join("");

  function linkify(md) {
    return outsideCode(md, (s) => s.replace(LINK_RE, (_, slug, label) => {
      const p = state.bySlug.get(slug);
      const title = p ? p.title : FIXED_TITLE[slug];
      const text = esc(label || title || slug);
      return title
        ? `<a class="wikilink" href="#/${slug}">${text}</a>`
        : `<span class="wikilink broken" title="尚未建立的頁面：${esc(slug)}">${text}</span>`;
    }));
  }
  function linksIn(md) {
    const out = new Set();
    outsideCode(md, (s) => { for (const m of s.matchAll(LINK_RE)) out.add(m[1]); return s; });
    return out;
  }
  const render = (body) => marked.parse(linkify(body));

  /* ---------- sidebar ---------- */
  function renderNav(query = "") {
    const q = query.trim().toLowerCase();
    const hit = (p) => !q || [p.title, p.summary, p.slug, ...(p.tags || [])].join(" ").toLowerCase().includes(q) ||
      (state.raw.get(p.path) || "").toLowerCase().includes(q);
    let html = q ? "" : `<ul>
      <li><a href="#/home" data-slug="home"><span class="num">✿</span>首頁・學習路線</a></li>
      <li><a href="#/index" data-slug="index"><span class="num">≡</span>目錄</a></li>
      <li><a href="#/log" data-slug="log"><span class="num">✎</span>維護紀錄</a></li></ul>`;
    for (const [label, { type }] of Object.entries(SECTIONS)) {
      const list = state.pages.filter((p) => p.type === type && hit(p));
      html += `<h2>${type === "concept" ? "Concepts · 概念" : "Sources · 來源"}</h2>`;
      html += list.length
        ? `<ul>${list.map((p) => `<li><a href="#/${p.slug}" data-slug="${p.slug}"><span class="num">${type === "concept" ? pad(p.order) : "·"}</span>${esc(p.short)}</a></li>`).join("")}</ul>`
        : `<p class="empty">沒有符合的${label}</p>`;
    }
    $("#nav").innerHTML = html;
    markActive();
  }
  const current = () => decodeURIComponent(location.hash.replace(/^#\/?/, "")) || "home";
  function markActive() {
    const s = current();
    document.querySelectorAll("#nav a").forEach((a) => a.classList.toggle("active", a.dataset.slug === s));
  }

  /* ---------- views ---------- */
  async function viewHome() {
    const { body } = splitFrontmatter(await load(FIXED.home));
    const concepts = state.pages.filter((p) => p.type === "concept");
    const sources = state.pages.filter((p) => p.type === "source");
    const [intro, ...rest] = render(body).split(/(?=<h2)/);
    return `<article class="article">
      <section class="hero"><div class="eyebrow">LLM Wiki · AI 入門講解</div>${intro}</section>
      <h2>學習路線</h2>
      <ol class="path">${concepts.map((p) => `<li><a href="#/${p.slug}">
        <span class="step">${pad(p.order)}</span>
        <span><h3>${esc(p.title)}</h3><p>${esc(p.summary)}</p></span></a></li>`).join("")}</ol>
      ${rest.join("")}
      <h2>資料來源</h2>
      <div class="cards">${sources.map((p) => `<a class="card" href="#/${p.slug}">${esc(p.title)}<span>${esc(p.summary)}</span></a>`).join("")}</div>
    </article>`;
  }

  async function viewFixed(slug) {
    const { body } = splitFrontmatter(await load(FIXED[slug]));
    const eyebrow = slug === "log" ? "Log · 維護紀錄" : "Index · 目錄";
    return `<article class="article"><div class="eyebrow">${eyebrow}</div>${render(body)}</article>`;
  }

  function pager(p) {
    if (p.type !== "concept") return "";
    const list = state.pages.filter((x) => x.type === "concept");
    const i = list.indexOf(p), prev = list[i - 1], next = list[i + 1];
    return `<nav class="pager">
      ${prev ? `<a href="#/${prev.slug}"><small>← PREV</small>${esc(prev.title)}</a>` : ""}
      ${next ? `<a class="next" href="#/${next.slug}"><small>NEXT →</small>${esc(next.title)}</a>` : ""}
    </nav>`;
  }

  async function viewPage(slug) {
    const p = state.bySlug.get(slug);
    if (!p) return `<article class="article"><div class="eyebrow">404</div><h1>找不到這一頁</h1>
      <p>wiki 裡還沒有 <code>${esc(slug)}</code>。<a href="#/home">回首頁</a></p></article>`;
    const { body } = splitFrontmatter(await load(p.path));
    const eyebrow = p.type === "concept" ? `Concept · ${pad(p.order)}` : "Source · 來源";
    const meta = `<div class="meta">
      ${(p.tags || []).map((t) => `<span class="chip">${esc(t)}</span>`).join("")}
      ${p.sources ? `<span class="chip butter">引用 ${esc(p.sources)} 份來源</span>` : ""}
      <span>更新於 ${esc(p.updated || "—")}</span></div>`;
    const html = render(body).replace("</h1>", `</h1>${meta}`);
    const back = [...(state.backlinks.get(slug) || [])].map((s) => state.bySlug.get(s)).filter(Boolean);
    const backHtml = `<section class="backlinks"><h2>反向連結 · 有哪些頁面提到這裡</h2>${
      back.length ? `<ul>${back.map((b) => `<li><a class="wikilink" href="#/${b.slug}">${esc(b.title)}</a></li>`).join("")}</ul>`
        : `<p class="muted">目前沒有其他頁面連到這裡。</p>`}</section>`;
    return `<article class="article"><div class="eyebrow">${eyebrow}</div>${html}${pager(p)}${backHtml}</article>`;
  }

  async function route() {
    const slug = current();
    const main = $("#content");
    try {
      main.innerHTML = slug === "home" ? await viewHome() : FIXED[slug] ? await viewFixed(slug) : await viewPage(slug);
      const p = state.bySlug.get(slug);
      document.title = (p ? p.short + " · " : FIXED_TITLE[slug] && slug !== "home" ? FIXED_TITLE[slug] + " · " : "") + "AI 入門講解 Wiki";
    } catch (e) {
      main.innerHTML = `<article class="article"><h1>載入失敗</h1><p>${esc(e.message)}</p>
        <p class="muted">如果是直接開啟本機檔案，請改用 <code>python -m http.server</code>。</p></article>`;
    }
    window.scrollTo(0, 0);
    markActive();
    closeMenu();
  }

  /* ---------- mobile menu ---------- */
  function closeMenu() { $("#sidebar").classList.remove("open"); $("#menuBtn").setAttribute("aria-expanded", "false"); }
  $("#menuBtn").addEventListener("click", () => {
    const open = $("#sidebar").classList.toggle("open");
    $("#menuBtn").setAttribute("aria-expanded", String(open));
  });

  /* ---------- boot ---------- */
  async function init() {
    marked.setOptions({ gfm: true });
    try {
      state.pages = parseIndex(await load(FIXED.index));
    } catch (e) {
      $("#content").innerHTML = `<article class="article"><h1>讀不到 wiki/index.md</h1>
        <p class="muted">請在專案根目錄執行 <code>python -m http.server</code> 後再開啟。</p></article>`;
      return;
    }
    await Promise.all(state.pages.map(async (p) => {
      try {
        const { meta, body } = splitFrontmatter(await load(p.path));
        const h1 = body.match(/^#\s+(.+)$/m);
        Object.assign(p, meta, { title: meta.title || (h1 ? h1[1] : p.slug) });
        for (const t of linksIn(body)) {
          if (t === p.slug) continue;
          if (!state.backlinks.has(t)) state.backlinks.set(t, new Set());
          state.backlinks.get(t).add(p.slug);
        }
      } catch (e) { p.title = p.slug; console.warn("無法讀取", p.path, e); }
      p.short = p.title.replace(/（.*?）/g, "");
      state.bySlug.set(p.slug, p);
    }));
    renderNav();
    $("#search").addEventListener("input", (e) => renderNav(e.target.value));
    window.addEventListener("hashchange", route);
    route();
  }
  init();
})();
