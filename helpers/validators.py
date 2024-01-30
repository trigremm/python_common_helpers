import datetime as dt

def validate_bool(value):
    if not isinstance(value, bool):
        raise ValueError("Value must be a bool")

def validate_callable(value):
    if not callable(value):
        raise TypeError("Value must be a callable")

def validate_date_or_datetime(value):
    if not isinstance(value, (dt.date, dt.datetime)):
        raise TypeError("Value must be a date or datetime")

def validate_date(value):
    if not isinstance(value, dt.date):
        raise TypeError("Value must be a date")

def validate_datetime(value):
    if not isinstance(value, dt.datetime):
        raise TypeError("Value must be a datetime")

def validate_dict(value):
    if not isinstance(value, dict):
        raise TypeError("Value must be a dict")

def validate_int(value):
    if not isinstance(value, int):
        raise TypeError("Value must be an integer")

def validate_list(value):
    if not isinstance(value, list):
        raise TypeError("Value must be a list")

def validate_list_of_str(value):
    validate_list(value)
    for item in value:
        if not isinstance(item, str):
            raise TypeError("All items in the list must be strings")

def validate_str(value):
    if not isinstance(value, str):
        raise TypeError("Value must be a string")
