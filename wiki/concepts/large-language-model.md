# 大型語言模型（Large Language Model, LLM）

> 用海量文字訓練出來、能根據上文一個一個預測下一個 token 的神經網路。

## 重點
- 核心任務只有一個：**預測下一個 token**，重複這件事就能寫出整段文字。
- 現代 LLM 幾乎都採用 [[transformer]] 架構。
- 輸入的文字會先經過 [[tokenization]] 切成 token。
- 一次能處理的長度受 **context window** 限制。
- 因為追求「看起來合理」，可能產生 [[hallucination]]。

## 說明
LLM 不是查資料庫，而是把訓練資料中的規律壓縮進數十億個參數裡。
當你輸入一句話，模型會算出「下一個 token 是什麼」的機率分布，挑一個輸出，
再把它接回輸入，繼續預測下一個——這個過程叫做 **自回歸生成（autoregressive generation）**。

### 訓練三階段

| 階段 | 做什麼 | 得到什麼 |
|------|--------|----------|
| 預訓練（Pre-training） | 讀大量文字，練習預測下一個 token | 會「接話」的基礎模型 |
| 指令微調（Instruction tuning） | 用「指令 → 好回答」的範例再訓練 | 會照指示回答的助理 |
| RLHF | 依人類對回答的偏好調整 | 更有幫助、更安全的回答 |

### 常見參數
- **temperature**：越高越隨機、越有創意；越低越穩定、可重複。
- **context window**：模型一次能「看見」的 token 上限，超過的部分會被忽略。

## 例子
輸入「台灣最高的山是」，模型會發現「玉」的機率最高，輸出後再預測下一個 token「山」，
接著可能是「，海拔約…」。每一步都只是在選下一個最合適的 token。

## 相關概念
- [[tokenization]]：LLM 看到的不是字，而是 token
- [[transformer]]：LLM 使用的神經網路架構
- [[prompt-engineering]]：如何下指令讓 LLM 表現更好
- [[hallucination]]：LLM 最常見的問題

## 來源
- [[2026-11-02-class-llm-transformer]]
