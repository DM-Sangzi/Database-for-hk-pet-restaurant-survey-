# Analysis Guide

Working conventions for anyone who cleans, updates or re-analyses the survey data in this repository. Written after the first full analysis pass, so most of the rules below come from problems we actually ran into.

---

## 1. Data files

| File | Encoding | Shape | Notes |
|---|---|---|---|
| `data/survey_a_main_144.csv` | `utf-8-sig` | 144 × 16 | Main survey. Part 3 (last 3 columns) only has ~89 responses. |
| `data/survey_b_followup_63.csv` | `utf-8-sig` | 63 × 6 | Follow-up survey. Independent sample. |

Always read with `encoding='utf-8-sig'`. Plain `utf-8` leaves a BOM on the first column name and breaks column lookup.

If the file arrives as a `.zip`, read it in memory rather than extracting:

```python
import io, zipfile, pandas as pd
z = zipfile.ZipFile(path)
df = pd.read_csv(io.BytesIO(z.read(z.namelist()[0])), encoding='utf-8-sig')
```

## 2. Cleaning rules

1. **Trim every string column** before counting. Google Forms exports sometimes carry trailing spaces and line breaks inside answers.
2. **Drop empty answers** from the base, but report them. An empty cell is missing data, not zero.
3. **Never overwrite the raw file.** All cleaning happens in the script; the CSV stays as exported.
4. **Check that single-choice totals equal the response count.** If A1 sums to 144 but A2 sums to 143, one respondent skipped A2 — say so in the figure caption (`n = 143`).

## 3. Counting conventions

**Single-choice questions** — percentage of respondents who answered.

**Multi-select questions** (answers separated by `;`) — split on `;`, count each option, and divide by the number of **respondents**, not the number of selections. This is why multi-select percentages can add up to more than 100% and should never be shown as a pie chart.

```python
items = []
for row in df[col].dropna().astype(str):
    items.extend([x.strip() for x in row.replace('；', ';').split(';') if x.strip()])
```

**n must be printed in every figure title.** Readers need to know whether a percentage is based on 144 people or on the 89 who reached Part 3.

## 4. Known pitfalls

### 4.1 Substring trap in the pet-ownership question

The options are:

- `目前沒有飼養寵物`
- `有飼養寵物，但從未帶寵物進入餐廳`
- `有飼養寵物，亦曾帶寵物進入餐廳`

`'有飼養' in '目前沒有飼養寵物'` is **True**, so a careless `str.contains('有飼養')` labels every respondent as a pet owner. Use a start-anchored match instead:

```python
is_owner = a1.str.strip().str.startswith('有飼養')
```

This bug silently flipped the entire cross-tabulation during the first pass.

### 4.2 Two independent samples

Dataset A (144) and Dataset B (63) are **not** one sample split in two. Do not merge them, do not pool their percentages, and do not weight one against the other. Report them side by side.

Note also that the same measure question appears in both datasets with *different rankings* (entrance rules lead in A, public education leads in B). That difference is a finding, not an error.

### 4.3 Part 3 has a smaller base

Q11–Q13 of Dataset A were answered by 89, 88 and 86 respondents respectively. Percentages there must use those bases, never 144.

### 4.4 Inconsistent five-point scales

A2 uses support/oppose wording, Q9 and Q10 use agree/disagree wording. Do not combine them into a single "positive attitude" score without stating the mapping explicitly.

## 5. Figure conventions

- English labels only — the report is written in English.
- Horizontal bars for distributions; grouped bars for comparisons; **no pie charts for multi-select**.
- One accent colour per figure, with the highest value in the darkest shade.
- Percentages labelled directly at the bar end, one decimal place.
- `n` stated in the title.
- Export at 220 dpi, white background, no chart borders.

## 6. When new responses arrive

1. Re-export the CSV from Google Forms and replace the file in `data/`.
2. Re-run `scripts/verify_data.py` and compare the totals with the previous run.
3. Re-run `scripts/make_charts.py`.
4. Update the response count in the README and in every `n` in the figures and report.

## 7. Pre-submission checklist

- [ ] Every percentage has a stated base.
- [ ] Single-choice totals equal the response count, or the gap is explained.
- [ ] Multi-select percentages use respondents as the base.
- [ ] Pet-owner grouping uses `startswith`, not `contains`.
- [ ] Dataset A and B are reported separately.
- [ ] Figure numbers follow the order in which they appear in the report.
- [ ] No personal names or reflections are committed to the repository.
