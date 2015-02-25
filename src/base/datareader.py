# -*- encoding: utf-8 -*-


class BaseDataReader(object):

    def __init__(self, *args):
        self.simulation_time = []
        self.alt_satellite = []
        self.az_satellite = []

    def _open(self):
        raise NotImplemented

    def open_files(self, index_satellite):
        raise NotImplemented

    def open_file(self, name):
        raise NotImplemented

    def get(self):
        return self.simulation_time, self.alt_satellite, self.az_satellite

    def get_sim_time(self):
        return self.simulation_time

    def get_alts(self):
        return self.alt_satellite

    def get_azs(self):
        return self.az_satellite
