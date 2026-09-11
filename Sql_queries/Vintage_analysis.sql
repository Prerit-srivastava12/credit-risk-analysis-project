-- Vintage/cohort default analysis: default rate by loan issue quarter
 
SELECT 
    DATE_TRUNC('quarter', issue_date) AS issue_quarter,
    COUNT(*) AS total_loans,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) AS defaults,
    ROUND(100.0 * SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct
FROM lc_loans
GROUP BY issue_quarter
ORDER BY issue_quarter;
