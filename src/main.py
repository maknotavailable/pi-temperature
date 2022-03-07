import os
import time
from datetime import datetime
import pandas as pd

from sensors import read_temperature
import utils

log = utils.Logger(__name__)

SLEEP_DELAY_SECONDS = 121
RECORD_INTERVAL_MINUTES = 2
WRITE_INTERVAL_MINUTES = 60
SENSOR_ID = utils.get_secret("SENSOR_ID")
FILENAME = "temperature_data.tsv"

time_since_last_record = datetime.strptime("2002-02-02", "%Y-%m-%d")
time_since_last_write = datetime.strptime("2002-02-02", "%Y-%m-%d")
log.info(time_since_last_record)
log.info(time_since_last_write)
data = []
while True:
    time_now = datetime.now()

    if utils.time_difference_passed_threshold(
        time_now, time_since_last_record, RECORD_INTERVAL_MINUTES
    ):
        temperature = read_temperature(SENSOR_ID)
        data.append(
            dict(
                temperature=temperature,
                timestamp=time_now,
                date=time_now.date().strftime("%d-%m-%Y"),
                time=time_now.strftime("%H:%M"),
                record_interval=RECORD_INTERVAL_MINUTES,
                write_interval=WRITE_INTERVAL_MINUTES,
            )
        )
        log.info(f"Recorded Temperature {temperature}")
        time_since_last_record = datetime.now()

    if utils.time_difference_passed_threshold(
        time_now, time_since_last_write, WRITE_INTERVAL_MINUTES
    ):
        df_data = pd.DataFrame(data)
        if os.path.isfile(FILENAME):
            df_data.to_csv(FILENAME, sep="\t", mode="a", index=False, header=False)
        else:
            df_data.to_csv(FILENAME, sep="\t", index=False)
        log.info(f"Wrote recently recorded temperature - {len(data)}")
        time_since_last_write = datetime.now()
        data = []

    time.sleep(SLEEP_DELAY_SECONDS)
