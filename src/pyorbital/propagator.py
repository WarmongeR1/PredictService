# -*- encoding: utf-8 -*-

import os

from pyorbital.orbital import Orbital

from dateconv import h2d, u2d
from src.base.propagator import BasePropagator


class Propagator(BasePropagator):

    def __init__(self, satellite_info,
                 output_folder,
                 start_time=None,
                 end_time=None):
        """

        :param satellite_info: tuple with 3 elements (element = list)
        :param output_folder:  string
        :param start_time:  datetime object
        :param end_time:  datetime object
        :return:
        """
        super(Propagator, self).__init__(output_folder,
                                         h2d(start_time,
                                             view='%Y-%m-%d_%H:%M:%S'),
                                         h2d(end_time,
                                             view='%Y-%m-%d_%H:%M:%S'))
        self._predict(satellite_info)

    def get_satellite(self, tle0, tle1, tle2):
        return Orbital(
            tle0,
            line1=tle1,
            line2=tle2)

    def _step(self, satellite, filepath, time):
        lon, lat, ele = self.get_location()

        az1, alt1 = satellite.get_observer_look(u2d(time), lon, lat, ele)

        if alt1 > 0:
            self.save(filepath, time, alt1, az1)

    def predict(self, satellite_name, line1, line2, i):
        output_filepath = os.path.join(self.output_folder,
                                       satellite_name)

        satellite = self.get_satellite(satellite_name, line1, line2)

        cur_time = self.start_time
        self._step(satellite, output_filepath, cur_time)

        while cur_time < self.end_time:
            cur_time += 1
            self._step(satellite, output_filepath, cur_time)
