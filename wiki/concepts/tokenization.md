# 斷詞與 Token（Tokenization）

> 把文字切成模型能處理的小單位（token），再轉成編號與向量的過程。

## 重點
- token 不等於「字」也不等於「單字」，而是由演算法學出來的常見片段。
- 英文常見單字可能是 1 個 token，罕見字會被拆成好幾塊。
- 中文一個字常是 1～2 個 token，同樣內容通常比英文用更多 token。
- 計費、context window 都是用 **token 數** 計算。
- 每個 token 會被轉成一個向量，稱為 **embedding**。

## 說明
模型只會處理數字。Tokenizer 先依照一份「詞表（vocabulary）」把文字切塊，
每一塊對應一個整數編號；接著模型用 embedding 表把編號換成高維向量，
這些向量才是 [[transformer]] 真正運算的對象。

常見的切法是 **BPE（Byte Pair Encoding）**：從單一字元開始，
反覆把最常一起出現的片段合併成新的 token，直到詞表夠大。

## 例子

```
輸入：  I love unbelievable cats
token： [I] [ love] [ un] [believ] [able] [ cats]
```

（實際切法依每個模型的 tokenizer 而不同，這裡只是示意。）

## 相關概念
- [[large-language-model]]：tokenization 是 LLM 處理文字的第一步
- [[transformer]]：接收 token 向量進行運算
- [[rag]]：檢索時同樣會把文件轉成 embedding

## 來源
- [[2026-11-02-class-llm-transformer]]
