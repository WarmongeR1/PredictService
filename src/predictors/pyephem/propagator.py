# -*- encoding: utf-8 -*-

import math
import os

import ephem
from dateconv import d2u, g2l, h2d, h2u, l2g, u2d, u2h

from src.base.propagator import BasePropagator


class Propagator(BasePropagator):

    def __init__(self, satellite_info,
                 output_folder,
                 start_time=None,
                 end_time=None):
        """

        :param satellite_info: tuple with 3 elements (element = list)
        :param output_folder:  string
        :param start_time:  human time, example '2015-01-01_18:21:26'
        :param end_time:  human time, example '2015-01-01_18:21:26'
        :return:
        """
        start_time = u2d(l2g(start_time, view='%Y-%m-%d_%H:%M:%S'))
        end_time = u2d(l2g(end_time, view='%Y-%m-%d_%H:%M:%S'))

        super(Propagator, self).__init__(output_folder,
                                         start_time,
                                         end_time)

        self.satellites_number = len(satellite_info[0])
        self.observer = self.gen_observer()

        self._predict(satellite_info)

    def get_satellite(self, tle0, tle1, tle2):
        satellite = ephem.readtle(tle0, tle1, tle2)
        satellite.compute(self.observer)
        return satellite

    def _step(self, satellite, time, output_filepath):
        self.observer.date = u2h(time)
        satellite.compute(self.observer)
        alt1 = math.degrees(satellite.alt)
        az1 = math.degrees(satellite.az)
        if alt1 >= 0:
            self.save(output_filepath, g2l(time),
                      alt1, az1)

    def predict(self, satellite_name, line1, line2, i):

        satellite = self.get_satellite(satellite_name, line1, line2)

        output_filepath = os.path.join(self.output_folder,
                                       satellite_name)
        cur_time = self.start_time
        self._step(satellite, cur_time, output_filepath)

        while cur_time < self.end_time:
            cur_time += 1
            self._step(satellite, cur_time, output_filepath)

    def gen_observer(self):
        observer = ephem.Observer()

        (lon, lat, ele) = self.get_location()

        observer.lon = ephem.degrees(lon)
        observer.lat = ephem.degrees(lat)
        observer.elevation = ele

        observer.date = ephem.now()
        observer.epoch = ephem.now()

        observer.horizon = '0'

        return observer
