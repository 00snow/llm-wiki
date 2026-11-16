# CLAUDE.md — LLM 學習 Wiki

> 這份文件是給 AI 協作者（Claude Code、Codex、Cursor…）看的專案規則。
> 開始任何工作前，請**完整讀完**本文件。`AGENTS.md` 只是指向這裡的入口。

---

## 1. 專案目的

這是一個「**LLM Wiki**」：一個由 AI 持續維護、以 Markdown 寫成、互相連結的個人知識庫，
主題是「**大型語言模型（LLM）基礎知識**」。

運作概念分三層：

| 層 | 資料夾 | 誰寫 | 說明 |
|----|--------|------|------|
| 原始資料 | `raw/` | 人類 | 課堂筆記、文章摘錄、心得。**AI 只讀不改。** |
| 知識庫 | `wiki/` | AI | 把原始資料整理成「概念頁」與「來源頁」，彼此交叉連結。 |
| 網站 | `index.html` + `assets/` | AI（很少改） | 在瀏覽器把 `wiki/` 的 Markdown 即時渲染成網頁，部署在 GitHub Pages。 |

人類負責「丟資料進 `raw/`、提問題」；AI 負責「整理、連結、保持一致」。
**新增內容 = 新增 / 修改 Markdown + 更新 `wiki/pages.json`，不需要寫 HTML。**

---

## 2. 資料夾結構

```
.
├── CLAUDE.md            ← 本文件（規則）
├── AGENTS.md            ← 指向 CLAUDE.md
├── README.md            ← 給人類看的介紹
├── index.html           ← 網站唯一的 HTML（單頁應用，hash 路由）
├── .nojekyll            ← 讓 GitHub Pages 不經過 Jekyll
├── assets/
│   ├── style.css        ← 全站樣式
│   └── app.js           ← 讀 pages.json、渲染 Markdown、wiki 連結、反向連結、搜尋
├── raw/                 ← 原始資料（人類寫，AI 唯讀）
│   └── YYYY-MM-DD-簡短描述.md
└── wiki/
    ├── pages.json       ← ★ 所有頁面的清單（網站靠它運作）
    ├── home.md          ← 首頁導言
    ├── log.md           ← 維護紀錄（append-only）
    ├── concepts/        ← 概念頁：一個概念一頁
    │   └── <slug>.md
    └── sources/         ← 來源頁：一份 raw 資料對應一頁摘要
        └── <slug>.md
```

---

## 3. 命名規則

- **slug** 一律用小寫英文 + 連字號：`transformer`、`prompt-engineering`、`rag`。
  不要用中文、空白、底線或大寫。
- 概念頁路徑：`wiki/concepts/<slug>.md`；來源頁路徑：`wiki/sources/<slug>.md`。
- 來源頁的 slug 用 `YYYY-MM-DD-主題`，例如 `2026-11-02-class-transformer`。
- `raw/` 檔名：`YYYY-MM-DD-簡短描述.md`（可以有中文）。
- 同一個 slug 在整個 wiki 中**必須唯一**（概念與來源之間也不能重複）。

---

## 4. 頁面格式

### 4.1 概念頁（`wiki/concepts/<slug>.md`）

```markdown
# 概念名稱（English Name）

> 一句話定義：用一句話說清楚它是什麼。

## 重點
- 3～6 條條列重點，每條一兩句。

## 說明
用自己的話解釋，可分小段。需要時用表格或程式碼區塊。

## 例子
至少一個具體例子。

## 相關概念
- [[other-slug]]：一句話說明兩者的關係

## 來源
- [[source-slug]]
```

### 4.2 來源頁（`wiki/sources/<slug>.md`）

```markdown
# 來源標題

- **類型**：課堂筆記 / 文章 / 影片 / 論文
- **原始檔**：`raw/檔名.md`
- **日期**：YYYY-MM-DD

## 摘要
3～5 句話。

## 學到的重點
- 條列

## 延伸到的概念
- [[concept-slug]]
```

### 4.3 寫作規則

- 語言：**繁體中文**，專有名詞第一次出現時附英文，例如「注意力機制（Attention）」。
- 頁面之間用 **wiki 連結** `[[slug]]` 互連；要顯示不同文字用 `[[slug|顯示文字]]`。
  不要寫成 `[x](concepts/x.md)` 這種相對路徑。
