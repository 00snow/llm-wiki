---
title: Google ML 速成課程：損失
type: source
tags: [訓練]
updated: 2026-11-17
---

# Google ML 速成課程：損失

- **原始檔**：`raw/2026-11-17-google-損失函數.md`
- **網址**：<https://developers.google.com/machine-learning/crash-course/linear-regression/loss>
- **作者 / 出處**：Google for Developers, Machine Learning Crash Course
- **收錄日期**：2026-11-17

## 這份資料在講什麼
用線性迴歸的例子說明什麼是損失，比較 L1 / L2、MAE / MSE，以及離群值的影響。

## 重點
- 損失 = 預測和正確答案的距離；訓練目標是讓它最小。
- L1 取絕對值、L2 取平方；平方會放大大誤差。
- MSE 容易被離群值影響，MAE 比較穩。
- 例子：預測 23.1、實際 24 → L2 損失 0.81。

## 用在哪些頁
- [[loss-function]]
