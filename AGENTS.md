# AGENTS.md — AI 入門講解 Wiki

> 這是給 AI 協作者（Claude Code、Codex、Cursor…）看的**專案規則（schema）**。
> 開始任何工作前，請完整讀完本文件。`CLAUDE.md` 只是匯入本文件的入口。
>
> 本專案參考 Andrej Karpathy 的 **LLM Wiki** 做法：
> <https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>

---

## 1. 專案目的

一個由 AI 持續維護的 Markdown 知識庫，主題是「**走向 LLM 研究之前，要先懂的 AI 基礎**」，
目前涵蓋：什麼是 AI、神經網路（NN）、損失函數、最佳化、反向傳播、卷積、卷積神經網路（CNN）。
（完整清單以 `wiki/index.md` 為準。）

**讀者是「第一次接觸 AI 的人」**。每一頁都要能拿來**講解給別人聽**：
白話、有比喻、有可以跟著算的例子，不假設讀者懂微積分或程式。

### 和 RAG 的不同
RAG 每次提問都重新從原始文件找答案；LLM Wiki 則是讓 AI **事先把資料整理成 wiki**，
知識會累積、交叉連結和矛盾檢查都已經做好。人類負責挑資料、問好問題，AI 負責整理。

---

## 2. 三層架構

| 層 | 位置 | 誰寫 | 規則 |
|----|------|------|------|
| **原始資料 Raw** | `raw/` | 人類挑選（可請 AI 從網路剪輯） | **不可修改**，是唯一的事實依據 |
| **知識庫 Wiki** | `wiki/` | AI | AI 建立、更新、交叉連結；人類閱讀 |
| **規則 Schema** | `AGENTS.md` | 人類與 AI 一起改 | 本文件 |

網站（`index.html` + `assets/`）只是 `wiki/` 的閱讀器，平常不需要改。

---

## 3. 資料夾結構

```
.
├── AGENTS.md              ← 規則（本文件，主要）
├── CLAUDE.md              ← 一行 @AGENTS.md，讓 Claude Code 讀到同一份規則
├── README.md              ← 給人類看的介紹
├── index.html             ← 網站（單頁應用，hash 路由）
├── .nojekyll
├── assets/
│   ├── style.css          ← 韓系風樣式
│   └── app.js             ← 讀 wiki/index.md、渲染 Markdown、[[連結]]、嵌入 SVG 圖、反向連結、搜尋
├── slides/                ← 用 wiki 產生的教學簡報（見 7.4）
│   ├── index.html         ← 產出的簡報（不要手改）
│   ├── outline.json       ← 大綱（LLM 寫的，唯一要手改的內容檔）
│   ├── graph.svg          ← 流程圖
│   ├── WORKFLOW.md        ← 流程設計與反思
│   ├── pipeline/          ← query_wiki.py、check_outline.py、build_slides.py、rules.json、template.html
│   └── build/             ← 自動產生：context.md / context.json、check_report.md、check_history.jsonl
├── raw/                   ← 原始資料（不可修改）
│   ├── assets/            ← 原始資料用到的圖片
│   └── YYYY-MM-DD-來源-主題.md
└── wiki/
    ├── index.md           ← ★ 目錄：每一頁一行（網站靠它運作）
    ├── log.md             ← ★ 維護紀錄（只往上加，不刪）
    ├── overview.md        ← 首頁：學習路線與本站說明
    ├── diagrams/          ← 講解用的 SVG 圖（見 5.4）
    │   └── <主題>.svg
    ├── concepts/          ← 概念講解頁（一個概念一頁）
    │   └── <slug>.md
    └── sources/           ← 來源摘要頁（一份 raw 對應一頁）
        └── <slug>.md
```

---

## 4. 命名規則

