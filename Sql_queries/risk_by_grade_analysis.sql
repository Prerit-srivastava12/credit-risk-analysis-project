SELECT 
    grade,
    COUNT(*) AS n_loans,
    ROUND(AVG(interest_rate)::numeric, 2) AS avg_interest_rate,
    ROUND((100.0 * SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) / COUNT(*))::numeric, 2) AS default_rate_pct
FROM lc_loans
GROUP BY grade
ORDER BY grade;