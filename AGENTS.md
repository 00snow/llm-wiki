# AGENTS.md

本專案的完整 AI 協作規則寫在 [`CLAUDE.md`](./CLAUDE.md)，請先閱讀它再開始任何工作。

最重要的幾條：

1. `raw/` 是人類的原始資料，**只讀不改**。
2. 知識內容寫在 `wiki/`（Markdown），頁面之間用 `[[slug]]` 連結。
3. 新增 / 改名 / 刪除頁面時，同步更新 `wiki/pages.json`，並在 `wiki/log.md` 最上方留紀錄。
4. 繁體中文、用自己的話、不捏造。
5. 純靜態網站，不加建置工具；用 `python -m http.server` 預覽。
