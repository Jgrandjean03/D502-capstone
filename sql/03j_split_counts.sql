SELECT
COUNT(*) FILTER (WHERE udi <= 7900) AS train_rows,
SUM(machine_failure) FILTER (WHERE udi <= 7900) AS train_failures,
COUNT(*) FILTER (WHERE udi BETWEEN 7901 AND 8000) AS gap_rows,
SUM(machine_failure) FILTER (WHERE udi BETWEEN 7901 AND 8000) AS gap_failures,
COUNT(*) FILTER (WHERE udi > 8000) AS test_rows,
SUM(machine_failure) FILTER (WHERE udi > 8000) AS test_failures,
ROUND(100.0 * SUM(machine_failure) FILTER (WHERE udi <= 8000) / 8000, 3) AS first80_rate_pct,
ROUND(100.0 * SUM(machine_failure) FILTER (WHERE udi > 8000) / 2000, 3) AS last20_rate_pct
FROM ai4i;
