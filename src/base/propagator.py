# -*- encoding: utf-8 -*-
import datetime
import os

from dateconv import d2u
import progressbar


class BasePropagator(object):
    def __init__(self,
                 output_folder,
                 start_time=None,
                 end_time=None):
        """
        :param output_folder:  string
        :param start_time:  datetime object
        :param end_time:  datetime object
        :return:
        """

        if start_time is None:
            now = datetime.datetime.now()
            self.start_time = now
        else:
            self.start_time = start_time

        if end_time is None:
            self.end_time = self.start_time + datetime.timedelta(days=1)
        else:
            self.end_time = end_time

        if output_folder is None:
            self.output_folder = './results/propagator'
        else:
            self.output_folder = output_folder

        self.create(self.output_folder)

        self.start_time = d2u(self.start_time)
        self.end_time = d2u(self.end_time)

    def _predict(self, satellite_info):
        bar = progressbar.ProgressBar(maxval=len(satellite_info[0]))
        bar.start()

        for i in range(len(satellite_info[0])):
            self.remove(os.path.join(self.output_folder,
                                     satellite_info[0][i]))
            self.predict(satellite_info[0][i], satellite_info[1][i],
                         satellite_info[2][i], i)
            bar.update(i + 1)

        bar.finish()

    def get_location(self):
        # todo
        # вынести в нормальный конфиг
        open_file = open(os.getenv('HOME') + '/.predict/predict.qth')
        lines = open_file.readlines()
        lines = [item.rstrip('\n') for item in lines]

        lat = float(lines[1])
        lon = float(lines[2])
        ele = int(lines[3])

        return lon, lat, ele

    def create(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def remove(self, output_filepath):
        if os.path.exists(output_filepath):
            os.remove(output_filepath)

    def save(self, output_filepath, time, alt, az):
        with open(output_filepath, 'a') as file:
            file.writelines('%d\t' % time)
            file.writelines('%0.6f\t' % alt)
            file.writelines('%0.6f\n' % az)

    def predict(self, param, param1, param2, i):
        raise NotImplemented
