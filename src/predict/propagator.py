# -*- encoding: utf-8 -*-

import os
import re
import tempfile
import subprocess

from dateconv import u2d, l2g

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
        start_time = u2d(l2g(start_time, view='%Y-%m-%d_%H:%M:%S'))
        end_time = u2d(l2g(end_time, view='%Y-%m-%d_%H:%M:%S'))

        super(Propagator, self).__init__(output_folder,
                                         start_time,
                                         end_time)
        self._predict(satellite_info)

    def predict(self, satellite_name, line1, line2, i):
        output_filepath = os.path.join(self.output_folder,
                                       satellite_name)

        sat_name = "SAT"
        sat_text = "{}\n{}\n{}\n".format(
            sat_name,
            line1,
            line2
        )

        fd, filename = tempfile.mkstemp()
        out_path = os.path.join('/tmp', '__preidct__data.out')
        self.remove(out_path)

        regexp = r'(\d+) ((\w+ ){2}\d+:\d+:\d+)  (\s*-?\d+)  (\s*-?\d+)  (\s*-?\d+)  (\s*-?\d+)  (\s*-?\d+)  (\s*-?\d+)  (\s*-?\d+)'
        reg = re.compile(regexp)
        sat_file = open(output_filepath, 'a')

        try:
            f = os.fdopen(fd, 'w')
            f.write(sat_text)
            f.close()

            command = "predict -t {} -f {} {} {} -o {}".format(
                filename,
                sat_name,
                self.start_time,
                self.end_time,
                out_path,
            )
            subprocess.call(command, stdout=subprocess.PIPE, shell=True)

            with open(out_path, 'r') as fio:
                lines = fio.readlines()

            for line in lines:
                res = reg.match(line)
                if res is not None:
                    info = res.groups()
                    time = info[0]
                    elevation = info[3]
                    azimuth = info[4]
                    # phase = info[5]
                    # lat = info[6]
                    # lon = info[7]
                    sat_file.write("%s\t%s\t%s\n" % (time, elevation, azimuth))
        finally:
            os.remove(filename)
            sat_file.close()
            os.remove(out_path)



