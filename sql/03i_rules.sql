-- rule 1 = TWF test: tool wear 200 to 240 min
-- rule 2 = HDF test: temperature difference below 8.6 K and speed below 1380 rpm
-- rule 3 = PWF test: power below 3500 W or above 9000 W
-- rule 4 = OSF test: wear x torque above 11000 (L), 12000 (M), 13000 (H)
WITH p AS (
SELECT *,
process_temp_k - air_temp_k AS temp_diff_k,
torque_nm * rot_speed_rpm * 2 * pi() / 60 AS power_w,
tool_wear_min * torque_nm AS wear_torque,
CASE ascii(type) WHEN 76 THEN 11000 WHEN 77 THEN 12000 WHEN 72 THEN 13000 END AS osf_limit
FROM ai4i
)
SELECT 1 AS rule, (tool_wear_min BETWEEN 200 AND 240) AS rule_met, twf AS flag, COUNT(*) AS n FROM p GROUP BY 2,3
UNION ALL
SELECT 2, (temp_diff_k < 8.6 AND rot_speed_rpm < 1380), hdf, COUNT(*) FROM p GROUP BY 2,3
UNION ALL
SELECT 3, (power_w < 3500 OR power_w > 9000), pwf, COUNT(*) FROM p GROUP BY 2,3
UNION ALL
SELECT 4, (wear_torque > osf_limit), osf, COUNT(*) FROM p GROUP BY 2,3
ORDER BY 1,2,3;
