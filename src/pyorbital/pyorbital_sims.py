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
import datetime
import os
import sys
from os import getenv
from os import getcwd, chdir

import pyorbital.orbital


class Do_list(object):

    def __init__(self):
        actual_dir = getcwd()

        file = actual_dir + '/TLEs/' + sys.argv[1]

        open_tle = open(file, 'r')
        lista_nombres_satelites = open_tle.readlines()
        lista_nombres_satelites = [
            item.rstrip('\n') for item in lista_nombres_satelites]

        length_list = len(lista_nombres_satelites)
        y = length_list / 3

        list_numbers = list(map(self.return_list, list(range(y))))

        self.mostrar_lista_satelites = []
        self.mostrar_lista_linea1 = []
        self.mostrar_lista_linea2 = []
        i = 0
        j = 1
        k = 2

        for i in range(len(list_numbers)):
            self.mostrar_lista_satelites.append(
                lista_nombres_satelites[
                    list_numbers[i]])
            self.mostrar_lista_linea1.append(lista_nombres_satelites[j])
            self.mostrar_lista_linea2.append(lista_nombres_satelites[k])
            j = list_numbers[i] + 4
            k = list_numbers[i] + 5

            self.return_values()

    def return_list(self, x):

        return 3 * x

    def return_values(self):

        return self.mostrar_lista_satelites
        return self.mostrar_lista_linea1
        return self.mostrar_lista_linea2


class Solve_coordinates(object):

    def __init__(self, lista_elementos, lista_prueba, lista_prueba2):

        self.satellites_number = len(lista_elementos)
        self.get_location()

        # Provide data to pyephem_routine
        for i in range(len(lista_elementos)):
            j = i + 1
            try:
                self.pyephem_routine(
                    lista_elementos[i],
                    lista_prueba[i],
                    lista_prueba2[i],
                    i)
            except NotImplementedError:
                print((
                    "pyorbital - Simulation [%d/%d] error!" %
                    (j, len(lista_elementos))))
                print("Deep space satellite - Propagation not available")
            i = i + 1

    def pyephem_routine(self, satellite_name, line1, line2, i):

        satellite = pyorbital.orbital.Orbital(
            satellite_name,
            line1=line1,
            line2=line2)

#		start_time = int(sys.argv[2])
#		end_time = int(sys.argv[3])

        start_time = int(sys.argv[2])
        end_time = int(sys.argv[3])

        iterations = end_time - start_time
        iterations = iterations - 1

        time1 = datetime.datetime.fromtimestamp(start_time)

        (lon, lat, ele) = self.get_location()

        az1, alt1 = satellite.get_observer_look(time1, lon, lat, ele)

        if alt1 > 0:
            #			start_time = start_time + 3200
            self.output_data(satellite_name, start_time, alt1, az1)

#		start_time = start_time + 3200
#		self.output_data(satellite_name, start_time, alt1, az1)

        n2 = start_time

        for j in range(iterations):

            n2 = n2 + 1

            timeN = datetime.datetime.fromtimestamp(n2)

            azN, altN = satellite.get_observer_look(timeN, lon, lat, ele)

            if altN > 0:
                #				n2 = n2 + 3200
                output_filepath = os.path.join(self.output_folder,
                                               satellite_name)

                self.output_data(output_filepath, n2, altN, azN)

#			if altN >= 0:
#			n2 = n2 + 3200
#			self.output_data(satellite_name, n2, altN, azN)

            j = j + 1

        i = i + 1
        print((
            "PyOrbital - Simulation [%s/%d] done!" %
            (i, self.satellites_number)))

    def output_data(self, name, time, alt, az):

        script_dir = getcwd()
        chdir(script_dir + '/results/PyOrbital')

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

        lat = float(lines[1])
        lon = float(lines[2])
        ele = int(lines[3])

        return lon, lat, ele


if __name__ == '__main__':
    print()
    print("PyOrbital data")
    do_list = Do_list()

    solve_coordinates = Solve_coordinates(
        do_list.mostrar_lista_satelites,
        do_list.mostrar_lista_linea1,
        do_list.mostrar_lista_linea2)
