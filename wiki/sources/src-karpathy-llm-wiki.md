---
title: Karpathy：LLM Wiki
type: source
tags: [方法論]
updated: 2026-11-17
---

# Karpathy：LLM Wiki

- **原始檔**：`raw/2026-11-17-karpathy-llm-wiki.md`
- **網址**：<https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>
- **作者 / 出處**：Andrej Karpathy（GitHub Gist）
- **收錄日期**：2026-11-17

## 這份資料在講什麼
一份「概念檔」，描述怎麼讓 LLM 維護一份個人知識庫。重點是讓知識**累積**：與其每次提問都重新檢索原始文件，不如讓 AI 事先把資料整理成互相連結的 wiki。**這個網站的結構就是照它設計的。**

## 重點
- 三層：raw（原始資料，只讀）、wiki（AI 寫的頁面）、schema（規則檔，本站是 `AGENTS.md`）。
- 三個操作：ingest（收錄）、query（提問）、lint（健康檢查）。
- 兩個特殊檔：`index.md`（內容目錄）、`log.md`（時間紀錄，固定前綴方便搜尋）。
- 一份來源常常會動到很多頁；好的問答結果也應該存回 wiki。
- 它是刻意抽象的「模式」，要依自己的主題調整。

## 用在哪些頁
- [[home|首頁・關於本站]]
- [[index|目錄]]
