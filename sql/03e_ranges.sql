SELECT
MIN(udi) AS udi_min, MAX(udi) AS udi_max,
MIN(air_temp_k) AS air_temp_min, MAX(air_temp_k) AS air_temp_max,
MIN(process_temp_k) AS process_temp_min, MAX(process_temp_k) AS process_temp_max,
MIN(rot_speed_rpm) AS speed_min, MAX(rot_speed_rpm) AS speed_max,
MIN(torque_nm) AS torque_min, MAX(torque_nm) AS torque_max,
MIN(tool_wear_min) AS wear_min, MAX(tool_wear_min) AS wear_max,
MIN(machine_failure) AS failure_min, MAX(machine_failure) AS failure_max,
MIN(twf) AS twf_min, MAX(twf) AS twf_max,
MIN(hdf) AS hdf_min, MAX(hdf) AS hdf_max,
MIN(pwf) AS pwf_min, MAX(pwf) AS pwf_max,
MIN(osf) AS osf_min, MAX(osf) AS osf_max,
MIN(rnf) AS rnf_min, MAX(rnf) AS rnf_max,
MIN(length(product_id)) AS pid_len_min, MAX(length(product_id)) AS pid_len_max
FROM ai4i;
