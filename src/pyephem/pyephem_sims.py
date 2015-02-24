# -*- encoding: utf-8 -*-

##########################################################################
# Copyright 2014 Samuel Gongora Garcia (s.gongoragarcia@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##########################################################################
# Author: s.gongoragarcia[at]gmail.com
##########################################################################

from os import chdir
from os import getenv
from sys import argv
from os import getcwd
import sys

import ephem
import math


class Do_list(object):

    def __init__(self):

        open_tle = open(getcwd() + '/TLEs/' + argv[1], 'r')
        satellite_list = open_tle.readlines()
        satellite_list = [item.rstrip('\n') for item in satellite_list]

        length_list = len(satellite_list)
        y = length_list / 3

        list_numbers = list(map(self.return_list, list(range(y))))

        self.show_satellite_list = []
        self.tle_first_line_list = []
        self.tle_second_line_list = []
        i = 0
        j = 1
        k = 2

        for i in range(len(list_numbers)):
            self.show_satellite_list.append(satellite_list[list_numbers[i]])
            self.tle_first_line_list.append(satellite_list[j])
            self.tle_second_line_list.append(satellite_list[k])
            j = list_numbers[i] + 4
            k = list_numbers[i] + 5

        # Funcion para sacar los valores de la clase
        self.return_values()

    def return_list(self, x):
        return 3 * x

    def return_values(self):
        return self.show_satellite_list
        return self.tle_first_line_list
        return self.tle_second_line_list


class Solve_coordinates(object):

    def __init__(self, satellites_name, lista_prueba, lista_prueba2):

        self.satellites_number = len(satellites_name)

        self.observer = ephem.Observer()

        (lon, lat, ele) = self.get_location()

        self.observer.lon = ephem.degrees(lon)
        self.observer.lat = ephem.degrees(lat)
        self.observer.elevation = ele

        self.observer.date = ephem.now()
        self.observer.epoch = ephem.now()

        self.observer.horizon = '0'

        # TO-DO
#		import progressbar
#		bar = progressbar.ProgressBar(maxval=len(satellites_name), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

        # Provide data to pyephem_routine
        for i in range(len(satellites_name)):
            self.pyephem_routine(
                satellites_name[i],
                lista_prueba[i],
                lista_prueba2[i],
                i)
            i = i + 1
#			bar.update(i+1)

#		bar.finish()

    def pyephem_routine(self, satellite_name, line1, line2, i):

        satellite = ephem.readtle(satellite_name, line1, line2)
        satellite.compute(self.observer)

        start_time = int(sys.argv[2])
        end_time = int(sys.argv[3])

        iterations = end_time - start_time
        iterations = iterations - 1

        n1 = (start_time + 2440587.5 * 86400) / 86400 - 2415020

        self.observer.date = n1

        satellite.compute(self.observer)
        alt1 = float(repr(satellite.alt))
        alt1 = math.degrees(alt1)
        az1 = float(repr(satellite.az))
        az1 = math.degrees(az1)
        if alt1 >= 0:
            self.output_data(satellite_name, start_time, alt1, az1)

        for j in range(iterations):
            time = ephem.Date(self.observer.date + ephem.second)
            self.observer.date = time

            # UNIX Time
            UnixTimeN = float(time)
            UnixTimeN = int((UnixTimeN - 25567.5) * 86400)

            satellite.compute(self.observer)
            altN = float(repr(satellite.alt))
            altN = math.degrees(altN)
            azN = float(repr(satellite.az))
            azN = math.degrees(azN)
            if altN >= 0:
                self.output_data(satellite_name, UnixTimeN, altN, azN)

            j = j + 1
        i = i + 1
        print((
            "PyEphem - Simulation [%s/%d] done!" %
            (i, self.satellites_number)))

    def output_data(self, name, time, alt, az):

        script_dir = getcwd()
        chdir(script_dir + '/results/PyEphem')

        create_file = open(name, 'a')
        create_file.writelines("%d\t" % time)
        create_file.writelines("%0.6f\t" % alt)
        create_file.writelines("%0.6f\n" % az)
        create_file.close()

        chdir(script_dir)

    def get_location(self):

        open_file = open(getenv("HOME") + '/.predict/predict.qth')
        lines = open_file.readlines()
        lines = [item.rstrip('\n') for item in lines]

        lines[0]
        lat = lines[1]
        lon = lines[2]
        ele = int(lines[3])

        return lon, lat, ele

if __name__ == '__main__':
    print()
    print("PyEphem data")
    do_list = Do_list()

    # Time will be in UNIX units
    solve_coordinates = Solve_coordinates(
        do_list.show_satellite_list,
        do_list.tle_first_line_list,
        do_list.tle_second_line_list)