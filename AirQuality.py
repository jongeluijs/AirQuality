import time
from datetime import datetime
from subprocess import PIPE, Popen
import sqlite3

#################### Helper classes

class Database():
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        
    def add_enviro(self, time, temp, pres, hum, light, prox, noise):
        self.cur.execute("INSERT INTO environ(timedate, temperature, pressure, humidity, light, proximity, noise) \
                         VALUES({}, {}, {}, {}, {}, {}, {} )".format(
                             time, temp, pres, hum, light, prox, noise
                         ))
        self.conn.commit()

    def add_gasses(self, time, oxidising, reducing, NH3):
        self.cur.execute("INSERT INTO gasses(timedate, oxidising, reducing, NH3) \
                         VALUES({}, {}, {}, {} )".format(
                             time, oxidising, reducing, NH3
                         ))
        self.conn.commit()

    def add_pms5003(self, time, pm1, pm25, pm10):
        self.cur.execute("INSERT INTO pms5003(timedate, pm1, pm25, pm10) \
                          VALUES({}, {}, {}, {})".format(
                              time, pm1, pm25, pm10
                          ))
        self.conn.commit()

    def close(self):
        self.conn.close()

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

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

    noise = noise.Noise()

    empty_runs = 1   # Give sensors time to get stable values
    factor = 5.0    # Factor to compensate for cpu-temperature
    db = Database('airquality.db')
    while True:
        time.sleep(60.0)
        try:
            raw_temp = bme280.get_temperature()
            cpu_temp = get_cpu_temperature()
            temp = raw_temp - ((cpu_temp - raw_temp) / factor)
            print("raw={} cpu={} temp={}".format(raw_temp, cpu_temp, temp))
            pres = bme280.get_pressure()
            hum  = bme280.get_humidity()
            light = ltr559.get_lux()
            prox = ltr559.get_proximity()

            low, mid, high, amp = noise.get_noise_profile()
            noise_amp = amp

            ct = datetime.now()

            # Add data to database
            print("enviro:\n  temp={}\n  pres={}\n  hum={}\n  light={}\n  prox={}\n  noise={}".format(
                temp, pres, hum, light, prox, noise_amp
            ))

            gas_data = gas.read_all()
            oxidising = gas_data.oxidising / 1000
            reducing = gas_data.reducing /1000
            nh3 = gas_data.nh3 / 1000
            print("gas:\n  oxidising={}\n  reducing={}\n. nh3={}".format(
                oxidising, reducing, nh3
            ))

            part_data = pms5003.read()
            pm1 = float(part_data.pm_ug_per_m3(1.0))
            pm2 = float(part_data.pm_ug_per_m3(2.5))
            pm10 = float(part_data.pm_ug_per_m3(10.0))
            print("particles:\n  1={}\n. 2.5={}\n. 10={}".format(pm1, pm2, pm10))

            if empty_runs > 5:
                db.add_enviro(ct.timestamp(), temp, pres, hum, light, prox, noise_amp)
                db.add_gasses(ct.timestamp(), oxidising, reducing, nh3)
                db.add_pms5003(ct.timestamp(), pm1, pm2, pm10)
            else:
                empty_runs = empty_runs + 1

        except:
            continue
