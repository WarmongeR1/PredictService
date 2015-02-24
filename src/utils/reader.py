# -*- encoding: utf-8 -*-

import sys


class TleReader(object):

    def __init__(self):
        self.show_satellite_list = []
        self.tle_first_line_list = []
        self.tle_second_line_list = []

    def read(self, filepath):
        """
        Read file and generate 3 lists with TLE lines
        :param filepath:
        :return:
        """

        with open(filepath, 'r') as file:
            list_names_satellites = file.readlines()
            list_names_satellites = [
                item.strip() for item in list_names_satellites
            ]

        length_list = len(list_names_satellites)

        if sys.version < '3':
            y = length_list / 3
        else:
            y = length_list // 3

        list_numbers = list(map(self.return_list, list(range(y))))

        self.show_satellite_list = []
        self.tle_first_line_list = []
        self.tle_second_line_list = []

        tle0 = 0
        tle1 = 1
        tle2 = 2

        for tle0 in range(len(list_numbers)):
            self.show_satellite_list.append(
                list_names_satellites[
                    list_numbers[tle0]])
            self.tle_first_line_list.append(list_names_satellites[tle1])
            self.tle_second_line_list.append(list_names_satellites[tle2])
            tle1 = list_numbers[tle0] + 4
            tle2 = list_numbers[tle0] + 5

    def return_list(self, x):
        return 3 * x

    def get(self):
        return self.show_satellite_list, \
            self.tle_first_line_list, \
            self.tle_second_line_list
