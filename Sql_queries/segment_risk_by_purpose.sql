-- Default Rate by Purpose
SELECT 
    purpose,
    COUNT(*) AS n_loans,
    ROUND((100.0 * SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) / COUNT(*))::numeric, 2) AS default_rate_pct
FROM lc_loans
GROUP BY purpose
HAVING COUNT(*) > 500
ORDER BY default_rate_pct DESC;