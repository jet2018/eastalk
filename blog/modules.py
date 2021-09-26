import time
import datetime
from django.http import JsonResponse


def JsTimestampToPyDatetime(js_date):
    """
        converts javascript timestamp to python datetime taking care of milliseconds and seconds

        Args:
            js_date(Timestamp, required)

        Returns:
            Datetime
    """
    try:
        # when timestamp is in seconds
        date = datetime.datetime.fromtimestamp(int(js_date))
    except (ValueError):
        # when timestamp is in miliseconds
        date = datetime.datetime.fromtimestamp(int(js_date) / 1000)
    return date


# a = JsTimestampToPyDatetime(1627303810000)
# b = JsTimestampToPyDatetime(1627476610000)


def GetDaysInDateTime(min_stamp, max_stamp):
    """
        Calculates time difference between two timestamps in days

        Args:
            min_stamp(Datetime, required): Minimum/start datetime
            max_stamp(Datetime, required): Maximum/end datetime

        Returns:
            Int: Days
    """
    days = (max_stamp-min_stamp).days
    return int(days)
