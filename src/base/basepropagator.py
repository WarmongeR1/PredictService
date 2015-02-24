# -*- encoding: utf-8 -*-
import os


class BasePropagator(object):

    def get_location(self):
        # todo
        # вынести в нормальный конфиг
        open_file = open(os.getenv("HOME") + '/.predict/predict.qth')
        lines = open_file.readlines()
        lines = [item.rstrip('\n') for item in lines]

        lat = lines[1]
        lon = lines[2]
        ele = int(lines[3])

        return lon, lat, ele

    def check_create(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def output_data(self, output_filepath, time, alt, az):
        with open(output_filepath, 'a') as file:
            file.writelines("%d\t" % time)
            file.writelines("%0.6f\t" % alt)
            file.writelines("%0.6f\n" % az)
