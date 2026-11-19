# Database for HK Pet-Restaurant Survey

Survey-based data project on **public attitudes towards pets (especially dogs) in Hong Kong restaurants**, carried out as part of the MM3301SL Service Learning course.

The repository stores the cleaned survey data, the analysis scripts, the generated figures and the analysis conventions used by the team.

---

## 1. Project background

Hong Kong has been promoting a "pet economy", yet whether pets should be allowed into restaurants remains unsettled. Restaurant operators and policymakers have little evidence on what the public actually expects — who should clean up after a pet, what conditions should apply, how concerns differ between pet owners and non-owners.

This project answers those questions with two rounds of street surveys.

## 2. Data

Two linked questionnaires were collected face to face on the street. Both were built in Google Forms and exported as CSV.

| Dataset | Topic | Responses | Fieldwork dates | Locations |
|---|---|---|---|---|
| **A** – Main survey | Public acceptance of pet behaviour in restaurants (13 questions, 3 parts) | 144 | 23–24 Oct 2026 | Whampoa Promenade; West Kowloon waterfront (M+ / Hong Kong Palace Museum) |
| **B** – Follow-up survey | Owner responsibility and support measures (5 questions) | 63 | 6–7 Nov 2026 | The Mills, Tsuen Wan; West Kowloon (M+); Wan Chai pet-friendly promenade |

The two datasets are **independent samples**, not a subset and superset. They must be reported separately, each with its own `n`.

### Survey structure (Dataset A)

- **Part 1** — background (pet ownership) and overall attitude on a five-point scale.
- **Part 2** — Q1–Q10: cleaning and conflict responsibility, owner duties before entry (multi-select), reactions to pets approaching, noise handling, main concerns (up to 2 choices), cross-contamination worries, acceptance of hair and dirt, vaccination and training requirements, willingness to pay an extra fee.
- **Part 3** — Q11–Q13: measures to improve owner responsibility, best stage for responsibility education, content of an SPCA responsibility scheme. Only ~89 respondents reached this part.

## 3. Method

1. **Cleaning** — trim whitespace, drop blank answers, standardise option labels, check that single-choice totals match the response count.
2. **Descriptive statistics** — frequency and percentage for every question.
3. **Multi-select handling** — split answers on `;` and report each option as a share of *respondents*, so percentages can exceed 100% in total.
4. **Cross-tabulation** — split the sample by pet ownership to compare attitudes towards allowing pets and towards mandatory training.
5. **Visualisation** — horizontal bar charts for distributions and grouped bars for comparisons.

Detailed conventions and known pitfalls are documented in [docs/analysis_guide.md](docs/analysis_guide.md).

## 4. Key findings (summary)

- **51.7%** supported or strongly supported allowing dogs into restaurants; **24.5%** were neutral; **15.4%** opposed.
- **76.3%** placed cleaning and compensation responsibility on the owner; **65.3%** expected the owner to intervene immediately when a pet causes trouble.
- **77.8%** supported mandatory vaccination and basic behavioural training before entry.
- Top concerns: sudden aggression / safety (**40.3%**), excretion or soiling (**37.5%**), hair and allergens (**34.7%**).
- **Attitudes diverge by ownership**: pet owners supported allowing dogs far more (**71.7%** vs **41.8%**), but non-owners supported mandatory training far more (**85.7%** vs **60.9%**).

## 5. Repository structure

```
.
├── README.md
├── .gitignore
├── data/
│   ├── survey_a_main_144.csv        # raw export, anonymised
│   ├── survey_b_followup_63.csv     # raw export, anonymised
│   └── README.md                    # column dictionary
├── scripts/
│   ├── verify_data.py               # data check and frequency report
│   └── make_charts.py               # figure generation
├── charts/                          # generated figures (Fig. 1–6)
└── docs/
    └── analysis_guide.md            # analysis conventions and pitfalls
```

The written report is submitted separately and is not stored in this repository.

## 6. How to run

```bash
pip install pandas matplotlib

# 1. check data and print frequency tables
python scripts/verify_data.py

# 2. regenerate all figures into charts/
python scripts/make_charts.py
```

Paths to the raw CSV files are configured at the top of each script.

## 7. Privacy

The repository contains **anonymised survey responses only**. Personal reflections, names and any material that identifies individual respondents or team members are deliberately excluded — see `.gitignore`.

## 8. Team

Five members worked on this project. Names are omitted; responsibilities are listed instead.

| Role | Responsibilities |
|---|---|
| Group leader | Overall coordination, liaison with the teacher and TA, questionnaire and poster design, fieldwork |
| Communication and design | Team communication, questionnaire and poster design, fieldwork, project introduction |
| Data analysis and reporting | Data cleaning and analysis, database building, report writing, problems and solutions |
| Report and presentation | Report writing, fieldwork, presentation of recommendations |
| Technical support | Technical support, data analysis, poster and video production |
