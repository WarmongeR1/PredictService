# -*- encoding: utf-8 -*-

from src.base.datachecker import BaseDataChecker


class DataChecker(BaseDataChecker):

    def ckeck(self, index, satellite_name=''):
        from os import listdir

        if index < len(listdir(self.data_folder)):
            self.result = 'yes'
        else:
            self.result = 'no'
