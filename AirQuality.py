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
        self.conn.commit()

    def add_gasses(self, time, CO, NO2, C2H5OH, H2, NH3, CO4, C3H8, C4H10):
        self.cur.execute("INSERT INTO gasses(timedate, CO2, NO2, C2H5OH, H2, NH3, CO4, C3H8, C4H10) \
                         VALUES('%s', %s, %s, %s, %s, %s, %s, %s, %s )" % 
                         (time, CO, NO2, C2H5OH, H2, NH3, CO4, C3H8, C4H10))
        self.conn.commit()

    def add_pms5003(self, time, pm1, pm25, pm10):
        self.cur.execute("INSERT INTO pms5003(timedate, pm1, pm25, pm10) \
                          VALUES('%s', %s, %s, %s)" % 
                          (time, pm1, pm25, pm10))
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == "__main__":

    from bme280 import BME280
    from pms5003 import PMS5003, ReadTimeoutError as pmsReadTimeoutError, SerialTimeoutError
    from enviroplus import gas, noise
    from ltr559 import LTR559

    # BME280 temperature/pressure/humidity sensor
    bme280 = BME280()

    # PMS5003 particulate sensor
    pms5003 = PMS5003()

    ltr559 = LTR559()

    # get database connection
    #db = Database('airquality.db')

    temp = bme280.get_temperature()
    pres = bme280.get_pressure()
    hum  = bme280.get_humidity()
    light = ltr559.get_lux()
    prox = ltr559.get_proximity()

    noise = noise.Noise()
    low, mid, high, amp = noise.get_noise_profile()
    noise = amp

    ct = datetime.now()

    # Add data to database
    print("enviro:\n  temp={}\n  pres={}\n  hum={}\n  light={}\n  prox={}\n  noise={}".format(
        temp, pres, hum, light, prox, noise
    ))
    #db.add_enviro(ct.timestamp(), temp, pres, hum, light, prox, noise)

    gas_data = gas.read_all()
    print("gas:\n  CO={}\n  NO2={}".format(gas_data.oxidising, gas_data.reducing))

    part_data = pms5003.read()
    print{"particles:\n  1={}\n. 2.5={}\n. 10={}".format(
        part_data.pm_ug_per_m3(1), part_data.pm_ug_per_m3(2.5), part_data.pm_ug_per_m3(10)
    )}
