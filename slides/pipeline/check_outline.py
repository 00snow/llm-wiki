"""節點 D：內容檢查。

檢查 slides/outline.json（「整理重點」節點寫的大綱），每一條錯誤都會指出
是哪一張投影片、該退回哪一個節點：

  SOURCE      來源 slug 不存在                → 退回 C（整理重點）
  NUMBER      數字在引用的 wiki 頁找不到       → 退回 C；若 wiki 本來就沒有 → A（取得資料）
  UNVERIFIED  用到 wiki 標「待查證」的內容     → 退回 A（先收錄來源，再重跑 B）
  MATH        算式左右兩邊算出來不相等         → 退回 C
  JARGON      術語還沒解釋就先用了             → 退回 C（調順序或補 defines）
  LENGTH      字數 / 條數超過上限              → 退回 C
  DIAGRAM     講解圖不存在                     → 退回 C
  QUIZ        測驗答案不在選項裡               → 退回 C

每跑一次都會把結果追加到 slides/build/check_history.jsonl，並重寫 check_report.md。
用法：python slides/pipeline/check_outline.py [--round-note "說明"]
離開碼：0 = 全部通過，1 = 有錯誤
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
SLIDES = ROOT / "slides"
BUILD = SLIDES / "build"
sys.path.insert(0, str(Path(__file__).parent))
from query_wiki import numbers_in, norm_text  # noqa: E402

ROUTE = {"SOURCE": "C", "NUMBER": "C/A", "UNVERIFIED": "A", "MATH": "C",
         "JARGON": "C", "LENGTH": "C", "DIAGRAM": "C", "QUIZ": "C", "MISMATCH": "C"}

# 會顯示在投影片上的欄位（notes 是講者備註，不算字數但要查數字）
LIST_FIELDS = ["bullets", "steps", "options", "levels", "pairs", "rows", "items", "head"]


def flat(v):
    if isinstance(v, str):
        return [v]
    if isinstance(v, list):
        return [s for x in v for s in flat(x)]
    return []


def visible_text(s):
    parts = [s.get("title", ""), s.get("lead", ""), s.get("subtitle", ""), s.get("question", ""),
             s.get("explain", ""), s.get("takeaway", ""), s.get("caption", "")]
    for f in LIST_FIELDS:
        parts += flat(s.get(f, []))
    return [p for p in parts if p]


# ---------- 算式檢查 ----------
SAFE = re.compile(r"^[\d\.\s\+\-\*/\(\),]*(?:(?:max|min)[\d\.\s\+\-\*/\(\),]*)*$")


def to_expr(seg):
    e = norm_text(seg).replace("×", "*").replace("÷", "/").replace("²", "**2").strip()
    e = re.sub(r"[，。；]+$", "", e)
    if not e or not re.search(r"\d", e):
        return None
    if not SAFE.match(e.replace("**", "*")):
        return None
    return e


def decimals(seg):
    m = re.findall(r"\d+\.(\d+)", seg)
    return max((len(x) for x in m), default=0)


def check_math(line):
    """'0.5 × 2 + (−1) × 3 = −2' 這類算式，相鄰兩段都能算的話必須相等。"""
    segs = re.split(r"[=≈]", line)
    vals = []
    for seg in segs:
        e = to_expr(seg)
        try:
            v = eval(e, {"__builtins__": {}, "max": max, "min": min}) if e else None
        except Exception:
            v = None
        vals.append((seg, v))
    errs = []
    for (a, va), (b, vb) in zip(vals, vals[1:]):
        if va is None or vb is None or isinstance(va, tuple) or isinstance(vb, tuple):
            continue
        tol = 0.5 * 10 ** -max(decimals(b), decimals(a)) + 1e-9
        if abs(va - vb) > tol:
            errs.append(f"「{a.strip()}」算出來是 {va:g}，不等於「{b.strip()}」")
    return errs


def diagram_section(pages, d):
    """回傳 wiki 裡嵌入這張圖的那個小節（### 或 ## 為界）的文字；圖不在 wiki 裡則回傳 None。"""
    for p in pages.values():
        if f"diagrams/{d})" in p["text"]:
            blocks = re.split(r"\n(?=#{2,3} )", p["text"])
            for k, blk in enumerate(blocks):
                if f"diagrams/{d})" in blk:
                    if blk.startswith("## "):  # 圖在大段開頭 → 整個大段（含底下的 ###）
                        for nxt in blocks[k + 1:]:
                            if nxt.startswith("## "):
                                break
                            blk += "\n" + nxt
                    return blk
    return None


