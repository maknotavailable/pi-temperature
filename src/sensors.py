import utils

log = utils.Logger(__name__)


def read_temperature(id: str):
    """Read Temperature from the Sensor in Celcius

    Args:
        id (str): identifier for the sensor

    Returns:
        float: temperature value, to 3 decimals
    """
    try:
        with open(f"/sys/bus/w1/devices/{id}/w1_slave") as f:
            temp = f.read()
        temp = temp.split("\n")[1].split(" ")[9]
        temp = float(temp[2:]) / 1000
    except OSError as e:
        log.warning(f'Sensor failure: temperature could not be read -> {e}')
        temp = 0.0
    return temp