- **slug**：小寫英文 + 連字號，例如 `neural-network`、`loss-function`。不用中文、空白、底線、大寫。
- 概念頁：`wiki/concepts/<slug>.md`
- 來源頁：`wiki/sources/src-<來源>-<主題>.md`，例如 `src-cs231n-cnn`
- raw 檔：`raw/YYYY-MM-DD-<來源>-<主題>.md`（日期 = 收錄日，主題可用中文）
- slug 在整個 wiki 中必須唯一。

---

## 5. 頁面格式

每一頁開頭都要有 **YAML frontmatter**（網站會讀取它）：

```yaml
---
title: 神經網路（Neural Network）
type: concept          # concept | source | overview
tags: [基礎]
sources: 2             # 這頁引用了幾份來源
updated: 2026-11-17
---
```

可用的 tags：`入門`、`基礎`、`訓練`、`影像`、`數學`、`方法論`。新增 tag 前先想能不能沿用。

### 5.1 概念講解頁（`wiki/concepts/<slug>.md`）

```markdown
# 頁面標題（和 frontmatter 的 title 相同）

> **一句話**：用一句話講完它是什麼。

## 用生活比喻來想
一個日常生活的比喻，讓完全不懂的人也能抓到感覺。

## 它是怎麼運作的
分步驟或分小節說明。可以用表格、程式碼區塊畫示意圖。

## 動手算一次
一個小到可以用紙筆算的數字例子，每一步都寫出來。

## 常見誤會
- ❌ 誤會 → ✅ 正確理解

## 重點回顧
- 3～5 條，講完一輪後讓聽眾帶走的東西

## 接下來讀什麼
- [[slug]]：為什麼下一步讀它

## 來源
- [[src-xxx]]
```

### 5.2 來源摘要頁（`wiki/sources/src-*.md`）

```markdown
# 來源標題

- **原始檔**：`raw/檔名.md`
- **網址**：<https://...>
- **作者 / 出處**：
- **收錄日期**：YYYY-MM-DD

## 這份資料在講什麼
2～4 句。

## 重點
- 條列（用自己的話）

## 用在哪些頁
- [[concept-slug]]
```

### 5.3 寫作規則

1. **繁體中文**；專有名詞第一次出現時附英文，例如「損失函數（Loss Function）」。
2. **講解口吻**：像在跟朋友解釋；短句、一段一個重點；先講直覺，再講公式。
3. 公式放在程式碼區塊裡，並且**一定要用文字解釋每個符號**。
4. 數字、年份、公式**必須出自 `raw/`**；raw 沒有的就不寫，或標「（待查證）」。不可捏造。
5. 用自己的話改寫，**不可大段複製**原始資料。
6. 頁面互連只用 `[[slug]]` 或 `[[slug|顯示文字]]`，不要寫相對路徑連結。
7. 每個概念頁至少連到 **2 個**其他頁；`#` 只用一次，內文從 `##` 開始。
8. 不寫行內 HTML 樣式；外觀一律交給 `assets/style.css`。

### 5.4 講解圖（`wiki/diagrams/*.svg`）

「動手算一次」盡量配一張圖，讓讀者**看圖就能跟著算**。

- **放哪裡**：`wiki/diagrams/<主題>.svg`，檔名用小寫英文 + 連字號，例如 `backprop.svg`。
- **怎麼插入**：在 Markdown 裡寫 `![圖說](diagrams/xxx.svg)`。圖說會顯示在圖的下方，要寫成一句完整的話。
  網站會把 SVG 直接嵌進頁面，所以圖的顏色會跟著淺色 / 深色模式改變。
