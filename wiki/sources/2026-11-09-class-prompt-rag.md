# 課堂筆記：Prompt 與 RAG

- **類型**：課堂筆記
- **原始檔**：`raw/2026-11-09-課堂筆記-Prompt與RAG.md`
- **日期**：2026-11-09

## 摘要
這堂課談「怎麼把 LLM 用好」。前半段整理寫 prompt 的技巧；後半段介紹 RAG，
讓模型先查資料再回答。最後提出 LLM Wiki 的想法：與其每次重新檢索，
不如讓 LLM 把資料整理成一份會持續累積的 wiki——也就是這個網站的由來。

## 學到的重點
- 好的 prompt 要交代角色、任務、限制與輸出格式；few-shot 範例很有效。
- 「一步一步想」常能提升推理題的正確率。
- RAG：切塊 → embedding → 檢索最相近的段落 → 放進 prompt 生成答案。
- RAG 可以引用來源、更新資料不必重新訓練，但檢索錯了就會答錯。
- LLM Wiki 分 raw / wiki / 規則檔三層，靠 ingest、query、lint 三個動作維護。

## 延伸到的概念
- [[prompt-engineering]]
- [[rag]]
- [[hallucination]]
- [[llm-wiki]]
