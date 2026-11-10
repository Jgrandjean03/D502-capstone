SELECT
type,
COUNT(*) AS n_rows,
SUM(machine_failure) AS n_failures,
ROUND(100.0 * SUM(machine_failure) / COUNT(*), 3) AS failure_rate_pct
FROM ai4i
GROUP BY ROLLUP (type)
ORDER BY type;
