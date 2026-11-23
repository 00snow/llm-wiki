"""節點 E：產生簡報。

slides/outline.json（已通過 check_outline.py）＋ wiki/diagrams/*.svg → slides/index.html
單一 HTML 檔，CSS / JS / SVG 全部內嵌；字型從 Google Fonts 載入。
用法：python slides/pipeline/build_slides.py
"""
import html
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
SLIDES = ROOT / "slides"
TEMPLATE = SLIDES / "pipeline" / "template.html"

PAGE_NAMES = {}


def e(s):
    return html.escape(str(s), quote=True)


def svg(name):
    p = ROOT / "wiki" / "diagrams" / name
    if not p.exists():
        p = SLIDES / name
    t = p.read_text(encoding="utf-8")
    return re.sub(r"<\?xml[^>]*\?>", "", t).strip()


def figure(name, caption=""):
    cap = f"<figcaption>{e(caption)}</figcaption>" if caption else ""
    return f'<figure class="diagram">{svg(name)}{cap}</figure>'


def src_chips(s):
    out = []
    for src in s.get("sources", []):
        if src.startswith("file:"):
            path = src[5:]
            out.append(f'<a class="src" href="../{e(path)}">{e(Path(path).name)}</a>')
        else:
            href = "../#/home" if src == "overview" else f"../#/{src}"
            out.append(f'<a class="src" href="{href}" target="_blank" rel="noopener">{e(PAGE_NAMES.get(src, src))}</a>')
    return "".join(out)


def mathy(t):
    """算式用等寬字，冒號前的說明保持一般字。"""
    if "：" in t:
        a, b = t.split("：", 1)
        return f'<span class="lbl">{e(a)}</span><code>{e(b)}</code>'
    return f"<code>{e(t)}</code>" if re.search(r"[=×]", t) else e(t)


def lead(s):
    return f'<p class="lead">{e(s["lead"])}</p>' if s.get("lead") else ""


def body(s):
    L = s["layout"]
    if L == "title":
        return f"""<div class="cover"><p class="kicker">LLM WIKI · DEEP LEARNING 101</p>
<h1>{e(s['title'])}</h1><p class="subtitle">{e(s['subtitle'])}</p>
<p class="hint">按 → 或空白鍵開始　·　N 顯示講者備註</p></div>"""
    if L == "roadmap":
        cards = "".join(
            f'<a class="stop" href="../#/{e(slug)}" target="_blank" rel="noopener"><b>{i:02d}</b><span>{e(t)}</span><small>{e(d)}</small></a>'
            for i, (t, d, slug) in enumerate(s["items"], 1))
        return f'<h2>{e(s["title"])}</h2><div class="road">{cards}</div>'
    if L == "analogy":
        rows = "".join(f'<div class="pair"><div class="life">{e(a)}</div><div class="arrow">→</div><div class="ai">{e(b)}</div></div>' for a, b in s["pairs"])
        return f'<h2>{e(s["title"])}</h2>{lead(s)}<div class="pairs"><div class="pair head"><div>生活裡</div><div></div><div>在 AI 裡</div></div>{rows}</div>'
    if L == "nest":
        inner = ""
        for name, desc in reversed(s["levels"]):
            inner = f'<div class="ring"><div class="ring-label"><b>{e(name)}</b><small>{e(desc)}</small></div>{inner}</div>'
        return f'<h2>{e(s["title"])}</h2><div class="nest">{inner}</div>'
    if L == "quiz":
        opts = "".join(f'<button class="opt" data-ok="{int(i == s["answer"])}"><b>{"ABC"[i]}</b>{e(o)}</button>' for i, o in enumerate(s["options"]))
        return f'<h2>{e(s["title"])}</h2><p class="question">{e(s["question"])}</p><div class="opts">{opts}</div><p class="explain">{e(s["explain"])}</p>'
    if L == "calc":
        steps = "".join(f"<li>{mathy(t)}</li>" for t in s["steps"])
        take = f'<p class="takeaway">{e(s["takeaway"])}</p>' if s.get("takeaway") else ""
        fig = figure(s["diagram"]) if s.get("diagram") else ""
        cls = "calc" if fig else "calc solo"
        return f'<h2>{e(s["title"])}</h2>{lead(s)}<div class="{cls}"><ol class="steps">{steps}</ol>{fig}</div>{take}'
    if L == "bullets":
        items = "".join(f"<li>{e(b)}</li>" for b in s["bullets"])
        fig = figure(s["diagram"]) if s.get("diagram") else ""
        cls = ("with-fig fig-wide" if s.get("fig") == "wide" else "with-fig") if fig else ""
        return f'<h2>{e(s["title"])}</h2>{lead(s)}<div class="blist {cls}"><ul>{items}</ul>{fig}</div>'
    if L == "table":
        head = "".join(f"<th>{e(h)}</th>" for h in s["head"])
        rows = "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in s["rows"])
        return f'<h2>{e(s["title"])}</h2>{lead(s)}<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>'
    if L == "loop":
        n = len(s["steps"])
        nodes = "".join(f'<div class="lstep"><b>{i}</b>{e(t)}</div>' + ('<div class="larrow">→</div>' if i < n else "") for i, t in enumerate(s["steps"], 1))
        return f'<h2>{e(s["title"])}</h2>{lead(s)}<div class="loopbox"><div class="lrow">{nodes}</div><div class="lback">↺ 回到第 1 步，一直重複</div></div>'
    if L == "myths":
        rows = "".join(f'<div class="myth"><div class="no">✕ {e(a)}</div><div class="yes">✓ {e(b)}</div></div>' for a, b in s["pairs"])
        return f'<h2>{e(s["title"])}</h2>{lead(s)}<div class="myths">{rows}</div>'
    raise ValueError(f"未知的 layout：{L}")


def main():
    ctx = json.loads((SLIDES / "build" / "context.json").read_text(encoding="utf-8"))
    for slug, p in ctx["pages"].items():
        PAGE_NAMES[slug] = re.split(r"[（(]", p["title"])[0].strip()
    PAGE_NAMES["overview"] = "Wiki 首頁"
    outline = json.loads((SLIDES / "outline.json").read_text(encoding="utf-8"))
    n = len(outline["slides"])
    parts = []
    for i, s in enumerate(outline["slides"], 1):
        notes = f'<aside class="notes"><b>講者備註</b>{e(s["notes"])}</aside>' if s.get("notes") else ""
        parts.append(f"""<section class="slide layout-{s['layout']}" id="s{i}" data-id="{e(s['id'])}" aria-label="第 {i} 張，共 {n} 張">
<div class="frame"><p class="eyebrow">{e(s['section'])}</p><div class="body">{body(s)}</div>
<footer><span class="srcs">{'來源 ' if s.get('sources') else ''}{src_chips(s)}</span><span class="pg">{i:02d} / {n:02d}</span></footer></div>{notes}</section>""")
    out = TEMPLATE.read_text(encoding="utf-8")
    out = out.replace("{{TITLE}}", e(outline["title"])).replace("{{SUBTITLE}}", e(outline["subtitle"]))
    out = out.replace("{{SLIDES}}", "\n".join(parts))
    (SLIDES / "index.html").write_text(out, encoding="utf-8")
    print(f"build_slides：{n} 張 → slides/index.html（{len(out) // 1024} KB）")


if __name__ == "__main__":
    main()
