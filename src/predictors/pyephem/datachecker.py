# -*- encoding: utf-8 -*-
import os
from os import listdir

from src.base.datachecker import BaseDataChecker


class DataChecker(BaseDataChecker):

    def __init__(self, index_satellite, sat_name, folder):
        self.checker_name = 'pyephem'
        data_folder = os.path.join(folder, self.checker_name)
        super().__init__(index_satellite, sat_name, data_folder)

    def check(self, index, satellite_name=''):
        if not os.path.exists(self.data_folder):
            self.result = False
        else:
            files = listdir(self.data_folder)

            if satellite_name in files:
                self.result = True
            else:
                self.result = False
