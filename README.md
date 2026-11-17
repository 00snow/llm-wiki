# AI 入門講解 Wiki

🌸 網站：<https://00snow.github.io/llm-wiki/>

一個參考 [Karpathy 的 LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 做法、由 AI 維護的知識庫。
主題是「走向 LLM 研究之前要先懂的 AI 基礎」，寫成可以講給初學者聽的講義：

01 什麼是 AI → 02 神經網路 → 03 損失函數 → 04 最佳化 → 05 卷積 → 06 CNN

## 結構

| 層 | 位置 | 說明 |
|----|------|------|
| 原始資料 | `raw/` | 從維基百科、Stanford CS231n、Google ML 速成課程剪輯的重點，附原始網址 |
| 知識庫 | `wiki/` | AI 整理的講解頁（`concepts/`）與來源摘要（`sources/`），目錄 `index.md`、紀錄 `log.md` |
| 規則 | `AGENTS.md` | 給 AI 看的規則；`CLAUDE.md` 直接匯入它 |

網站是純靜態單頁應用（`index.html` + `assets/`），在瀏覽器把 Markdown 渲染成韓系風網頁，
支援 `[[wiki 連結]]`、反向連結、學習路線、上一頁 / 下一頁、搜尋與深色模式。

## 本機預覽

```bash
python -m http.server 8000
```

開啟 <http://localhost:8000>。

## 怎麼繼續擴充

- 收錄新資料：「幫我找反向傳播的資料收進 wiki」或「收錄 raw/xxx.md」
- 提問：「MSE 和 MAE 什麼時候該用哪個？」——好的回答可以存回 wiki
- 健康檢查：「檢查 wiki」

AI 會依 `AGENTS.md` 的規則建立頁面、更新 `wiki/index.md`，並在 `wiki/log.md` 留紀錄。
