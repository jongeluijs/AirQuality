import psycopg2 as pg
from datetime import datetime

#################### Helper classes

class MyDatabase():
    def __init__(self, dbname, user, passwd, host='localhost'):
        self.conn = pg.connect("host={} dbname={} user={} password={}".format(host, dbname, user, passwd))
        self.cur = self.conn.cursor()

    def add_environ(self, time, temp, pres, hum, light, prox, noise):
        self.cur.execute("INSERT INTO environ(timestamp, temperature, pressure, humidity, light, proximity, noise) 
                         VALUES('%s', %s, %s, %s, %s, %s, %s )" % 
                         (time, temp, pres, hum, light, prox, noise))
        self.conn.commit()

    def add_gasses(self, time, CO, NO2, C2H5OH, H2, NH3, CO4, C3H8, C4H10)
        self.cur.execute("INSERT INTO gasses(timestamp, CO2, NO2, C2H5OH, H2, NH3, CO4, C3H8, C4H10) 
                         VALUES('%s', %s, %s, %s, %s, %s, %s, %s, %s )" % 
                         (time, CO, NO2, C2H5OH, H2, NH3, CO4, C3H8, C4H10))
        self.conn.commit()

    def add_pms5003(self, time, pm1, pm25, pm10)
        self.cur.execute("INSERT INTO pms5003(timestamp, pm1, pm25, pm10) 
                          VALUES('%s', %s, %s, %s)" % 
                          (time, pm1, pm25, pm10))
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()