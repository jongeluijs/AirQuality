CREATE TABLE IF NOT EXISTS environ ( timedate timestamp, 
                                     temperature NUMERIC,
                                     pressure NUMERIC,
                                     humidity NUMERIC,
                                     light NUMERIC,
                                     proximity NUMERIC,
                                     noise NUMERIC);

CREATE TABLE IF NOT EXISTS gasses ( timedate timestamp,
                                    oxidising NUMERIC,
                                    reducing NUMERIC,
                                    NH3 NUMERIC);

CREATE TABLE IF NOT EXISTS pms5003 ( timedate timestamp, 
                                     pm1 NUMERIC, 
                                     pm25 NUMERIC, 
                                     pm10 NUMERIC);

create role airquality login password 'Abcd1234!';

GRANT SELECT,INSERT ON environ,gasses,pms5003 TO airquality;
            