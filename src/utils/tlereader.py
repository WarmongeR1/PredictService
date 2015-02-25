# -*- encoding: utf-8 -*-

import sys

from ephem import Observer, degrees, now
import ephem


class TLEReader(object):

    def __init__(self):
        self.show_satellite_list = []
        self.tle_first_line_list = []
        self.tle_second_line_list = []

        self.observer = None
        self.inclination = None
        self.mean_motion = None
        self.epoch = None

    def read(self, filepath):
        """Read file and generate 3 lists with TLE lines.

        :param filepath:
        :return:

        """
        # HINDI FUCKING CODE!!!!

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

        list_numbers = [x * 3 for x in range(y)]

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

    def get(self):
        return self.show_satellite_list, \
            self.tle_first_line_list, \
            self.tle_second_line_list

    def devuelve_lista(self, x):
        return 3 * x

    def pyephem_routine(self, name, line1, line2):

        satellite = ephem.readtle(name, line1, line2)
        satellite.compute(self.observer)

        self.inclination = degrees(satellite._inc)
        self.mean_motion = satellite._n
        self.epoch = satellite._epoch

    def get_location(self):
        # todo
        # load from settings
        lon = '-2.314722'
        lat = '36.832778'
        ele = 20

        return lon, lat, ele

    def solve_coordinates(self, index):

        self.observer = Observer()
        (lon, lat, ele) = self.get_location()

        self.observer.lon = degrees(lon)
        self.observer.lat = degrees(lat)
        self.observer.elevation = ele

        self.observer.date = now()
        self.observer.epoch = now()

        for i in range(index):
            self.pyephem_routine(self.show_satellite_list[i],
                                 self.tle_first_line_list[i],
                                 self.tle_second_line_list[i])
