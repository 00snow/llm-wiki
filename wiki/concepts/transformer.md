# Transformer

> 2017 年提出、以注意力機制為核心的神經網路架構，是現代 LLM 的基礎。

## 重點
- 出自論文〈Attention Is All You Need〉（2017）。
- 核心元件是 **自注意力**（見 [[attention]]），讓每個 token 能參考整段上下文。
- 可以**平行處理**整段序列，比逐字處理的 RNN 更容易訓練、更容易放大。
- 由很多層「注意力 + 前饋網路」堆疊而成，層數越多模型通常越強。
- GPT 類的 LLM 只使用 Transformer 的 **decoder** 部分。

## 說明
在 Transformer 之前，處理文字主要用 RNN：一次讀一個字，把記憶傳給下一步。
這樣不但慢，句子一長前面的資訊就容易被忘掉。

Transformer 改成一次看整段文字。每一層做兩件事：
1. **注意力層**：每個 token 決定要從其他 token 拿多少資訊。
2. **前饋層**：對每個 token 各自做進一步的轉換。

另外還有 **位置編碼（positional encoding）**，因為一次看全部時，
模型本身不知道誰在前、誰在後，需要額外告訴它順序。

## 例子
句子「銀行旁邊的河岸很美」中的「岸」，經過幾層注意力後，
它的向量會吸收「河」的資訊，讓模型知道這裡的「岸」和「銀行」無關。

## 相關概念
- [[attention]]：Transformer 最核心的機制
- [[tokenization]]：Transformer 的輸入是 token 向量
- [[large-language-model]]：建立在 Transformer 之上

## 來源
- [[2026-11-02-class-llm-transformer]]
