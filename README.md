# LLM 學習 Wiki

一個由 AI 協助維護的「大型語言模型基礎知識」個人知識庫，採用 **LLM Wiki** 的做法：

- `raw/`：我自己的上課筆記（原始資料）
- `wiki/`：AI 依照規則整理出來、互相連結的 Markdown 頁面
- `CLAUDE.md` / `AGENTS.md`：給 AI 看的專案規則——AI 讀完就知道怎麼繼續擴充這個 wiki

網站是純靜態的單頁應用，瀏覽器直接把 `wiki/` 中的 Markdown 渲染成網頁，
支援 `[[wiki 連結]]`、反向連結、全文搜尋與深色模式。

## 本機預覽

```bash
python -m http.server 8000
```

然後開啟 <http://localhost:8000>。

## 新增內容

1. 把新筆記放進 `raw/`，檔名 `YYYY-MM-DD-描述.md`
2. 對 AI 說：「把 `raw/新檔名.md` 收進 wiki」
3. AI 會依 `CLAUDE.md` 建立來源頁與概念頁、更新 `wiki/pages.json` 和 `wiki/log.md`

## 部署

推送到 GitHub 後，在 **Settings → Pages** 選擇 `main` 分支的根目錄即可。
