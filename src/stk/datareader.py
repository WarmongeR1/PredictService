# -*- encoding: utf-8 -*-
import csv
from os import listdir
import os

from src.base.datareader import BaseDataReader


class DataReader(BaseDataReader):

    def __init__(self, data_folder, index_satellite, *args):
        super().__init__(*args)
        index_satellite = index_satellite
        self.data_folder = data_folder

        self._open()
        self.open_files(index_satellite)

    def _open(self):

        self.files_STK = listdir(self.data_folder)
        self.files_STK.sort()

    def open_files(self, index_satellite):

        open_file = open(os.path.join(self.data_folder, 'temp'))
        copy_names = open_file.readlines()
        copy_names = [item.rstrip('\n\r') for item in copy_names]
        copy_names = [item.strip() for item in copy_names]

        satellite = copy_names[index_satellite].replace(' ', '_')

        for i in range(len(copy_names)):
            if satellite in self.files_STK[i]:
                name = self.files_STK[i]
                self.open_file(name)

    def open_file(self, name):
        with open(name, 'rb') as open_file:
            reader = csv.reader(open_file)
            for row in reader:
                try:
                    valor = int((float(row[0]) - 2440587.5) * 86400)
                    self.simulation_time.append(int(valor))
                    self.az_satellite.append(float(row[1]))
                    self.alt_satellite.append(float(row[2]))
                except Exception as e:
                    print(e)
