# Karpathy：LLM Wiki（idea file）

- 網址：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- 作者：Andrej Karpathy（GitHub Gist，2026 年 4 月）
- 收錄日期：2026-11-17
- 說明：AI 從原文整理的重點摘錄，非全文。

## 重點摘錄
- 核心想法：不是每次提問都從原始文件檢索（RAG），而是讓 LLM 逐步建立並維護一份持續存在、互相連結的 Markdown wiki，知識「編譯一次、持續更新」。
- 三層：
  1. Raw sources：人挑選的原始文件（文章、論文、圖片、資料），LLM 只讀不改，是事實依據。
  2. Wiki：LLM 產生的 Markdown，包含摘要、實體頁、概念頁、比較、總覽；LLM 負責建立、更新、交叉引用，人負責閱讀。
  3. Schema：設定文件（例如 CLAUDE.md 或 AGENTS.md），定義 wiki 結構、慣例、工作流程，由人和 LLM 一起持續修改。
- 三個操作：
  - Ingest：放入新來源 → LLM 讀、討論重點、寫摘要頁、更新 index、更新相關頁、在 log 加紀錄。一份來源可能動到 10～15 頁；作者偏好一次收錄一份並在旁監督。
  - Query：LLM 先讀 index 找相關頁，讀完後給出附引用的答案；好的答案可以存回 wiki，讓探索也能累積。
  - Lint：定期檢查矛盾、被新來源推翻的舊說法、沒有連入連結的孤兒頁、缺少獨立頁面的概念、缺少的交叉引用、可用網路搜尋補上的資料缺口。
- 特殊檔案：
  - index.md：內容導向的目錄，每頁一行（連結 + 一行摘要 + 可選的日期、來源數），依類別分組；每次收錄都更新，查詢時先讀它。
  - log.md：時間導向、只往後加的紀錄；建議每筆用固定前綴，例如 `## [2026-04-02] ingest | Article Title`，方便用 grep 解析。
- 可選 YAML frontmatter（tags、日期、來源數）。
- 工具：用 Obsidian 瀏覽、Obsidian Web Clipper 把網頁轉成 Markdown、圖片放固定資料夾如 raw/assets/、wiki 本身是 git repo。
- 這是刻意抽象的「模式」，不是固定實作；資料夾結構與格式都應依主題調整。
