# -*- encoding: utf-8 -*-
import numpy


class BaseComparator(object):

    def __init__(self, data_folder, index_first,
                 index_second, first_reader, second_reader):
        self.data_folder_first = data_folder
        self.data_folder_second = data_folder
        self.index_first = index_first
        self.index_second = index_second

        self.second_reader = second_reader
        self.second_times = []
        self.second_alts = []
        self.second_azs = []

        self.first_reader = first_reader
        self.first_times = []
        self.first_alts = []
        self.first_azs = []

    def _prepare(self, first=True):
        if first:
            reader = self.first_reader(self.data_folder_first,
                                       self.index_first)
        else:
            reader = self.second_reader(self.data_folder_second,
                                        self.index_second)

        times = [int(item) for item in reader.get_sim_time()]
        alts = [float(item) for item in reader.get_alts()]
        azs = [float(item) for item in reader.get_azs()]

        return times, alts, azs

    def prepare_second(self):
        self.second_times, self.second_alts, self.second_azs = self._prepare(
            False)

    def prepare_first(self):
        self.first_times, self.first_alts, self.first_azs = self._prepare(True)

    def _compare(self):
        self.prepare_first()
        self.prepare_second()

        # Differences
        list_alt = []
        list_az = []

        time_intersected = list(
            set(self.first_times).intersection(self.second_times))
        # todo
        # времена расчетов не совпадают
        for i in range(len(time_intersected)):
            difference_alt = \
                float(self.second_alts[
                    self.second_times.index(time_intersected[i])]) - \
                float(
                    self.first_alts[
                        self.first_times.index(
                            time_intersected[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(self.second_azs[
                    self.second_times.index(time_intersected[i])]) - \
                float(
                    self.first_azs[
                        self.first_times.index(
                            time_intersected[i])])

            list_az.append(difference_az)

        return time_intersected, list_alt, list_az

    def compare_deviation(self):
        _, list_alt, list_az = self._compare()
        # Force mean to zero
        m = 0

        alt = numpy.asarray(list_alt)
        az = numpy.asarray(list_az)

        # Standard deviation
        std_alt = numpy.sqrt(numpy.mean((alt - m) ** 2))
        std_az = numpy.sqrt(numpy.mean((az - m) ** 2))

        return std_alt, std_az

    def compare(self):
        return self._compare()
