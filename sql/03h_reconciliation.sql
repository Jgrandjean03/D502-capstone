SELECT
SUM(twf) AS twf_total,
SUM(hdf) AS hdf_total,
SUM(pwf) AS pwf_total,
SUM(osf) AS osf_total,
SUM(rnf) AS rnf_total,
SUM(twf + hdf + pwf + osf + rnf) AS flag_total,
COUNT(*) FILTER (WHERE twf + hdf + pwf + osf + rnf > 0) AS rows_with_any_flag,
COUNT(*) FILTER (WHERE twf + hdf + pwf + osf + rnf > 1) AS rows_with_multiple_flags,
COUNT(*) FILTER (WHERE machine_failure = 1 AND twf + hdf + pwf + osf + rnf = 0) AS b_failure_no_flag,
COUNT(*) FILTER (WHERE machine_failure = 0 AND twf + hdf + pwf + osf + rnf > 0) AS any_flag_label_0,
COUNT(*) FILTER (WHERE rnf = 1 AND twf + hdf + pwf + osf = 0) AS a_random_only,
COUNT(*) FILTER (WHERE rnf = 1 AND machine_failure = 0) AS c_random_flag_label_0,
COUNT(*) FILTER (WHERE machine_failure = 1 AND twf + hdf + pwf + osf > 0) AS failure_with_nonrandom_flag
FROM ai4i;
