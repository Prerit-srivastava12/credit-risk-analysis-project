-- Default rate by purpose and income bracket combined

SELECT 
    t1.purpose,
    CASE 
        WHEN t2.annual_income < 40000 THEN 'Low'
        WHEN t2.annual_income < 90000 THEN 'Mid'
        ELSE 'High'
    END AS income_bracket,
    COUNT(*) AS n_loans,
    ROUND((100.0 * SUM(CASE WHEN t1.loan_status = 'Charged Off' THEN 1 ELSE 0 END) / COUNT(*))::numeric, 2) AS default_rate_pct
FROM lc_loans t1
JOIN lc_borrowers t2 ON t1.borrower_id = t2.borrower_id
GROUP BY t1.purpose, income_bracket
HAVING COUNT(*) > 500
ORDER BY default_rate_pct DESC
LIMIT 20;
