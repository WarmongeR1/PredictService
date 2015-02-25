# -*- encoding: utf-8 -*-
from os import listdir
import os

from src.base.datachecker import BaseDataChecker


class DataChecker(BaseDataChecker):

    def __init__(self, index_satellite, sat_name, folder):
        super().__init__(index_satellite, sat_name, folder)
        self.checker_name = 'pyorbital'
        self.data_folder = os.path.join(self.data_folder, self.checker_name)

    def check(self, index, satellite_name=''):
        sat_name = 'SAT%s' % (index + 1)

        files = listdir(self.data_folder)

        if sat_name in files:
            self.result = 'yes'
        else:
            self.result = 'no'
