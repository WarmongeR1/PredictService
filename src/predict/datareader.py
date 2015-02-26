# -*- encoding: utf-8 -*-

import csv
import os

from src.base.datareader import BaseDataReader


class DataReader(BaseDataReader):

    def __init__(self, data_folder, index_satellite, *args):
        super().__init__(*args)

        self.satellite_name = None
        self.reader_name = 'predict'
        self.data_folder = os.path.join(data_folder, self.reader_name)
        self.files = []
        index_satellite += 1
        self._open()
        self.open_files(index_satellite)

    def _open(self):
        self.files = os.listdir(self.data_folder)
        if 'temp' in self.files:
            self.files.remove('temp')
        self.files.sort()

    def open_files(self, index_satellite):

        for i in range(index_satellite):
            self.open_file(self.files[i])
            self.satellite_name = self.files[i]

    def open_file(self, name):

        with open(os.path.join(self.data_folder, name)) as tsv:
            for line in csv.reader(tsv, delimiter='\t'):
                self.simulation_time.append(int(line[0]))
                self.alt_satellite.append(float(line[1]))
                self.az_satellite.append(float(line[2]))