- 每個概念頁至少要有 **2 個** 指向其他頁的 `[[ ]]` 連結，避免孤兒頁。
- `#` 標題只用一次（頁面標題），內文從 `##` 開始。
- 用自己的話改寫，**不要大段複製**原始資料或網路文章。
- 不確定的內容寫「（待確認）」，不要捏造數字或引用。

---

## 5. `wiki/pages.json` 格式

網站的導覽、搜尋、分類全部依賴這個檔案。**新增、改名、刪除頁面時一定要同步更新。**

```json
{
  "slug": "transformer",
  "title": "Transformer",
  "type": "concept",          // "concept" 或 "source"
  "path": "concepts/transformer.md",  // 相對於 wiki/
  "summary": "一句話摘要（會顯示在卡片與搜尋結果）",
  "tags": ["架構"],
  "updated": "2026-11-16"
}
```

- 陣列依 `type` 分組，組內依 `title` 排序。
- `home.md` 與 `log.md` 不列在 `pages.json`（它們是固定頁，路由 `#/home`、`#/log`）。
- 可用的 tags（新增 tag 前先看能不能沿用）：`基礎`、`架構`、`訓練`、`應用`、`方法論`、`課堂`。

---

## 6. 三種工作流程

### 6.1 Ingest（收錄新資料）—— 使用者說「把 raw/xxx.md 收進 wiki」
1. 讀 `raw/` 中的檔案（**不要修改它**）。
2. 建立一個來源頁 `wiki/sources/<日期-主題>.md`。
3. 找出資料中的概念：
   - 已有概念頁 → **補充**內容、在「來源」加上這個來源頁。
   - 沒有概念頁 → 依 4.1 格式**新建**。
4. 檢查相關頁面，補上雙向的 `[[ ]]` 連結。
5. 更新 `wiki/pages.json`（新增項目、修改 `updated` 日期）。
6. 在 `wiki/log.md` **最上方**加一筆紀錄（格式見 6.4）。

### 6.2 Query（提問）—— 使用者問問題
- 先讀 `wiki/pages.json` 找相關頁，再讀頁面內容回答，回答中註明引用哪些頁。
- 如果答案有保存價值，詢問使用者是否要存成新的概念頁。

### 6.3 Lint（健康檢查）—— 使用者說「檢查 wiki」
檢查並修正：
- `pages.json` 有列但檔案不存在，或檔案存在但沒列。
- 指向不存在 slug 的 `[[ ]]` 連結（壞連結）。
- 沒有任何頁面連過來的孤兒頁。
- 概念頁缺少 4.1 規定的段落。
- 頁面之間說法矛盾。
最後在 `log.md` 記錄這次檢查的結果。

### 6.4 `log.md` 紀錄格式（新的寫在最上面）

```markdown
## 2026-11-16 · ingest · 課堂筆記：Transformer
- 新增：[[2026-11-02-class-transformer]]、[[attention]]
- 更新：[[transformer]]（補充多頭注意力）
```

---

## 7. 網站與樣式

- 純靜態，**沒有建置步驟**、沒有 npm。`index.html` 透過 CDN 載入 `marked` 渲染 Markdown。
- 外部函式庫只能用 CDN 且**固定版本號**（例如 `marked@12.0.2`）。
- 風格：簡潔的「筆記本」感——米白底、深灰字、單一強調色（墨綠 `--accent`），支援深色模式。
  顏色只能用 `assets/style.css` 中 `:root` 定義的 CSS 變數，不要在 Markdown 裡寫行內樣式。
- 版面：左側邊欄（搜尋 + 頁面清單）、右側內文、文末自動顯示「反向連結」。手機寬度時側欄收合。
- 一般新增內容**不需要改** `index.html`、`app.js`、`style.css`。要改網站功能時，先說明要改什麼再動手。

### 本機預覽
```bash
python -m http.server 8000
# 開啟 http://localhost:8000
```
（直接雙擊 `index.html` 會因瀏覽器限制讀不到 Markdown，必須用本機伺服器。）

---

## 8. AI 必須遵守的規則（摘要）

1. **不修改 `raw/`**。
2. 每次新增 / 改名 / 刪除頁面，**同步更新 `pages.json`**，並在 `log.md` 留紀錄。
3. 只用 `[[slug]]` 互連；新增頁面後確認沒有壞連結。
4. 遵守第 3 節命名、第 4 節頁面格式。
5. 繁體中文、自己的話、不捏造。
6. 不新增建置工具或框架；保持「打開就能跑」的純靜態網站。
7. 完成後用本機伺服器預覽，確認新頁面能正常顯示、連結可點。
