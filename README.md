# Credit Risk Analysis (SQL Project)

This project applies SQL-based credit risk analysis to two real lending datasets : Lending Club (US, full loan lifecycle) and L&T Financial Services (India, vehicle loan underwriting). The goal was to combine my Financial Economics background with SQL, and to see whether the same risk-segmentation approach holds up across different markets and loan products, not just one dataset in isolation.

## Stack
- PostgreSQL
- Python (pandas, SQLAlchemy) for cleaning and loading the data
- Excel for the charts

## Running this yourself
1. Grab the two datasets from Kaggle:
   - [Lending Club Loan Data](https://www.kaggle.com/datasets/wordsforthewise/lending-club) — use `accepted_2007_to_2018Q4.csv`
   - [L&T Vehicle Loan Default Prediction](https://www.kaggle.com/datasets/mamtadhaker/lt-vehicle-loan-default-prediction) — `train.csv`
2. Create a PostgreSQL database.
3. The cleaning scripts have a placeholder password (`YOUR_PASSWORD_HERE`) in the connection string, swap in your own before running them.
4. Run `clean_lending_club.py` then `clean_lt_nbfc.py`.
5. Queries live in `sql_queries/`, run them against the tables once loaded.

## What's in here

1. sql_queries/    : the actual SQL
2. results/        : raw output from each query, as CSV
3. charts/         : charts built from those results
4. clean_lending_club.py
5. clean_lt_nbfc.py


## Part 1: Lending Club

The question I was working from: is the loan book getting riskier over time, where's the risk concentrated, and is the interest rate actually pricing for it? Everything here runs on ~1.34 million closed loans (Fully Paid or Charged Off).

### Default rate by issue quarter (vintage analysis)
[`Sql_queries/Vintage_analysis.sql`](Sql_queries/Vintage_analysis.sql) · [`Charts/Vintage_default_rate_chart.png`](Charts/Vintage_default_rate_chart.png)

Default rate went from around 12% in 2008 up to roughly 26% by 2016, then flattened out near 24%. I cut the chart off after Q3 2017 on purpose because anything issued after that hasn't had time to actually default yet, so the raw numbers for those quarters look artificially low. Including them would make it look like risk suddenly dropped at the end, which isn't real.

### Interest rate vs. default rate, by grade
[`Sql_queries/risk_by_grade_analysis.sql`](Sql_queries/risk_by_grade_analysis.sql) · [`Charts/risk_by_grade_chart.png`](Charts/risk_by_grade_chart.png)

Grade A loans charge about 7% interest and default 6% of the time which is a decent cushion. Grade G only charges around 28% interest but defaults on nearly half of all loans. The gap between what's charged and what's lost basically disappears at the risky end, which suggests the pricing isn't really keeping up with the risk. Worth saying: this is just interest rate minus default rate by loan count, not a real profitability number that would need recovery rates and dollar weighting, which I didn't have here.

### Same thing, by sub-grade
[`Sql_queries/risk_by_sub_grade_analysis.sql`](Sql_queries/risk_by_sub_grade_analysis.sql) · [`Charts/risk_by_sub_grade_chart.png`](Charts/risk_by_sub_grade_chart.png)

Just checking whether the grade-level pattern holds at a finer level (A1 to G5 instead of just A to G). It does as both interest rate and default rate climb smoothly within each letter grade, so the grading system looks internally consistent.

### Default rate by income bracket
[`Sql_queries/segment_risk_by_income.sql`](Sql_queries/segment_risk_by_income.sql) · [`Charts/segment_risk_by_income_chart.png`](Charts/segment_risk_by_income_chart.png)

Low income: 23.75%. Mid: 20.63%. High: 16.31%. Pretty steady decline, about a 7-point gap top to bottom.

### Default rate by loan purpose
[`Sql_queries/segment_risk_by_purpose.sql`](Sql_queries/segment_risk_by_purpose.sql) · [`Charts/segment_risk_by_purpose_chart.png`](Charts/segment_risk_by_purpose_chart.png)

Small business loans stand out at 29.71% default rate, well above everything else (next closest is renewable energy at 23.69%). Wedding loans are the safest at 12.16%.

### Purpose and income together
[`Sql_queries/segment_risk_purpose_income.sql`](Sql_queries/segment_risk_purpose_income.sql) · [`Charts/segment_risk_by_purpose_income_heatmap.png`](Charts/segment_risk_by_purpose_income_heatmap.png)

Wanted to check if these two interact or just add up independently, it looks like the latter. Small business loans stay risky no matter the income bracket, and within basically every purpose, default rate drops as income rises. The riskiest combination (small business, mid income, 31.71%) is close to 3x the safest one (car loans, high income, 11.54%).
