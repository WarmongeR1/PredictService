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

import progressbar
import pyorbital.orbital

from src.base.basepropagator import BasePropagator
from src.utils.reader import TleReader


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

        self.satellites_number = len(satellite_info[0])

        bar = progressbar.ProgressBar(maxval=len(satellite_info[0]))
        bar.start()

        # Provide data to pyephem_routine
        for i in range(len(satellite_info[0])):
            self.predict(satellite_info[0][i], satellite_info[1][i],
                         satellite_info[2][i], i)
            i = i + 1
            bar.update(i + 1)

        bar.finish()

    def get_satellite(self, tle0, tle1, tle2):
        return pyorbital.orbital.Orbital(
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
            self.output_data(output_filepath, self.start_time, alt1, az1)

        n2 = self.start_time

        for j in range(iterations):
            n2 += 1
            timeN = datetime.datetime.fromtimestamp(n2)
            azN, altN = satellite.get_observer_look(timeN, lon, lat, ele)

            if altN > 0:


                self.output_data(output_filepath, n2, altN, azN)


def main():
    print()
    print("PyOrbit data")
    filpeath = '/home/warmonger/Develop/Github/propagators/bin/TLEs/dmc.txt'
    output_folder = '/home/warmonger/Develop/Github/propagators/bin/result/PyOrbital'
    obj = TleReader()
    obj.read(filpeath)

    # Time will be in UNIX units
    solve_coordinates = Propagator(
        obj.get(), output_folder)


if __name__ == '__main__':
    main()