- **畫法**：
  - `viewBox` 寬度固定 680，高度依內容決定；不要設定 `width` / `height` 屬性。
  - **不可寫死顏色**（不用 `fill="#..."`、`style="..."`），只能用 `style.css` 定義的 class：

    | 用途 | class |
    |------|-------|
    | 方框 | `d-box`（白）、`d-gray`、`d-rose`（重點）、`d-sage`（正確 / 正向）、`d-butter`（輸入 / 參數）、`d-ink`（深色格） |
    | 文字 | 預設 14px；`d-sub`（12px 灰）、`d-b`（粗體）、`d-t-rose`、`d-t-sage`、`d-t-inv`（深色格上的字） |
    | 線條 | `d-line`、`d-line-rose`、`d-line-sage`，虛線再加 `d-dash`；框選用 `d-win` |
    | 箭頭 | `<marker>` 裡的 path 用 `d-head`、`d-head-rose`、`d-head-sage` |
    | 圓點 | `d-dot-rose`、`d-dot-sage` |

  - 每個 `<marker>` 的 `id` 要加上檔案專屬前綴（例如 `h-bp-s`），避免同一頁多張圖時互相衝突。
  - 圖上的數字必須和頁面內文的計算**完全一致**，也要追得回 `raw/`。
  - 字不要壓在線上；同一張圖最多 3 種顏色，顏色要有意義（例如綠 = 正向 / 正確、粉 = 反向 / 重點）。
- 要加新的 class 時，先加在 `assets/style.css` 的 diagrams 區塊，再回來更新這張表。

---

## 6. 特殊檔案

### 6.1 `wiki/index.md` —— 目錄（內容導向）

網站的側欄、首頁卡片、搜尋都從這裡讀。**每次新增、改名、刪除頁面都要更新。**

```markdown
## 概念
- [[artificial-intelligence]] — 一行摘要
## 來源
- [[src-wikipedia-ai]] — 一行摘要
```

- 只有兩個分區：`## 概念`（→ `concepts/`）、`## 來源`（→ `sources/`）。
- 每行格式固定：`- [[slug]] — 摘要`。
- **概念區的順序 = 建議閱讀順序**（由淺到深），首頁會照這個順序排學習路線。

### 6.2 `wiki/log.md` —— 維護紀錄（時間導向）

只往**最上方**加新紀錄，不刪舊紀錄。標題前綴固定，方便用 `grep "^## \[" wiki/log.md` 查：

```markdown
## [2026-11-17] ingest | Google 機器學習速成課程：損失函數
- 新增：[[src-google-loss]]、[[loss-function]]
- 更新：[[optimization]]（補上損失曲線）
```

動作只用：`setup`、`ingest`、`query`、`lint`、`update`（改善既有頁面，例如加圖、改寫說明）。

---

## 7. 工作流程

### 7.1 Ingest（收錄）—— 使用者說「收錄 raw/xxx.md」或「幫我找 ○○ 的資料收進來」
1. 如果是請 AI 找資料：從**可信的公開來源**（維基百科、大學課程、官方文件、論文）剪輯重點，
   存成 `raw/` 檔，檔案開頭寫明網址、出處、收錄日期，並註明「重點摘錄，非全文」。
2. 讀 raw 檔，先跟使用者**簡短報告重點**，再動手寫。
3. 建立來源頁 `wiki/sources/src-*.md`。
4. 更新或新建相關概念頁；一份來源通常會動到好幾頁。在概念頁的「來源」補上這份來源頁。
   新的概念頁在「動手算一次」依 5.4 畫一張講解圖。
5. 補齊雙向的 `[[ ]]` 連結。
6. 更新 `wiki/index.md`，在 `wiki/log.md` 最上方加紀錄。

### 7.2 Query（提問）
1. 先讀 `wiki/index.md` 找相關頁，再讀頁面回答，並註明引用哪些頁。
2. 好的回答（比較表、整理、新觀點）詢問使用者後，存成新的概念頁，讓知識累積。
3. 在 log 記一筆 `query`。

### 7.3 Lint（健康檢查）—— 使用者說「檢查 wiki」
檢查並修正：
- `index.md` 有列但檔案不存在，或有檔案但沒列入
- 壞連結（`[[ ]]` 指向不存在的 slug）
- 孤兒頁（沒有任何頁面連過來）
- 被多頁提到、卻還沒有自己頁面的概念
- 頁面之間說法矛盾；新來源推翻了舊說法
- 概念頁缺少 5.1 規定的段落
- 值得補充的資料缺口（建議使用者可以找什麼來源）

