CREATE TABLE IF NOT EXISTS environ ( timedate timestamp, 
                                     temperature NUMERIC,
                                     pressure NUMERIC,
                                     humidity NUMERIC,
                                     light NUMERIC,
                                     proximity NUMERIC,
                                     noise NUMERIC);

CREATE TABLE IF NOT EXISTS gasses ( timedate timestamp,
                                    CO NUMERIC,
                                    NO2 NUMERIC,
                                    C2H5OH NUMERIC,
                                    H2 NUMERIC, 
                                    NH3 NUMERIC, 
                                    CO4 NUMERIC, 
                                    C3H8 NUMERIC, 
                                    C4H10 NUMERIC);

CREATE TABLE IF NOT EXISTS pms5003 ( timedate timestamp, 
                                     pm1 NUMERIC, 
                                     pm25 NUMERIC, 
                                     pm10 NUMERIC);

create role airquality login password 'Abcd1234!';

GRANT SELECT,INSERT ON environ,gasses,pms5003 TO airquality;
            