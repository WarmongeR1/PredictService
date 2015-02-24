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


from os import listdir
from datetime import datetime
import csv
import os
from os import getcwd, chdir

import numpy





class Read_data(object):

    def __init__(self, index_pyephem, index_predict, index_pyorbital,
                 index_orbitron, sat_selected, index_STK, STK_dir, orbitron_dir):

        # Orbitron stuff
        self.file = '/home/case/Orbitron/Output/output.txt'
        self.index_orbitron = index_orbitron + 1
        self.sat_selected = sat_selected
        # PyEphem stuff
        self.index_pyephem = index_pyephem
        # predict stuff
        self.index_predict = index_predict + 1
        # PyOrbital stuff
        self.index_pyorbital = index_pyorbital
        # STK stuff
        self.index_STK = index_STK
        self.STK_dir = STK_dir
        self.orbitron_dir = orbitron_dir

        self.directorio_script = getcwd()

    def STK_vs_predict(self):

        # STK routine
        directorio_script = getcwd()
        self.open_STK(self.STK_dir)
        self.open_files_STK(self.index_STK, directorio_script)
        chdir(directorio_script)

        # predict routine
        self.open_predict(directorio_script)
        self.open_files_predict()

        # Differences
        list_alt = []
        list_az = []

        time_intersected_predict = []
        time_intersected_predict = list(
            set(self.STK_simulation_time).intersection(self.predict_simulation_time))

        i = 0

        for i in range(len(time_intersected_predict)):

            difference_alt = \
                float(self.predict_alt_satellite[self.predict_simulation_time.index(time_intersected_predict[i])]) - \
                float(
                    self.STK_alt_satellite[
                        self.STK_simulation_time.index(
                            time_intersected_predict[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(self.predict_az_satellite[self.predict_simulation_time.index(time_intersected_predict[i])]) - \
                float(
                    self.STK_az_satellite[
                        self.STK_simulation_time.index(
                            time_intersected_predict[i])])

            list_az.append(difference_az)

            i = i + 1

        # Force mean to zero
        m = 0

        alt = numpy.asarray(list_alt)
        az = numpy.asarray(list_az)

        # Standard deviation
        std_alt = numpy.sqrt(numpy.mean((alt - m) ** 2))
        std_az = numpy.sqrt(numpy.mean((az - m) ** 2))

        chdir(self.directorio_script)

        return std_alt, std_az

    def STK_vs_predict_comp(self):

        # STK routine

        directorio_script = getcwd()
        self.open_STK(self.STK_dir)
        self.open_files_STK(self.index_STK, directorio_script)
        chdir(directorio_script)

        # predict routine
        self.open_predict(directorio_script)
        self.open_files_predict()

        # Differences
        list_alt = []
        list_az = []

        time_intersected_predict = []
        time_intersected_predict = list(
            set(self.STK_simulation_time).intersection(self.predict_simulation_time))

        i = 0

        for i in range(len(time_intersected_predict)):

            difference_alt = \
                float(self.predict_alt_satellite[self.predict_simulation_time.index(time_intersected_predict[i])]) - \
                float(
                    self.STK_alt_satellite[
                        self.STK_simulation_time.index(
                            time_intersected_predict[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(self.predict_az_satellite[self.predict_simulation_time.index(time_intersected_predict[i])]) - \
                float(
                    self.STK_az_satellite[
                        self.STK_simulation_time.index(
                            time_intersected_predict[i])])

            list_az.append(difference_az)

            i = i + 1

        chdir(self.directorio_script)

        return time_intersected_predict, list_alt, list_az

    def STK_vs_PyEphem(self):

        chdir(self.directorio_script)

        object_pyephem = Read_pyephem_data(self.index_pyephem)

        pyephem_time = object_pyephem.pyephem_simulation_time
        pyephem_time = [int(item) for item in pyephem_time]

        pyephem_alt = object_pyephem.pyephem_alt_satellite
        pyephem_alt = [float(item) for item in pyephem_alt]

        pyephem_az = object_pyephem.pyephem_az_satellite
        pyephem_az = [float(item) for item in pyephem_az]

        # Differences
        list_alt = []
        list_az = []

        time_intersected = []
        time_intersected = list(
            set(self.STK_simulation_time).intersection(pyephem_time))

        i = 0

        for i in range(len(time_intersected)):

            difference_alt = \
                float(pyephem_alt[pyephem_time.index(time_intersected[i])]) - \
                float(
                    self.STK_alt_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(pyephem_az[pyephem_time.index(time_intersected[i])]) - \
                float(
                    self.STK_az_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_az.append(difference_az)

            i = i + 1

        # Force mean to zero
        m = 0

        alt = numpy.asarray(list_alt)
        az = numpy.asarray(list_az)

        # Standard deviation
        std_alt = numpy.sqrt(numpy.mean((alt - m) ** 2))
        std_az = numpy.sqrt(numpy.mean((az - m) ** 2))

        chdir(self.directorio_script)

        return std_alt, std_az

    def STK_vs_PyEphem_comp(self):

        # STK routine

        directorio_script = getcwd()
        self.open_STK(self.STK_dir)
        self.open_files_STK(self.index_STK, directorio_script)
        chdir(directorio_script)

        chdir(self.directorio_script)

        object_pyephem = Read_pyephem_data(self.index_pyephem)

        pyephem_time = object_pyephem.pyephem_simulation_time
        pyephem_time = [int(item) for item in pyephem_time]

        pyephem_alt = object_pyephem.pyephem_alt_satellite
        pyephem_alt = [float(item) for item in pyephem_alt]

        pyephem_az = object_pyephem.pyephem_az_satellite
        pyephem_az = [float(item) for item in pyephem_az]

        # Differences
        list_alt = []
        list_az = []

        time_intersected = []
        time_intersected = list(
            set(self.STK_simulation_time).intersection(pyephem_time))

        i = 0

        for i in range(len(time_intersected)):

            difference_alt = \
                float(pyephem_alt[pyephem_time.index(time_intersected[i])]) - \
                float(
                    self.STK_alt_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(pyephem_az[pyephem_time.index(time_intersected[i])]) - \
                float(
                    self.STK_az_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_az.append(difference_az)

            i = i + 1

        chdir(self.directorio_script)

        return time_intersected, list_alt, list_az

    def STK_vs_PyOrbital(self):

        chdir(self.directorio_script)

        object_pyorbital = Read_pyorbital_data(self.index_pyorbital)

        pyorbital_time = object_pyorbital.pyorbital_simulation_time
        pyorbital_time = [int(item) for item in pyorbital_time]

        pyorbital_alt = object_pyorbital.pyorbital_alt_satellite
        pyorbital_alt = [float(item) for item in pyorbital_alt]

        pyorbital_az = object_pyorbital.pyorbital_az_satellite
        pyorbital_az = [float(item) for item in pyorbital_az]

        # Differences
        list_alt = []
        list_az = []

        time_intersected = []
        time_intersected = list(
            set(self.STK_simulation_time).intersection(pyorbital_time))

        i = 0

        for i in range(len(time_intersected)):

            difference_alt = \
                float(pyorbital_alt[pyorbital_time.index(time_intersected[i])]) -\
                float(
                    self.STK_alt_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(pyorbital_az[pyorbital_time.index(time_intersected[i])]) - \
                float(
                    self.STK_az_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_az.append(difference_az)

            i = i + 1

        # Force mean to zero
        m = 0

        alt = numpy.asarray(list_alt)
        az = numpy.asarray(list_az)

        # Standard deviation
        std_alt = numpy.sqrt(numpy.mean((alt - m) ** 2))
        std_az = numpy.sqrt(numpy.mean((az - m) ** 2))

        chdir(self.directorio_script)

        return std_alt, std_az

    def STK_vs_PyOrbital_comp(self):

        # STK routine
        directorio_script = getcwd()
        self.open_STK(self.STK_dir)
        self.open_files_STK(self.index_STK, directorio_script)
        chdir(directorio_script)

        chdir(self.directorio_script)

        object_pyorbital = Read_pyorbital_data(self.index_pyorbital)

        pyorbital_time = object_pyorbital.pyorbital_simulation_time
        pyorbital_time = [int(item) for item in pyorbital_time]

        pyorbital_alt = object_pyorbital.pyorbital_alt_satellite
        pyorbital_alt = [float(item) for item in pyorbital_alt]

        pyorbital_az = object_pyorbital.pyorbital_az_satellite
        pyorbital_az = [float(item) for item in pyorbital_az]

        # Differences
        list_alt = []
        list_az = []

        time_intersected = []
        time_intersected = list(
            set(self.STK_simulation_time).intersection(pyorbital_time))

        i = 0

        for i in range(len(time_intersected)):

            difference_alt = \
                float(pyorbital_alt[pyorbital_time.index(time_intersected[i])]) -\
                float(
                    self.STK_alt_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(pyorbital_az[pyorbital_time.index(time_intersected[i])]) - \
                float(
                    self.STK_az_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_az.append(difference_az)

            i = i + 1

        chdir(self.directorio_script)

        return time_intersected, list_alt, list_az

    def STK_vs_Orbitron(self):

        object_orbitron = Read_orbitron_data(
            self.index_orbitron,
            self.sat_selected,
            self.orbitron_dir)
        orbitron_time = object_orbitron.orbitron_time
        orbitron_time = [int(item) for item in orbitron_time]

        orbitron_alt = object_orbitron.orbitron_alt_satellite
        orbitron_alt = [float(item) for item in orbitron_alt]

        orbitron_az = object_orbitron.orbitron_az_satellite
        orbitron_az = [float(item) for item in orbitron_az]

        # Differences
        list_alt = []
        list_az = []

        time_intersected = []
        time_intersected = list(
            set(self.STK_simulation_time).intersection(orbitron_time))

        for i in range(len(time_intersected)):

            difference_alt = \
                float(orbitron_alt[orbitron_time.index(time_intersected[i])]) -\
                float(
                    self.STK_alt_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(orbitron_az[orbitron_time.index(time_intersected[i])]) - \
                float(
                    self.STK_az_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_az.append(difference_az)

        # Force mean to zero
        m = 0

        alt = numpy.asarray(list_alt)
        az = numpy.asarray(list_az)

        # Standard deviation
        std_alt = numpy.sqrt(numpy.mean((alt - m) ** 2))
        std_az = numpy.sqrt(numpy.mean((az - m) ** 2))

        return std_alt, std_az

    def STK_vs_Orbitron_comp(self):

        # STK routine
        directorio_script = getcwd()
        self.open_STK(self.STK_dir)
        self.open_files_STK(self.index_STK, directorio_script)
        chdir(directorio_script)

        chdir(self.directorio_script)

        object_orbitron = Read_orbitron_data(
            self.index_orbitron,
            self.sat_selected,
            self.orbitron_dir)
        orbitron_time = object_orbitron.orbitron_time
        orbitron_time = [int(item) for item in orbitron_time]

        orbitron_alt = object_orbitron.orbitron_alt_satellite
        orbitron_alt = [float(item) for item in orbitron_alt]

        orbitron_az = object_orbitron.orbitron_az_satellite
        orbitron_az = [float(item) for item in orbitron_az]

        # Differences
        list_alt = []
        list_az = []

        time_intersected = []
        time_intersected = list(
            set(self.STK_simulation_time).intersection(orbitron_time))

        for i in range(len(time_intersected)):

            difference_alt = \
                float(orbitron_alt[orbitron_time.index(time_intersected[i])]) -\
                float(
                    self.STK_alt_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(orbitron_az[orbitron_time.index(time_intersected[i])]) - \
                float(
                    self.STK_az_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_az.append(difference_az)

        return time_intersected, list_alt, list_az

    # predict data
    def open_predict(self, script_dir):

        chdir(script_dir + '/results/predict')

        self.files_predict = listdir(getcwd())
        self.files_predict.remove('temp')
        self.files_predict.sort()

    def open_files_predict(self):

        for i in range(self.index_predict):
            self.open_file_predict(self.files_predict[i])

    def open_file_predict(self, name):

        self.predict_simulation_time = []
        self.predict_alt_satellite = []
        self.predict_az_satellite = []

        with open(name) as tsv:
            for line in csv.reader(tsv, delimiter="\t"):
                self.predict_simulation_time.append(int(line[0]))
                self.predict_alt_satellite.append(float(line[1]))
                self.predict_az_satellite.append(float(line[2]))

    def open_STK(self, directorio_datos):

        chdir(directorio_datos)

        self.files_STK = listdir(getcwd())
        self.files_STK.sort()

    def open_files_STK(self, index_satellite, script_dir):

        open_file = open(script_dir + '/results/PyEphem/temp')
        copy_names = open_file.readlines()
        copy_names = [item.rstrip('\n\r') for item in copy_names]
        copy_names = [item.strip() for item in copy_names]

        satellite = copy_names[index_satellite].replace(" ", "_")

        i = 0

        for i in range(len(copy_names)):
            if satellite in self.files_STK[i]:
                name = self.files_STK[i]

            i = i + 1

        self.open_file_STK(name)

    def open_file_STK(self, name):

        self.STK_simulation_time = []
        self.STK_alt_satellite = []
        self.STK_az_satellite = []

        with open(name, 'rb') as open_file:
            reader = csv.reader(open_file)
            for row in reader:
                # Tengo que comprobar si la linea esta vacia
                try:
                    valor = int((float(row[0]) - 2440587.5) * 86400)
                    self.STK_simulation_time.append(valor)
                    self.STK_az_satellite.append((row[1]))
                    self.STK_alt_satellite.append((row[2]))
                except:
                    pass


class Check_data(object):

    def __init__(self, index_satellite, sat_name, STK_folder, Orbitron_folder):

        index = index_satellite + 1
        satellite_name = "SAT%s" % (index)

        self.directorio_actual = getcwd()

        self.check_predict(index_satellite, satellite_name)
        self.check_pyephem(index_satellite, satellite_name)
        self.check_pyorbital(index_satellite, satellite_name)
        self.check_orbitron(index_satellite, sat_name, Orbitron_folder)
        self.check_STK(index_satellite, STK_folder)

        chdir(self.directorio_actual)

    def check_predict(self, index, satellite_name):

        chdir(self.directorio_actual + '/results/predict')

        files = listdir(getcwd())

        if satellite_name in files:
            self.predict = 'yes'
        else:
            self.predict = 'no'

    def check_pyephem(self, index, satellite_name):

        chdir(self.directorio_actual + '/results/PyEphem')

        files = listdir(getcwd())

        if satellite_name in files:
            self.pyephem = 'yes'
        else:
            self.pyephem = 'no'

    def check_pyorbital(self, index, satellite_name):

        chdir(self.directorio_actual + '/results/PyOrbital')

        files = listdir(getcwd())

        if satellite_name in files:
            self.pyorbital = 'yes'
        else:
            self.pyorbital = 'no'

    def check_orbitron(self, index, actual_sat_name, Orbitron_folder):

        file = Orbitron_folder + '/output.txt'

#		file = '/home/case/Orbitron/Output/output.txt'

        try:
            open_file = open(file, 'r')
            file_lines = open_file.readlines()

            file_lines_converted = []

            for i in range(len(file_lines)):
                file_lines_converted.append(file_lines[i].rstrip('\r\n'))

            lineas_validas = []
            for j in range(len(file_lines_converted)):
                if file_lines_converted[j][0:4] == '2014':
                    lineas_validas.append(file_lines_converted[j])

            sats_name = []
            for k in range(len(lineas_validas)):
                sat_name = lineas_validas[k][20:36]
                sat_name = sat_name.strip(' ')

                sats_name.append(sat_name)

            if actual_sat_name in sats_name:
                self.orbitron = 'yes'
            else:
                self.orbitron = 'no'

        # File not available
        except IOError:
            self.orbitron = 'no'

    def check_STK(self, index, STK_folder):
        from os import listdir

        if index < len(listdir(STK_folder)):
            self.STK = 'yes'
        else:
            self.STK = 'no'
