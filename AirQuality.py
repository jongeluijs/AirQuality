from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from datetime import datetime

#################### Helper classes

class Database():
    def __init__(self, dbname, user, passwd, host='localhost'):
        url = f"postgresql://{user}:{passwd}@{host}:5432/{dbname}"
        self.engine = create_engine(url, pool_size=50, echo=False)
        self.conn = scoped_session(sessionmaker(bind=self.engine))

    def add_enviro(self, time, temp, pres, hum, light, prox, noise):
        self.conn.execute("INSERT INTO environ(timestamp, temperature, pressure, humidity, light, proximity, noise) \
                          VALUES('%s', %s, %s, %s, %s, %s, %s )" % 
                          (time, temp, pres, hum, light, prox, noise))
        self.conn.commit()

    def add_gasses(self, time, CO, NO2, C2H5OH, H2, NH3, CO4, C3H8, C4H10):
        self.conn.execute("INSERT INTO gasses(timestamp, CO2, NO2, C2H5OH, H2, NH3, CO4, C3H8, C4H10) \
                          VALUES('%s', %s, %s, %s, %s, %s, %s, %s, %s )" % 
                          (time, CO, NO2, C2H5OH, H2, NH3, CO4, C3H8, C4H10))
        self.conn.commit()

    def add_pms5003(self, time, pm1, pm25, pm10):
        self.conn.execute("INSERT INTO pms5003(timestamp, pm1, pm25, pm10) \
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

    db = Database('airquality', 'airquality', 'Abcd1234!')
    print("Connection made.")

    ct = datetime.now()
    db.add_enviro(ct.timestamp(), 
                  bme280.get_temperature(), 
                  bme280.get_pressure(), 
                  bme280.get_humidity(), 
                  ltr559.get_lux(),
                  ltr559.get_proximity(),
                  )