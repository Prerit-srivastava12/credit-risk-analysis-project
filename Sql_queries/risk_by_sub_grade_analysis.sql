-- Risk by sub-grade: same as risk_by_grade, a more precise analysis (A1-G5)

SELECT 
    sub_grade,
    COUNT(*) AS n_loans,
    ROUND(AVG(interest_rate)::numeric, 2) AS avg_interest_rate,
    ROUND(100.0 * SUM(CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END) / COUNT(*), 2) AS default_rate_pct
FROM lc_loans
GROUP BY sub_grade
ORDER BY sub_grade;
