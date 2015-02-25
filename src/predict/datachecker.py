# -*- encoding: utf-8 -*-
from os import listdir

from src.base.datachecker import BaseDataChecker


class DataChecker(BaseDataChecker):

    def check(self, index, satellite_name=''):
        sat_name = 'SAT%s' % (index + 1)

        files = listdir(self.data_folder)

        if sat_name in files:
            self.result = 'yes'
        else:
            self.result = 'no'
