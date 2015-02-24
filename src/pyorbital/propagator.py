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
import datetime
import os

from pyorbital.orbital import Orbital

from src.base.basepropagator import BasePropagator


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
                                         start_time, end_time)

        self._predict(satellite_info)

    def get_satellite(self, tle0, tle1, tle2):
        return Orbital(
            tle0,
            line1=tle1,
            line2=tle2)

    def predict(self, satellite_name, line1, line2, i):

        satellite = self.get_satellite(satellite_name, line1, line2)

        iterations = self.end_time - self.start_time
        iterations -= 1

        time1 = datetime.datetime.fromtimestamp(self.start_time)

        (lon, lat, ele) = self.get_location()

        az1, alt1 = satellite.get_observer_look(time1, lon, lat, ele)

        output_filepath = os.path.join(self.output_folder,
                                       satellite_name)
        if alt1 > 0:
            self.save(output_filepath, self.start_time, alt1, az1)

        n2 = self.start_time

        for j in range(iterations):
            n2 += 1
            timeN = datetime.datetime.fromtimestamp(n2)
            azN, altN = satellite.get_observer_look(timeN, lon, lat, ele)

            if altN > 0:
                self.save(output_filepath, n2, altN, azN)
