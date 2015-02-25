# -*- encoding: utf-8 -*-
import os
from src.base.datachecker import BaseDataChecker


class DataChecker(BaseDataChecker):

    def __init__(self, index_satellite, sat_name, folder):
        super().__init__(index_satellite, sat_name, folder)
        self.checker_name = 'orbitron'
        self.data_folder = os.path.join(self.data_folder, self.checker_name)

    def check(self, index, sat_name):

        file = os.path.join(self.data_folder, 'output.txt')

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

            if sat_name in sats_name:
                self.result = 'yes'
            else:
                self.result = 'no'

        # File not available
        except IOError:
            self.result = 'no'
