# -*- encoding: utf-8 -*-
import csv
import os

from src.base.datareader import BaseDataReader


class DataReader(BaseDataReader):
    def __init__(self, data_folder, index_satellite):
        super().__init__(data_folder, index_satellite)
        self.simulation_time = []
        self.alt_satellite = []
        self.az_satellite = []
        self.satellite_name = None
        self.data_folder = data_folder
        index_satellite += 1
        self._open()
        self.open_files(index_satellite)

    def _open(self):
        self.files_pyephem = os.listdir(self.data_folder)
        if 'temp' in self.files_pyephem:
            self.files_pyephem.remove('temp')
        self.files_pyephem.sort()

    def open_files(self, index_satellite):

        for i in range(index_satellite):
            self.open_file(self.files_pyephem[i])
            self.satellite_name = self.files_pyephem[i]

    def open_file(self, name):

        with open(os.path.join(self.data_folder, name)) as tsv:
            for line in csv.reader(tsv, delimiter="\t"):
                self.simulation_time.append(int(line[0]))
                self.alt_satellite.append(float(line[1]))
                self.az_satellite.append(float(line[2]))

    def get(self):
        return self.simulation_time, self.alt_satellite, self.az_satellite


if __name__ == '__main__':
    obj = DataReader(
        '/home/warmonger/Develop/Github/propagators/bin/result/PyEphem', 1)
    print(obj.get())