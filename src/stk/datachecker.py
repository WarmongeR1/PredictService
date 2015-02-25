# -*- encoding: utf-8 -*-
import os

from src.base.datachecker import BaseDataChecker


class DataChecker(BaseDataChecker):

    def __init__(self, index_satellite, sat_name, folder):
        super().__init__(index_satellite, sat_name, folder)
        self.checker_name = 'stk'
        self.data_folder = os.path.join(self.data_folder, self.checker_name)

    def check(self, index, satellite_name=''):
        from os import listdir

        if index < len(listdir(self.data_folder)):
            self.result = 'yes'
        else:
            self.result = 'no'
