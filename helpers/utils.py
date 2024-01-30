# helpers/utils.py
import datetime as dt
from typing import Union

from helpers.constants import DATETIME_FORMAT, DATETIMETZ_FORMAT, DATETIMETZ_WITH_MICROSECONDS_FORMAT


def deduplicate_address_list(address_list) -> list:
    return sorted(set(i.lower().strip() for i in address_list if i.strip()))


def is_it_today(date_str: Union[str, dt.datetime]) -> bool:
    if not date_str:
        return False
    return dt.datetime.now().date() == str_to_datetime(date_str).date()


def str_to_datetime(date_str: Union[str, dt.datetime]) -> dt.datetime:
    if isinstance(date_str, dt.datetime):
        return date_str
    if "Z" in date_str:
        try:
            date_value = dt.datetime.strptime(date_str, DATETIMETZ_FORMAT)
        except ValueError:
            date_value = dt.datetime.strptime(date_str, DATETIMETZ_WITH_MICROSECONDS_FORMAT)
        return date_value.replace(tzinfo=None)  # Remove timezone info
    return dt.datetime.strptime(date_str, DATETIME_FORMAT)


def timedelta_since(date_str: Union[str, dt.datetime]) -> dt.timedelta:
    return dt.datetime.now() - str_to_datetime(date_str)


def get_end_of_hour(time):
    return time.replace(minute=59, second=59, microsecond=0)

