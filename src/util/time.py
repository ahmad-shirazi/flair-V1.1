import pytz
from datetime import datetime


def localize(dt, tz=pytz.timezone('America/New_York')):
    return pytz.utc.localize(dt).astimezone(tz)


def get_current_time():
    dt = datetime.utcnow()
    return localize(dt)


def get_current_timestamp():
    return get_current_time().timestamp()


def from_timestamp(timestamp):
    dt = datetime.utcfromtimestamp(timestamp)
    return localize(dt)


def get_timestamp_in_milliseconds_from_datetime(dt):
    timestamp = dt.timestamp()
    return int(timestamp * 1000.0)

