import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:YOUR_PASSWORD_HERE@localhost:5432/credit_risk_analysis_project')

path = r"C:\Users\ansht\Downloads\lending-club\accepted_2007_to_2018q4.csv\accepted_2007_to_2018Q4.csv"

cols = ['id', 'loan_amnt', 'term', 'int_rate', 'grade', 'sub_grade', 'purpose',
        'issue_d', 'installment', 'loan_status', 'annual_inc', 'dti', 'emp_length', 'home_ownership']

rename_map = {
    'id': 'loan_id',
    'loan_amnt': 'loan_amount',
    'int_rate': 'interest_rate',
    'issue_d': 'issue_date',
    'annual_inc': 'annual_income',
    'dti': 'debt_to_income',
    'emp_length': 'employment_years',
    'home_ownership': 'home_ownership_status'
}

chunks = []
for c in pd.read_csv(path, usecols=cols, chunksize=200000, low_memory=False):
    c = c.rename(columns=rename_map)
    c = c[c['loan_status'].isin(['Fully Paid', 'Charged Off'])]
    chunks.append(c)

loan_table = pd.concat(chunks, ignore_index=True)
print(loan_table.shape)
print(loan_table['loan_status'].value_counts())

loan_table['issue_date'] = pd.to_datetime(loan_table['issue_date'], format='%b-%Y', errors='coerce')
loan_table['interest_rate'] = loan_table['interest_rate'].astype(str).str.replace('%', '').astype(float)

borrowers = loan_table[['loan_id', 'annual_income', 'debt_to_income', 'employment_years', 'home_ownership_status']].rename(columns={'loan_id': 'borrower_id'})

loans = loan_table[['loan_id', 'loan_amount', 'term', 'interest_rate', 'grade', 'sub_grade', 'purpose', 'issue_date', 'installment', 'loan_status']]
loans['borrower_id'] = loan_table['loan_id']

borrowers.to_sql('lc_borrowers', engine, if_exists='replace', index=False, chunksize=5000)
loans.to_sql('lc_loans', engine, if_exists='replace', index=False, chunksize=5000)

print("DONE WITH LENDING CLUB")

