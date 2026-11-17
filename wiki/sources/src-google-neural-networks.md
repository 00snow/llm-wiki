---
title: Google ML 速成課程：神經網路與激勵函數
type: source
tags: [基礎]
updated: 2026-11-17
---

# Google ML 速成課程：神經網路與激勵函數

- **原始檔**：`raw/2026-11-17-google-神經網路與激勵函數.md`
- **網址**：<https://developers.google.com/machine-learning/crash-course/neural-networks/nodes-hidden-layers>
- **作者 / 出處**：Google for Developers, Machine Learning Crash Course（兩個章節）
- **收錄日期**：2026-11-17

## 這份資料在講什麼
說明神經網路的輸入層、隱藏層、輸出層，以及為什麼一定要有激勵函數，並介紹 sigmoid、tanh、ReLU。

## 重點
- 神經元 = 上一層的加權總和 + 偏差，再過激勵函數。
- 權重和偏差是參數；3 輸入的線性模型有 4 個參數，加一層 4 個神經元變 21 個。
- 只疊線性計算，結果仍是線性的，所以需要激勵函數。
- ReLU = max(0, x)：計算簡單、比較不會梯度消失，建議先用。

## 用在哪些頁
- [[neural-network]]
