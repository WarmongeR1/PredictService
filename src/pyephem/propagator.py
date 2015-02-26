# -*- encoding: utf-8 -*-

##########################################################################
# Copyright 2014 Sapronov Alexander (sapronov.alexander92@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##########################################################################
# Author: sapronov.alexander92[at]gmail.com
##########################################################################
import os
import math

from dateconv import d2u
import ephem

from src.base.propagator import BasePropagator


class Propagator(BasePropagator):

    def __init__(self, satellite_info,
                 output_folder,
                 start_time=None,
                 end_time=None):
        """

        :param satellite_info: tuple with 3 elements (element = list)
        :param output_folder:  string
        :param start_time:  human time, example '2015-01-01 18:21:26'
        :param end_time:  human time, example '2015-01-01 18:21:26'
        :return:
        """

        super(Propagator, self).__init__(output_folder,
                                         start_time, end_time)

        self.satellites_number = len(satellite_info[0])
        self.observer = self.gen_observer()

        self._predict(satellite_info)

    def get_satellite(self, tle0, tle1, tle2):
        satellite = ephem.readtle(tle0, tle1, tle2)
        satellite.compute(self.observer)
        return satellite

    def predict(self, satellite_name, line1, line2, i):

        satellite = self.get_satellite(satellite_name, line1, line2)

        iterations = self.end_time - self.start_time
        iterations -= 1

        self.observer.date = self.start_time

        satellite.compute(self.observer)
        alt1 = float(repr(satellite.alt))
        alt1 = math.degrees(alt1)
        az1 = float(repr(satellite.az))
        az1 = math.degrees(az1)
        output_filepath = os.path.join(self.output_folder,
                                       satellite_name)
        if alt1 >= 0:
            self.save(output_filepath, self.start_time, alt1, az1)

        for j in range(iterations):
            time = ephem.Date(self.observer.date + ephem.second)
            self.observer.date = time

            satellite.compute(self.observer)
            alt = float(repr(satellite.alt))
            alt = math.degrees(alt)
            az = float(repr(satellite.az))
            az = math.degrees(az)
            if alt >= 0:
                self.save(output_filepath, d2u(self.observer.date), alt, az)

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
