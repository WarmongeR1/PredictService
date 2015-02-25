# -*- encoding: utf-8 -*-


class STKvsPredictComparator(object):

    def STK_vs_predict(self):

        # STK routine
        directorio_script = getcwd()
        self.open_STK(self.STK_dir)
        self.open_files_STK(self.index_STK, directorio_script)
        chdir(directorio_script)

        # predict routine
        self.open_predict(directorio_script)
        self.open_files_predict()

        # Differences
        list_alt = []
        list_az = []

        time_intersected_predict = []
        time_intersected_predict = list(
            set(self.STK_simulation_time).intersection(
                self.predict_simulation_time))

        i = 0

        for i in range(len(time_intersected_predict)):
            difference_alt = \
                float(self.predict_alt_satellite[
                    self.predict_simulation_time.index(
                        time_intersected_predict[i])]) - \
                float(
                    self.STK_alt_satellite[
                        self.STK_simulation_time.index(
                            time_intersected_predict[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(self.predict_az_satellite[
                    self.predict_simulation_time.index(
                        time_intersected_predict[i])]) - \
                float(
                    self.STK_az_satellite[
                        self.STK_simulation_time.index(
                            time_intersected_predict[i])])

            list_az.append(difference_az)

            i = i + 1

        # Force mean to zero
        m = 0

        alt = numpy.asarray(list_alt)
        az = numpy.asarray(list_az)

        # Standard deviation
        std_alt = numpy.sqrt(numpy.mean((alt - m) ** 2))
        std_az = numpy.sqrt(numpy.mean((az - m) ** 2))

        chdir(self.directorio_script)

        return std_alt, std_az

    def STK_vs_predict_comp(self):

        # STK routine

        directorio_script = getcwd()
        self.open_STK(self.STK_dir)
        self.open_files_STK(self.index_STK, directorio_script)
        chdir(directorio_script)

        # predict routine
        self.open_predict(directorio_script)
        self.open_files_predict()

        # Differences
        list_alt = []
        list_az = []

        time_intersected_predict = []
        time_intersected_predict = list(
            set(self.STK_simulation_time).intersection(
                self.predict_simulation_time))

        i = 0

        for i in range(len(time_intersected_predict)):
            difference_alt = \
                float(self.predict_alt_satellite[
                    self.predict_simulation_time.index(
                        time_intersected_predict[i])]) - \
                float(
                    self.STK_alt_satellite[
                        self.STK_simulation_time.index(
                            time_intersected_predict[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(self.predict_az_satellite[
                    self.predict_simulation_time.index(
                        time_intersected_predict[i])]) - \
                float(
                    self.STK_az_satellite[
                        self.STK_simulation_time.index(
                            time_intersected_predict[i])])

            list_az.append(difference_az)

            i = i + 1

        chdir(self.directorio_script)

        return time_intersected_predict, list_alt, list_az
