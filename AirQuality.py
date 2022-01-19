import sqlite3

from datetime import datetime

#################### Helper classes

class Database():
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        
    def add_enviro(self, time, temp, pres, hum, light, prox, noise):
        self.cur.execute("INSERT INTO environ(timedate, temperature, pressure, humidity, light, proximity, noise) \
                         VALUES('%s', %s, %s, %s, %s, %s, %s )" % 
                         (time, temp, pres, hum, light, prox, noise))
        self.cur.commit()

    def add_gasses(self, time, CO, NO2, C2H5OH, H2, NH3, CO4, C3H8, C4H10):
        self.cur.execute("INSERT INTO gasses(timedate, CO2, NO2, C2H5OH, H2, NH3, CO4, C3H8, C4H10) \
                         VALUES('%s', %s, %s, %s, %s, %s, %s, %s, %s )" % 
                         (time, CO, NO2, C2H5OH, H2, NH3, CO4, C3H8, C4H10))
        self.cur.commit()

    def add_pms5003(self, time, pm1, pm25, pm10):
        self.cur.execute("INSERT INTO pms5003(timedate, pm1, pm25, pm10) \
                          VALUES('%s', %s, %s, %s)" % 
                          (time, pm1, pm25, pm10))
        self.cur.commit()

    def close(self):
        self.cur.close()


if __name__ == "__main__":

    from bme280 import BME280
    from pms5003 import PMS5003, ReadTimeoutError as pmsReadTimeoutError, SerialTimeoutError
    from enviroplus import gas, noise
    from ltr559 import LTR559
    from enviroplus.noise import Noise

    # BME280 temperature/pressure/humidity sensor
    bme280 = BME280()

    # PMS5003 particulate sensor
    pms5003 = PMS5003()

    ltr559 = LTR559()

    noise = noise.Noise()
    low, mid, high, amp = noise.get_noise_profile()
    print("Noise: {}".format(amp))
    print("Temeparture: {}".format(bme280.get_temperature()))

    db = Database('airquality.db')
    print("Connection made.")

    ct = datetime.now()
    db.add_enviro(ct.timestamp(), 
                  bme280.get_temperature(), 
                  bme280.get_pressure(), 
                  bme280.get_humidity(), 
                  ltr559.get_lux(),
                  ltr559.get_proximity(),
                  amp
                  )