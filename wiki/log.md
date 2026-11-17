# 維護紀錄

> 新的紀錄寫在最上面，不刪舊紀錄。查最近 5 筆：`grep "^## \[" wiki/log.md | head -5`

## [2026-11-17] ingest | Stanford CS231n：反向傳播
- 起因：上次 lint 發現 [[optimization]] 的「反向傳播」標著（待查證），依 `AGENTS.md` 7.1 找來源補上
- 新增：`raw/2026-11-17-cs231n-反向傳播.md`、[[src-cs231n-backprop]]、[[backpropagation]]（排在學習路線第 05 頁）
- 更新：[[optimization]]（移除待查證、改連到反向傳播、來源 +1）、[[neural-network]]（「接下來讀什麼」加入反向傳播）
- 更新：[[index|目錄]]、[[home|首頁]]的主題關係圖
- 剩下的資料缺口：分類用的「交叉熵」損失（[[loss-function]]）

## [2026-11-17] lint | 建站後第一次檢查
- 6 個概念頁、7 個來源頁都已列入 [[index|目錄]]
- 沒有壞連結、沒有孤兒頁
- 資料缺口：分類用的「交叉熵」損失、神經網路的「反向傳播」還沒有來源，已在 [[loss-function]]、[[optimization]] 標註（待查證）

## [2026-11-17] ingest | Stanford CS231n：卷積神經網路
- 新增：[[src-cs231n-cnn]]、[[cnn]]

## [2026-11-17] ingest | 維基百科：卷積
- 新增：[[src-wikipedia-convolution]]、[[convolution]]
- 更新：[[cnn]]（補上「實際上是互相關」的說明）

## [2026-11-17] ingest | Google ML 速成課程：梯度下降與超參數
- 新增：[[src-google-gradient-descent]]、[[optimization]]

## [2026-11-17] ingest | Google ML 速成課程：損失
- 新增：[[src-google-loss]]、[[loss-function]]

## [2026-11-17] ingest | Google ML 速成課程：神經網路與激勵函數
- 新增：[[src-google-neural-networks]]、[[neural-network]]

## [2026-11-17] ingest | 維基百科：人工智慧
- 新增：[[src-wikipedia-ai]]、[[artificial-intelligence]]
- 更新：[[neural-network]]、[[cnn]]（補上歷史年份）

## [2026-11-17] setup | 依 Karpathy LLM Wiki 重建專案
- 收錄 [[src-karpathy-llm-wiki]]，依它改寫 `AGENTS.md`（主要規則）與 `CLAUDE.md`（匯入 AGENTS.md）
- 目錄改用 `wiki/index.md`、紀錄改用固定前綴 `## [日期] 動作 | 標題`
- 主題改為「AI 入門講解」；網站改成韓系風樣式
- 移除先前由 AI 自行編寫的範例筆記（不是真實資料）
