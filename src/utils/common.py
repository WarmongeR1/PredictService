# -*- encoding: utf-8 -*-
from datetime import datetime
import os
import sys

from settings import PROGRAMMS


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


def create_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def get_cnt_lines_in_file(filepath):
    return len(read_file(filepath))


def read_file(filepath):
    try:
        with open(filepath, 'r') as fi:
            return [item.rstrip('\n') for item in fi.readlines()]
    except FileNotFoundError:
        create_dir(os.path.dirname(filepath))
        open(filepath, 'w').close()
        raise


def get_cnt_satellites(data_folder):
    return len(get_names(data_folder))


def get_satellite_names(filepath):
    lines = read_file(filepath)

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

    for programm in PROGRAMMS:
        filepath = os.path.join(data_folder, programm, 'temp')
        create_dir(os.path.dirname(filepath))
        with open(filepath, 'w') as fi:
            fi.writelines(['%s\n' % item for item in satellites_list])


def get_names(data_folder):
    # hindi
    # todo
    result = 0
    for programm in PROGRAMMS:
        filepath = os.path.join(data_folder, programm, 'temp')
        if os.path.exists(filepath):
            result = get_satellite_names(filepath)
            break
        else:
            continue
    else:
        raise Exception('Not found results in folder %s' % data_folder)
    return result


def get_name(index, data_folder):
    return get_names(data_folder)[index]
