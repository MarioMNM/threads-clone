from datetime import datetime
import pytz


def datetime_now() -> datetime:
    gmt = pytz.timezone('GMT')
    return datetime.now(gmt)
