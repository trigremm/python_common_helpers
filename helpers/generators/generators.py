# helpers/generators.py
import datetime as dt
from datetime import datetime, timedelta


def dates_generator(date_from, date_to=None, ascending=True):
    if isinstance(date_from, str):
        date_from = dt.datetime.strptime(date_from, "%Y-%m-%d").date()
    if isinstance(date_from, dt.datetime):
        date_from = date_from.date()

    if date_to is None:
        date_to = dt.datetime.now().date()
    if isinstance(date_to, str):
        date_to = dt.datetime.strptime(date_to, "%Y-%m-%d").date()
    if isinstance(date_to, dt.datetime):
        date_to = date_to.date()

    if ascending:
        current_date = date_from
        while current_date <= date_to:
            yield current_date
            current_date += timedelta(days=1)
    else:
        current_date = date_to
        while current_date >= date_from:
            yield current_date
            current_date -= timedelta(days=1)


def months_generator(start_date):
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m").date()

    current_date = start_date
    today = datetime.now().date()

    while current_date <= today:
        yield current_date.strftime("%Y-%m"), current_date.strftime("%Y-%m-%d")
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)


def infinite_generator(start: int = 0, step: int = 1) -> int:
    i = start
    while True:
        yield i
        i += step


def batch_generator(lst, size=2000):
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def chunk_generator(lst, size=2000):
    for i in range(0, len(lst), size):
        yield lst[i : i + size]
