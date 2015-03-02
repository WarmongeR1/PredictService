# -*- encoding: utf-8 -*-
import os
from os import listdir

from src.base.datachecker import BaseDataChecker


class DataChecker(BaseDataChecker):

    def __init__(self, index_satellite, sat_name, folder):
        self.checker_name = 'stk'
        data_folder = os.path.join(folder, self.checker_name)
        super().__init__(index_satellite, sat_name, data_folder)

    def check(self, index, satellite_name=''):
        if os.path.exists(self.data_folder):
            if index < len(listdir(self.data_folder)) - 1:  # minus temp file
                self.result = True
            else:
                self.result = False
        else:
            self.result = False
