# 課堂筆記：LLM 與 Transformer

- **類型**：課堂筆記
- **原始檔**：`raw/2026-11-02-課堂筆記-LLM與Transformer.md`
- **日期**：2026-11-02

## 摘要
這堂課從「LLM 其實只是在預測下一個 token」出發，說明文字如何被切成 token、轉成向量，
再交給 Transformer 處理。重點放在自注意力機制如何讓每個 token 參考整段上下文，
最後介紹訓練的三個階段，以及模型為什麼會產生幻覺。

## 學到的重點
- 生成 = 不斷重複「預測下一個 token」。
- token 不等於字；中文通常比英文花更多 token。
- Transformer 靠自注意力平行處理整段文字，比 RNN 更容易放大規模。
- 訓練三階段：預訓練 → 指令微調 → RLHF。
- context window 限制模型一次能看的長度；temperature 控制隨機程度。
- 模型追求的是「看起來合理」，不是「一定正確」，所以會幻覺。

## 延伸到的概念
- [[large-language-model]]
- [[tokenization]]
- [[transformer]]
- [[attention]]
- [[hallucination]]
