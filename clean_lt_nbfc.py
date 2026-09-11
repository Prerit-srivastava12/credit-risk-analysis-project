import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:Jgl%401234@localhost:5432/credit_risk_analysis_project')

path = r"C:\Users\ansht\Downloads\lt-vehicle-loan-default-prediction\train.csv"

# only the columns needed for the underwriting-risk segmentation queries
cols = ['UniqueID', 'disbursed_amount', 'asset_cost', 'ltv',
        'Employment.Type', 'DisbursalDate', 'PERFORM_CNS.SCORE', 'loan_default']

# cleaner column names for the database
rename_map = {
    'UniqueID': 'unique_id',
    'Employment.Type': 'employment_type',
    'DisbursalDate': 'disbursal_date',
    'PERFORM_CNS.SCORE': 'bureau_score',
    'ltv': 'loan_to_value_ratio'
}

loan_table = pd.read_csv(path, usecols=cols)
loan_table = loan_table.rename(columns=rename_map)

print(loan_table.shape)
print(loan_table['loan_default'].value_counts())

# Indian date format is day-first, unlike Lending Club's US-style dates
loan_table['disbursal_date'] = pd.to_datetime(loan_table['disbursal_date'], errors='coerce', dayfirst=True)
# coerce handles rows where bureau score is missing/non-numeric instead of crashing
loan_table['bureau_score'] = pd.to_numeric(loan_table['bureau_score'], errors='coerce')

borrowers = loan_table[['unique_id', 'employment_type', 'bureau_score']].rename(columns={'unique_id': 'borrower_id'})

loans = loan_table[['unique_id', 'disbursed_amount', 'asset_cost', 'loan_to_value_ratio', 'disbursal_date', 'loan_default']]
loans = loans.rename(columns={'unique_id': 'loan_id'})
loans['borrower_id'] = loan_table['unique_id']

borrowers.to_sql('lt_borrowers', engine, if_exists='replace', index=False, chunksize=5000)
loans.to_sql('lt_loans', engine, if_exists='replace', index=False, chunksize=5000)

print("DONE WITH L&T")