def main():
    note = sys.argv[sys.argv.index("--round-note") + 1] if "--round-note" in sys.argv else ""
    ctx = json.loads((BUILD / "context.json").read_text(encoding="utf-8"))
    rules = json.loads((SLIDES / "pipeline" / "rules.json").read_text(encoding="utf-8"))
    L = rules["limits"]
    outline = json.loads((SLIDES / "outline.json").read_text(encoding="utf-8"))
    pages = ctx["pages"]
    errors = []

    def err(i, s, code, msg):
        errors.append({"slide": i, "id": s.get("id"), "code": code, "route": ROUTE[code], "msg": msg})

    glossary = [g["term"] for g in ctx["glossary"]]
    defined_at = {}
    for i, s in enumerate(outline["slides"], 1):
        for t in s.get("defines", []):
            defined_at.setdefault(t, i)
    first_used = {}

    for i, s in enumerate(outline["slides"], 1):
        texts = visible_text(s)
        joined = "".join(texts)

        # SOURCE
        src_text = ""
        if not s.get("sources"):
            err(i, s, "SOURCE", "沒有標來源")
        for src in s.get("sources", []):
            if src.startswith("file:"):
                f = ROOT / src[5:]
                if f.exists():
                    src_text += f.read_text(encoding="utf-8")
                else:
                    err(i, s, "SOURCE", f"檔案 {src[5:]} 不存在")
            elif src in pages:
                src_text += pages[src]["text"]
            else:
                err(i, s, "SOURCE", f"[[{src}]] 不在 wiki 裡")

        # NUMBER（含講者備註）
        allowed = numbers_in(src_text)
        nums_text = " ".join(texts + [s.get("notes", "")])
        missing = sorted(n for n in numbers_in(nums_text) if n not in allowed)
        if missing and src_text:
            err(i, s, "NUMBER", "引用的頁面裡找不到這些數字：" + ", ".join(f"{n:g}" for n in missing))

        # UNVERIFIED
        for u in ctx["unverified"]:
            if u["term"] in joined or u["term"] in s.get("notes", ""):
                err(i, s, "UNVERIFIED", f"「{u['term']}」在 [[{u['page']}]] 標著待查證，要先收錄來源")

        # MATH
        for line in flat(s.get("steps", [])) + flat(s.get("bullets", [])):
            for m in check_math(line):
                err(i, s, "MATH", m)

        # JARGON（preview 頁只是預告名字，例如封面、路線圖，不算「使用」）
        for t in ([] if s.get("preview") else glossary):
            if t in joined:
                first_used.setdefault(t, i)
        # LENGTH
        if len(s.get("title", "")) > L["title"]:
            err(i, s, "LENGTH", f"標題 {len(s['title'])} 字 > {L['title']}")
        if len(s.get("lead", "")) > L["lead"]:
            err(i, s, "LENGTH", f"引言 {len(s['lead'])} 字 > {L['lead']}")
        for f in ["bullets", "steps", "options", "items", "levels", "pairs"]:
            items = s.get(f, [])
            if s.get("layout") == "roadmap" and f == "items":
                items = [it[:2] for it in items]  # 第三欄是 slug，不顯示
                cap = L["roadmap_items"]
            else:
                cap = L["max_items"]
            if len(items) > cap:
                err(i, s, "LENGTH", f"{f} 有 {len(items)} 條 > {cap}")
            for it in items:
                n = sum(len(x) for x in flat(it))
                if n > L["item"]:
                    err(i, s, "LENGTH", f"{f} 一條 {n} 字 > {L['item']}：{''.join(flat(it))[:16]}…")
        if len(s.get("rows", [])) > L["max_rows"]:
            err(i, s, "LENGTH", f"表格 {len(s['rows'])} 列 > {L['max_rows']}")
        for c in flat(s.get("rows", [])) + flat(s.get("head", [])):
            if len(c) > L["cell"]:
                err(i, s, "LENGTH", f"表格一格 {len(c)} 字 > {L['cell']}：{c[:12]}…")
        total = len(joined)
        if total > L["slide_total"]:
            err(i, s, "LENGTH", f"整張 {total} 字 > {L['slide_total']}")

        # DIAGRAM
        d = s.get("diagram")
        if d and not ((ROOT / "wiki" / "diagrams" / d).exists() or (SLIDES / d).exists()):
            err(i, s, "DIAGRAM", f"找不到圖 {d}")

        # MISMATCH（v2 新增，從版面檢查往前移）：算式和圖必須是同一個例子。
        # 找出這張圖在 wiki 裡嵌在哪一段（### 小節），算式的數字要大多出現在那一段。
        if d and s.get("layout") == "calc":
            sec = diagram_section(pages, d)
            step_nums = numbers_in(" ".join(flat(s.get("steps", []))))
            if sec is not None and step_nums:
                hit = len(step_nums & numbers_in(sec)) / len(step_nums)
                if hit < 0.8:
                    err(i, s, "MISMATCH", f"算式的數字只有 {hit:.0%} 出現在 {d} 所在的 wiki 段落，圖和算式可能不是同一個例子")

        # QUIZ
        if s.get("layout") == "quiz":
            if not (0 <= s.get("answer", -1) < len(s.get("options", []))):
                err(i, s, "QUIZ", "answer 不是選項的位置")

    slides = outline["slides"]
    for t, i in first_used.items():
        j = defined_at.get(t)
        s = slides[i - 1]
        if j is None:
            err(i, s, "JARGON", f"用到「{t}」但沒有任何一張投影片負責解釋它（defines）")
        elif i < j:
            err(i, s, "JARGON", f"「{t}」第 {i} 張就用了，第 {j} 張才解釋")

    errors.sort(key=lambda e: (e["slide"], e["code"]))

    # ---------- 紀錄 ----------
    hist_f = BUILD / "check_history.jsonl"
    rnd = 1 + (sum(1 for _ in hist_f.open(encoding="utf-8")) if hist_f.exists() else 0)
    counts = {}
    for e in errors:
        counts[e["code"]] = counts.get(e["code"], 0) + 1
    rec = {"round": rnd, "time": datetime.now().isoformat(timespec="seconds"), "note": note,
           "rules_version": rules["version"], "slides": len(slides), "errors": len(errors),
           "by_code": counts, "failed_slides": sorted({e["id"] for e in errors}), "details": errors}
    with hist_f.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    hist = [json.loads(l) for l in hist_f.open(encoding="utf-8")]
    md = ["# 內容檢查紀錄（check_outline.py 自動產生）", "",
          "| 輪 | 時間 | 規則版本 | 投影片 | 錯誤 | 類型 | 說明 |", "|---|---|---|---|---|---|---|"]
    for h in hist:
        kinds = "、".join(f"{k} {v}" for k, v in sorted(h["by_code"].items())) or "—"
        md.append(f"| {h['round']} | {h['time'][5:16].replace('T', ' ')} | v{h['rules_version']} | {h['slides']} | {h['errors']} | {kinds} | {h['note']} |")
    for h in hist:
        md += ["", f"## 第 {h['round']} 輪：{h['errors']} 個錯誤", ""]
        md += [f"- 第 {e['slide']} 張 `{e['id']}` **{e['code']}** → 退回 {e['route']}：{e['msg']}" for e in h["details"]] or ["- 全部通過 ✅"]
    (BUILD / "check_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"check_outline 第 {rnd} 輪：{len(slides)} 張投影片，{len(errors)} 個錯誤")
    for e in errors:
        print(f"  [{e['slide']:02d} {e['id']}] {e['code']} → {e['route']}：{e['msg']}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
