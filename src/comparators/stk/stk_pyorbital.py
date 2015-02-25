# -*- encoding: utf-8 -*-


class STKvsPyOrbitalComparator(object):

    def STK_vs_PyOrbital(self):

        chdir(self.directorio_script)

        object_pyorbital = Read_pyorbital_data(self.index_pyorbital)

        pyorbital_time = object_pyorbital.pyorbital_simulation_time
        pyorbital_time = [int(item) for item in pyorbital_time]

        pyorbital_alt = object_pyorbital.pyorbital_alt_satellite
        pyorbital_alt = [float(item) for item in pyorbital_alt]

        pyorbital_az = object_pyorbital.pyorbital_az_satellite
        pyorbital_az = [float(item) for item in pyorbital_az]

        # Differences
        list_alt = []
        list_az = []

        time_intersected = []
        time_intersected = list(
            set(self.STK_simulation_time).intersection(pyorbital_time))

        i = 0

        for i in range(len(time_intersected)):
            difference_alt = \
                float(
                    pyorbital_alt[pyorbital_time.index(time_intersected[i])]) - \
                float(
                    self.STK_alt_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(pyorbital_az[pyorbital_time.index(time_intersected[i])]) - \
                float(
                    self.STK_az_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

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

    def STK_vs_PyOrbital_comp(self):

        # STK routine
        directorio_script = getcwd()
        self.open_STK(self.STK_dir)
        self.open_files_STK(self.index_STK, directorio_script)
        chdir(directorio_script)

        chdir(self.directorio_script)

        object_pyorbital = Read_pyorbital_data(self.index_pyorbital)

        pyorbital_time = object_pyorbital.pyorbital_simulation_time
        pyorbital_time = [int(item) for item in pyorbital_time]

        pyorbital_alt = object_pyorbital.pyorbital_alt_satellite
        pyorbital_alt = [float(item) for item in pyorbital_alt]

        pyorbital_az = object_pyorbital.pyorbital_az_satellite
        pyorbital_az = [float(item) for item in pyorbital_az]

        # Differences
        list_alt = []
        list_az = []

        time_intersected = []
        time_intersected = list(
            set(self.STK_simulation_time).intersection(pyorbital_time))

        i = 0

        for i in range(len(time_intersected)):
            difference_alt = \
                float(
                    pyorbital_alt[pyorbital_time.index(time_intersected[i])]) - \
                float(
                    self.STK_alt_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(pyorbital_az[pyorbital_time.index(time_intersected[i])]) - \
                float(
                    self.STK_az_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_az.append(difference_az)

            i = i + 1

        chdir(self.directorio_script)

        return time_intersected, list_alt, list_az
