DROP TABLE IF EXISTS ai4i;
CREATE TABLE ai4i (
udi integer,
product_id text,
type text,
air_temp_k numeric,
process_temp_k numeric,
rot_speed_rpm integer,
torque_nm numeric,
tool_wear_min integer,
machine_failure smallint,
twf smallint,
hdf smallint,
pwf smallint,
osf smallint,
rnf smallint
);
