# -*- encoding: utf-8 -*-
from os import listdir
import os

from src.base.datachecker import BaseDataChecker


class DataChecker(BaseDataChecker):

    def __init__(self, index_satellite, sat_name, folder):
        self.checker_name = 'pyorbital'
        data_folder = os.path.join(folder, self.checker_name)
        super().__init__(index_satellite, sat_name, data_folder)


    def check(self, index, satellite_name=''):
        sat_name = 'SAT%s' % (index + 1)

        files = listdir(self.data_folder)

        if sat_name in files:
            self.result = True
        else:
            self.result = False

