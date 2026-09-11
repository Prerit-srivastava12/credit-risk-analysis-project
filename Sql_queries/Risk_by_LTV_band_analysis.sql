SELECT 
    CASE 
        WHEN loan_to_value_ratio < 70 THEN 'Low LTV (<70%)'
        WHEN loan_to_value_ratio < 90 THEN 'Mid LTV (70-90%)'
        ELSE 'High LTV (90%+)'
    END AS ltv_band,
    COUNT(*) AS n_loans,
    ROUND((100.0 * AVG(loan_default))::numeric, 2) AS default_rate_pct
FROM lt_loans
GROUP BY ltv_band
ORDER BY ltv_band;