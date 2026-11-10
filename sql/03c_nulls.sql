SELECT
COUNT(*) - COUNT(udi) AS udi,
COUNT(*) - COUNT(product_id) AS product_id,
COUNT(*) - COUNT(type) AS type,
COUNT(*) - COUNT(air_temp_k) AS air_temp_k,
COUNT(*) - COUNT(process_temp_k) AS process_temp_k,
COUNT(*) - COUNT(rot_speed_rpm) AS rot_speed_rpm,
COUNT(*) - COUNT(torque_nm) AS torque_nm,
COUNT(*) - COUNT(tool_wear_min) AS tool_wear_min,
COUNT(*) - COUNT(machine_failure) AS machine_failure,
COUNT(*) - COUNT(twf) AS twf,
COUNT(*) - COUNT(hdf) AS hdf,
COUNT(*) - COUNT(pwf) AS pwf,
COUNT(*) - COUNT(osf) AS osf,
COUNT(*) - COUNT(rnf) AS rnf,
COUNT(*) FILTER (WHERE length(product_id) = 0) AS product_id_empty,
COUNT(*) FILTER (WHERE length(type) = 0) AS type_empty
FROM ai4i;
