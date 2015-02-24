# -*- encoding: utf-8 -*-

from math import degrees
from os import getcwd, chdir

import ephem
from ephem import Observer, now


class Get_elements(object):

    def __init__(self, file, index):

        self.index = index + 1
        file = str(file)

        actual_dir = getcwd()
        chdir(actual_dir + '/TLEs')

        open_tle = open(file, 'r')
        lista_nombres_satelites = open_tle.readlines()
        lista_nombres_satelites = [
            item.rstrip('\n') for item in lista_nombres_satelites]

        chdir(actual_dir)

        list_length = len(lista_nombres_satelites)
        y = list_length / 3

        numbers_list = list(map(self.devuelve_lista, list(range(y))))

        lista_satelites = []
        lista_linea1 = []
        lista_linea2 = []
        i = 0
        j = 1
        k = 2

        for i in range(len(numbers_list)):
            lista_satelites.append(lista_nombres_satelites[numbers_list[i]])
            lista_linea1.append(lista_nombres_satelites[j])
            lista_linea2.append(lista_nombres_satelites[k])
            j = numbers_list[i] + 4
            k = numbers_list[i] + 5

        self.solve_coordinates(lista_satelites, lista_linea1, lista_linea2)

    def devuelve_lista(self, x):
        return 3 * x

    def solve_coordinates(self, satellites, lines1, lines2):

        self.observer = Observer()
        (lon, lat, ele) = self.get_location()

        self.observer.lon = degrees(lon)
        self.observer.lat = degrees(lat)
        self.observer.elevation = ele

        self.observer.date = now()
        self.observer.epoch = now()

        for i in range(self.index):
            self.pyephem_routine(satellites[i], lines1[i], lines2[i])

    def pyephem_routine(self, name, line1, line2):

        satellite = ephem.readtle(name, line1, line2)
        satellite.compute(self.observer)

        # Inclinacion en grados.
        self.inclination = satellite._inc

        self.inclination = degrees(self.inclination)
        self.mean_motion = satellite._n
        self.epoch = satellite._epoch

    # No es relevante. Comprobar.
    def get_location(self):
        lon = '-2.314722'
        lat = '36.832778'
        ele = 20

        return lon, lat, ele


class Get_name(object):

    def __init__(self, index):
        actual_dir = getcwd()

        chdir(actual_dir + '/results/predict')

        open_temp = open('temp', 'r')
        names_list = open_temp.readlines()
        names_list = [item.rstrip('\n') for item in names_list]
        names_list = [item.rstrip('\r') for item in names_list]
        names_list = [item.strip() for item in names_list]

        self.name = names_list[index]

        chdir(actual_dir)


class Get_names(object):

    def __init__(self):

        actual_dir = getcwd()

        chdir(actual_dir + '/results/predict')

        open_temp = open('temp', 'r')
        names_list = open_temp.readlines()
        names_list = [item.rstrip('\n') for item in names_list]
        names_list = [item.rstrip('\r') for item in names_list]
        names_list = [item.strip() for item in names_list]

        self.names_list = names_list

        chdir(actual_dir)


class Get_list_length(object):

    def __init__(self):

        actual_dir = getcwd()
        chdir(actual_dir + '/results/predict')

        open_temp = open('temp', 'r')
        names_list = open_temp.readlines()

        chdir(actual_dir)

        self.length = len(names_list)
