SELECT
COUNT(*) AS total_rows,
COUNT(DISTINCT udi) AS distinct_udi,
COUNT(DISTINCT product_id) AS distinct_product_id,
(SELECT COUNT(*) FROM (SELECT product_id, type, air_temp_k, process_temp_k, rot_speed_rpm, torque_nm, tool_wear_min, machine_failure, twf, hdf, pwf, osf, rnf FROM ai4i GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13 HAVING COUNT(*) > 1) d) AS identical_row_groups
FROM ai4i;
