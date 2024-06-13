import calendar
import datetime


def get_current_time(*, time_format=None):
    # output: '2022-09-26 13:50:29.410860'
    current_time = datetime.datetime.now()
    if time_format:
        return current_time.strftime(time_format)
    return current_time


def get_current_date_iso_format():
    current_date = str(datetime.datetime.now())
    return datetime.datetime.fromisoformat(current_date).strftime("%Y-%m-%d")


def get_time_in_current_date(hour=0, minute=0, second=0, microsecond=0):
    current = datetime.datetime.now()
    return current.replace(hour=hour, minute=minute, second=second, microsecond=microsecond)


def get_fmt(date_time, /, *, fmt="%Y-%m-%d"):
    return date_time.strftime(fmt)


def get_month(time_start=None, *, move_month=1):
    _DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    _today = datetime.datetime.fromisoformat(time_start) if time_start else datetime.datetime.today()
    _current_month = _today.month - 1  # match with index, count from 0
    _current_year = _today.year

    _negative = 1
    if move_month < 0:
        move_month = abs(move_month)
        _negative = -1

    _total_days = 0
    for i in range(move_month):
        _inc_year, _feb = divmod(_current_month + i * _negative, 12)
        # Divmod a negative number always return negative,
        # so we need to move it forward by 1
        if _inc_year < 0:
            _inc_year += 1

        if _feb == 1:  # Feb
            _total_days += 29 if calendar.isleap(_current_year + _inc_year * _negative) else 28
            continue

        _total_days += _DAYS[(_current_month + i * _negative) % 12]
    return _today + _negative * datetime.timedelta(days=_total_days)


def move_date_by_number_of_days(date_move, *, day_start=None, time_format=None):
    current_date = datetime.datetime.now()
    if day_start:
        current_date = datetime.datetime.fromisoformat(str(day_start))
    moved_to_date = current_date + datetime.timedelta(days=date_move)
    if time_format:
        return moved_to_date.strftime(time_format)
    return moved_to_date


def pretty_time(seconds):
    sign_string = "-" if seconds < 0 else ""
    seconds = abs(int(seconds))
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return "%s%dd%dh%dm%ds" % (sign_string, days, hours, minutes, seconds)
    elif hours > 0:
        return "%s%dh%dm%ds" % (sign_string, hours, minutes, seconds)
    elif minutes > 0:
        return "%s%dm%ds" % (sign_string, minutes, seconds)
    else:
        return "%s%ds" % (sign_string, seconds)


def calculate_quarter_hourly_interval():
    now = get_current_time()
    return now.replace(minute=15 * (now.minute // 15)) + datetime.timedelta(minutes=15)