完成後在 log 記一筆 `lint`。

### 7.4 Slides（產生教學簡報）—— 使用者說「用 wiki 做簡報」或「更新簡報」
流程圖見 `slides/graph.svg`，設計理由見 `slides/WORKFLOW.md`。
1. **B 查詢**：`python slides/pipeline/query_wiki.py` → 讀 `slides/build/context.md`（資料包，最上面是規則與字數上限）。
2. **C 整理**：只根據資料包改 `slides/outline.json`。每張都要有 `sources`；新術語寫進 `defines`；封面、路線圖標 `preview`。
3. **D 檢查**：`python slides/pipeline/check_outline.py --round-note "這輪改了什麼"`。
   - 有錯 → 依錯誤碼退回：多數退回 C，**只重寫錯的那幾張**；`UNVERIFIED` 退回 7.1 先收錄來源再重跑 B。
   - 最多 3 輪；還不通過就停下來跟使用者說明。
4. **E 產生**：`python slides/pipeline/build_slides.py` → `slides/index.html`。
5. **F 版面**：本機預覽 `/slides/`，在主控台跑 `__checkLayout()` 要回傳 `[]`；桌機 1280×760 與手機 375 寬逐張看過。
   樣式問題改 `slides/pipeline/template.html` 重跑 E；內容問題（例如圖文不符）退回 C。
6. 同一種錯誤反覆出現時，把它變成 `rules.json` 的提示（往前移到 B）或 `check_outline.py` 的新規則（從 F 移到 D），並在 `WORKFLOW.md` 記下原因。
7. 在 `wiki/log.md` 記一筆 `query`（簡報是對 wiki 的一次提問）。

---

## 8. 網站與風格（韓系風）

- **純靜態、沒有建置步驟**。Markdown 用 CDN 的 `marked@12.0.2` 在瀏覽器渲染；外部函式庫一律固定版本號。
- 風格關鍵字：**柔和、留白、圓角、溫暖**
  - 底色：暖象牙白；主色：乾燥玫瑰粉；輔色：鼠尾草綠、奶油黃
  - 大圓角卡片（16～24px）、極淡陰影、細線分隔
  - 字體：Noto Sans TC（細、字距略寬）＋ Quicksand（英文小標）
  - 每頁頂端有英文小標（eyebrow），例如 `CONCEPT · 01`
  - 支援深色模式（暖炭灰底，粉色變柔和）
- 顏色只能用 `assets/style.css` 裡 `:root` 定義的 CSS 變數。
- 版面：左側欄（搜尋 + 目錄）、右側內文、文末自動產生「反向連結」；手機寬度時側欄收合成選單。
- 要改網站功能時，**先跟使用者說明要改什麼**再動手。
- 改了 `style.css` 或 `app.js`，要把 `index.html` 裡的 `?v=日期` 改成當天日期，避免瀏覽器用到舊的快取。

### 本機預覽
```bash
python -m http.server 8000
```
開啟 <http://localhost:8000>。直接雙擊 `index.html` 讀不到 Markdown，一定要用本機伺服器。

---

## 9. AI 必守規則（摘要）

1. **不修改 `raw/`**；所有事實都要追得回 raw。
2. 每次增刪改頁面：同步更新 `wiki/index.md`，並在 `wiki/log.md` 最上方留紀錄。
3. 只用 `[[slug]]` 互連；完成後確認沒有壞連結和孤兒頁。
4. 遵守第 4 節命名、第 5 節頁面格式（含 frontmatter）。
5. 繁體中文、講解口吻、自己的話、**不捏造**。
6. 不加建置工具或框架。
7. 完成後用本機伺服器預覽，確認新頁面能正常顯示、連結都能點。
