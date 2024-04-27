-- facubrt_coderhouse.neo_data definition

-- Drop table

-- DROP TABLE facubrt_coderhouse.neo_data;

--DROP TABLE facubrt_coderhouse.neo_data;
CREATE TABLE IF NOT EXISTS facubrt_coderhouse.neo_data
(
	"timestamp" TIMESTAMP WITHOUT TIME ZONE   ENCODE az64
	,near_earth_objects INTEGER   ENCODE az64
	,absolute_magnitude_min REAL   ENCODE RAW
	,absolute_magnitude_max REAL   ENCODE RAW
	,potentially_hazardous INTEGER   ENCODE az64
	,sentry_objects INTEGER   ENCODE az64
	,date VARCHAR(256)   ENCODE lzo
)
DISTSTYLE AUTO
;
ALTER TABLE facubrt_coderhouse.neo_data owner to facubrt_coderhouse;