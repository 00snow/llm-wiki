"""節點 B：查詢 Wiki。

讀 wiki/index.md 決定順序，把每一頁拆成段落，整理出：
  - 每頁出現過的數字（給檢查節點追查用）
  - 標著「待查證」的詞（不可以寫進簡報）
  - 術語表（中文名＋英文，第一次在哪一頁定義）
輸出：
  slides/build/context.json   給腳本讀
  slides/build/context.md     給「整理重點」節點（LLM）讀的資料包
用法：python slides/pipeline/query_wiki.py
"""
import json
import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
BUILD = ROOT / "slides" / "build"

NUM_RE = re.compile(r"\d+(?:\.\d+)?")


def norm_text(s: str) -> str:
    """統一負號、去掉千分位逗號，讓數字比對一致。"""
    s = s.replace("−", "-").replace("–", "-")
    return re.sub(r"(?<=\d),(?=\d{3}\b)", "", s)


def numbers_in(s: str) -> set:
    return {float(m) for m in NUM_RE.findall(norm_text(s))}


def parse_page(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        for line in fm.strip().splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    sections, cur = {}, "_top"
    for line in body.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip()
            sections[cur] = []
        else:
            sections.setdefault(cur, []).append(line)
    one = re.search(r"\*\*一句話\*\*：(.+)", body)
    return {
        "slug": path.stem,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "title": meta.get("title", path.stem),
        "one_liner": one.group(1).strip() if one else "",
        "sections": {k: "\n".join(v).strip() for k, v in sections.items()},
        "text": body,
        "numbers": sorted(numbers_in(body)),
        "diagrams": re.findall(r"!\[[^\]]*\]\(diagrams/([\w\-]+\.svg)\)", body),
    }


def parse_index():
    concepts, sources, part = [], [], None
    for line in (WIKI / "index.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("## 概念"):
            part = concepts
        elif line.startswith("## 來源"):
            part = sources
        m = re.match(r"- \[\[([\w\-]+)\]\] — (.+)", line)
        if m and part is not None:
            part.append({"slug": m.group(1), "summary": m.group(2)})
    return concepts, sources


# 術語：中文名（English）或 x（中文, english）
TERM_RES = [
    re.compile(r"([一-鿿]{2,8})（[A-Za-z][A-Za-z \-]*(?:, ?[A-Za-z]+)?）"),
    re.compile(r"（([一-鿿]{2,6}), ?[a-z][a-z ]*）"),
]
# 抽出來但不是「需要先教」的詞
TERM_SKIP = {"什麼是卷積", "什麼是", "最佳化與梯度下降", "卷積神經網路", "和", "正的就把變數調小", "把窗口"}
# 沒附英文、但講課一定要先解釋的詞
TERM_EXTRA = {"機器學習": "artificial-intelligence", "深度學習": "artificial-intelligence", "神經元": "neural-network",
              "梯度": "optimization", "梯度下降": "optimization", "卷積": "convolution"}


def glossary(pages):
    seen = {}
    for p in pages:
        for rx in TERM_RES:
            for m in rx.finditer(p["text"]):
                t = m.group(1)
                if t not in TERM_SKIP and t not in seen:
                    seen[t] = p["slug"]
    # 「卷積神經網路」用簡稱 CNN 教，這裡收簡稱
    seen.setdefault("CNN", "cnn")
    for t, slug in TERM_EXTRA.items():
        seen.setdefault(t, slug)
    return [{"term": t, "first_page": s} for t, s in seen.items()]


def unverified(pages):
    out = []
    for p in pages:
        for line in p["text"].splitlines():
            if "待查證" in line:
                for b in re.findall(r"\*\*([^*]+)\*\*", line):
                    out.append({"term": re.split(r"[（(]", b)[0], "page": p["slug"], "line": line.strip()})
    return out


def main():
    concepts, sources = parse_index()
    pages = {}
    for c in concepts:
        pages[c["slug"]] = parse_page(WIKI / "concepts" / f"{c['slug']}.md") | {"kind": "concept", "summary": c["summary"]}
    for s in sources:
        pages[s["slug"]] = parse_page(WIKI / "sources" / f"{s['slug']}.md") | {"kind": "source", "summary": s["summary"]}
    pages["overview"] = parse_page(WIKI / "overview.md") | {"kind": "overview", "summary": "首頁"}

    concept_pages = [pages[c["slug"]] for c in concepts]
    ctx = {
        "order": [c["slug"] for c in concepts],
        "pages": pages,
        "glossary": glossary(concept_pages),
        "unverified": unverified(concept_pages),
        "diagrams": sorted(p.name for p in (WIKI / "diagrams").glob("*.svg")),
    }
    BUILD.mkdir(parents=True, exist_ok=True)
    (BUILD / "context.json").write_text(json.dumps(ctx, ensure_ascii=False, indent=1), encoding="utf-8")

    # 給 LLM 的資料包：照閱讀順序，只放講課需要的段落
    keep = ["用生活比喻來想", "它是怎麼運作的", "動手算一次", "動手試一次", "常見誤會", "重點回顧"]
    md = ["# 簡報資料包（由 query_wiki.py 自動產生，不要手改）", ""]
    md += ["## 規則提醒（來自 slides/pipeline/rules.json）", ""]
    rules = json.loads((ROOT / "slides" / "pipeline" / "rules.json").read_text(encoding="utf-8"))
    md += [f"- {r}".format(**rules["limits"]) for r in rules["prompt_rules"]] + [""]
    if ctx["unverified"]:
        md += ["## 不可寫進簡報的詞（Wiki 標著待查證）", ""]
        md += [f"- {u['term']}（{u['page']}）" for u in ctx["unverified"]] + [""]
    md += ["## 術語與首次定義的頁面", "", ", ".join(f"{g['term']}←{g['first_page']}" for g in ctx["glossary"]), ""]
    md += ["## 可用的講解圖", "", ", ".join(ctx["diagrams"]), ""]
    for i, slug in enumerate(ctx["order"], 1):
        p = pages[slug]
        md += [f"---", f"## {i:02d} {p['title']}  [[{slug}]]", "", f"一句話：{p['one_liner']}", ""]
        for k in keep:
            if k in p["sections"]:
                md += [f"### {k}", p["sections"][k], ""]
    (BUILD / "context.md").write_text("\n".join(md), encoding="utf-8")

    print(f"query_wiki: {len(concepts)} 個概念頁、{len(sources)} 個來源頁")
    print(f"  術語 {len(ctx['glossary'])} 個：{', '.join(g['term'] for g in ctx['glossary'])}")
    print(f"  待查證 {len(ctx['unverified'])} 個：{', '.join(u['term'] for u in ctx['unverified']) or '無'}")
    print(f"  → slides/build/context.json、context.md")


if __name__ == "__main__":
    main()
