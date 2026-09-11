SELECT 
    t2.employment_type,
    COUNT(*) AS n_loans,
    ROUND((100.0 * AVG(t1.loan_default))::numeric, 2) AS default_rate_pct
FROM lt_loans t1
JOIN lt_borrowers t2 ON t1.borrower_id = t2.borrower_id
GROUP BY t2.employment_type
ORDER BY default_rate_pct DESC;