# Data dictionary

Raw exports from Google Forms. Unmodified — all cleaning is done in `scripts/`.

## `survey_a_main_144.csv` — main survey (144 rows)

| # | Column (Chinese) | Meaning | Type |
|---|---|---|---|
| 0 | 时间戳记 | Submission timestamp | datetime |
| 1 | 基本背景 1. 您屬於以下哪一類人士？ | Pet ownership: `目前沒有飼養寵物` / `有飼養寵物，但從未帶寵物進入餐廳` / `有飼養寵物，亦曾帶寵物進入餐廳` | single choice |
| 2 | 2. 您對「容許狗隻進入餐廳」這項政策的整體態度 | Overall attitude, 5-point + `暫時未有足夠資訊判斷` | single choice |
| 3 | Q1 便溺或損壞公物的責任劃分 | Who cleans and pays | single choice |
| 4 | Q2 打架或影響他人用餐的責任 | Who is responsible for conflict | single choice |
| 5 | Q3 主人帶寵物入餐廳前應履行的責任 | Owner duties | **multi-select** |
| 6 | Q4 寵物主動靠近其他顧客時的反應 | Reaction to a pet approaching | single choice |
| 7 | Q5 寵物發出噪音時的處理 | Expected handling of noise | single choice |
| 8 | Q6 用餐時最令您顧慮的寵物問題 | Main concerns | **multi-select, max 2** |
| 9 | Q7 人寵餐具混用或交叉污染的疑慮 | Cross-contamination worry | single choice |
| 10 | Q8 對寵物掉毛或弄髒設施的接受程度 | Acceptance of hair and dirt | single choice |
| 11 | Q9 是否同意要求疫苗接種及基本社交能力 | Support for mandatory training | single choice |
| 12 | Q10 是否同意收取額外寵物友善費用 | Acceptance of extra fee | single choice |
| 13 | Q11 最能有效提升飼主責任的措施 | Effective measures | **multi-select, max 2**, n = 89 |
| 14 | Q12 飼主責任教育應從哪個階段開始 | Best stage for education | single choice, n = 88 |
| 15 | Q13 SPCA 計劃最希望包括的內容 | Desired scheme content | **multi-select, max 2**, n = 86 |

## `survey_b_followup_63.csv` — follow-up survey (63 rows)

| # | Column (Chinese) | Meaning | Type |
|---|---|---|---|
| 0 | 时间戳记 | Submission timestamp | datetime |
| 1 | 最能有效提升飼主責任的措施 | Effective measures | **multi-select, max 2** |
| 2 | 飼主責任教育應從哪個階段開始 | Best stage for education | single choice |
| 3 | SPCA 計劃最希望包括的內容 | Desired scheme content | **multi-select, max 2** |
| 4 | 違規投訴及跟進機制應包括甚麼 | Complaint and follow-up design | **multi-select, max 2** |
| 5 | 是否同意「加重罰款」比「教育宣傳」更有效 | Fines vs education, 1–5 scale | single choice |

## Notes

- Multi-select answers are stored in one cell, separated by `;`.
- Empty cells mean the respondent did not answer — treat as missing, not as zero.
- Column names contain line breaks and question numbers; address columns by position if the exact header is unstable.
- Datasets A and B are **independent samples** and must not be merged.
