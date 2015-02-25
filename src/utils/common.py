# -*- encoding: utf-8 -*-
from datetime import datetime


def local_to_unix(year, month, day, hour, minute, second):

    d = datetime(
        int(year),
        int(month),
        int(day),
        int(hour),
        int(minute),
        int(second))

    unix_time = d.strftime('%s')

    return unix_time
