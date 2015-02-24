# -*- encoding: utf-8 -*-


class BaseDataChecker(object):

    def __init__(self, index_satellite, sat_name, folder):
        self.data_folder = folder
        self.ckeck(index_satellite, sat_name)
        self.result = 'no'

    def get(self):
        return self.result

    def ckeck(self, index, sat_name):
        raise NotImplemented
