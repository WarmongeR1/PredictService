# -*- encoding: utf-8 -*-
from datetime import datetime

import os
import sys


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


def get_satellite_names(filepath):
    with open(filepath, 'r') as fi:
        lines = [item.rstrip('\n') for item in fi.readlines()]

    if sys.version < '3':
        y = len(lines) / 3
    else:
        y = len(lines) // 3

    list_numbers = [x * 3 for x in range(y)]

    satellites_list = []
    for i in range(len(list_numbers)):
        satellites_list.append(lines[list_numbers[i]])
    return satellites_list


def generate_temp_files(tle_filepath, data_folder):
    satellites_list = get_satellite_names(tle_filepath)

    programms = [
        'PyEphem',
        'predict',
        'PyOrbital',
        'Orbitron'
    ]

    for programm in programms:
        filepath = os.path.join(data_folder, programm, 'temp')
        with open(filepath, 'w') as fi:
            fi.writelines(['%s\n' % item for item in satellites_list])

