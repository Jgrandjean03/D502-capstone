-- HDF flagged but rule not met, and TWF flagged but outside 200 to 240 min
SELECT
CASE WHEN hdf = 1 THEN 1 ELSE 0 END AS hdf_flag,
CASE WHEN twf = 1 THEN 1 ELSE 0 END AS twf_flag,
udi,
type,
process_temp_k - air_temp_k AS temp_diff_k,
rot_speed_rpm,
tool_wear_min,
machine_failure,
twf, hdf, pwf, osf, rnf
FROM ai4i
WHERE (hdf = 1 AND NOT (process_temp_k - air_temp_k < 8.6 AND rot_speed_rpm < 1380))
OR (twf = 1 AND NOT (tool_wear_min BETWEEN 200 AND 240))
ORDER BY hdf_flag DESC, udi;
