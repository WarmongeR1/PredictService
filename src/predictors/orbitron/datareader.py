# -*- encoding: utf-8 -*-
import datetime
import os

from src.base.datareader import BaseDataReader
from src.utils.common import local_to_unix


class DataReader(BaseDataReader):

    def __init__(self, data_folder, index_satellite, *args):
        super().__init__(*args)

        self.lineas_validas = []
        self.satellite_name = None
        self.reader_name = 'orbitron'
        self.data_folder = os.path.join(data_folder, self.reader_name)
        self.files = []
        self.open_file(args[0])

    def open_file(self, sat_name):
        filepath = os.path.join(self.data_folder, '/output.txt')

        with open(filepath, 'r') as fi:
            file_lines_converted = [x.rstrip('\r\n') for x in fi.readlines()]

        for i in range(len(file_lines_converted)):
            self.extract_data(file_lines_converted[i])

        self.lineas_validas = []
        self.process_data(sat_name)

    def extract_data(self, line):
        if line[0:4] == str(datetime.datetime.now().year()):
            self.lineas_validas.append(line)

    def process_data(self, sat_selected):
        for i in range(len(self.lineas_validas)):
            sat_name = self.lineas_validas[i][20:36]
            sat_name = sat_name.strip(' ')

            if sat_name == sat_selected:
                year = self.lineas_validas[i][0:4]
                month = self.lineas_validas[i][5:7]
                day = self.lineas_validas[i][8:10]
                hour = self.lineas_validas[i][11:13]
                minute = self.lineas_validas[i][14:16]
                second = self.lineas_validas[i][17:19]

                unix_time = local_to_unix(
                    year,
                    month,
                    day,
                    hour,
                    minute,
                    second)

                az = self.lineas_validas[i][41:46]
                alt = self.lineas_validas[i][47:51]
                alt = alt.strip(' ')
                az = az.strip(' ')

                self.simulation_time.append(int(unix_time))
                self.az_satellite.append(float(az))
                self.alt_satellite.append(float(alt))
                break
