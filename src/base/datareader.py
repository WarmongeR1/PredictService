# -*- encoding: utf-8 -*-


class BaseDataReader(object):
    def __init__(self, *args):
        pass

    def _open(self):
        pass

    def open_files(self, index_satellite):
        pass

    def open_file(self, name):
        pass

    def get(self):
        pass

