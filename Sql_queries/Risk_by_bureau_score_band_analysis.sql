SELECT 
    CASE 
        WHEN t2.bureau_score < 500 THEN 'Poor (<500)'
        WHEN t2.bureau_score < 700 THEN 'Fair (500-700)'
        ELSE 'Good (700+)'
    END AS score_band,
    COUNT(*) AS n_loans,
    ROUND((100.0 * AVG(t1.loan_default))::numeric, 2) AS default_rate_pct
FROM lt_loans t1
JOIN lt_borrowers t2 ON t1.borrower_id = t2.borrower_id
GROUP BY score_band
ORDER BY default_rate_pct DESC;