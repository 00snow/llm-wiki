---
title: Google ML 速成課程：梯度下降與超參數
type: source
tags: [訓練]
updated: 2026-11-17
---

# Google ML 速成課程：梯度下降與超參數

- **原始檔**：`raw/2026-11-17-google-梯度下降與超參數.md`
- **網址**：<https://developers.google.com/machine-learning/crash-course/linear-regression/gradient-descent>
- **作者 / 出處**：Google for Developers, Machine Learning Crash Course（兩個章節）
- **收錄日期**：2026-11-17

## 這份資料在講什麼
說明梯度下降的步驟、損失曲線與收斂，以及學習率、批次大小、epoch 這些超參數怎麼影響訓練。

## 重點
- 梯度下降：算損失 → 看斜率 → 往下坡走一小步 → 重複。
- 新值 = 舊值 − 學習率 × 斜率。
- 學習率太小收斂很慢，太大會讓損失亂跳、無法收斂。
- SGD 每次看 1 筆、小批次每次看一小批、全批次每次看全部。
- 1 個 epoch = 全部資料看過一次。

## 用在哪些頁
- [[optimization]]
