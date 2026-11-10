SELECT
type,
COUNT(*) AS n_rows,
ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_rows
FROM ai4i
GROUP BY type
ORDER BY type;
