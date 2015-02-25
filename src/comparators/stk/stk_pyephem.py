# -*- encoding: utf-8 -*-


class STKvsPyEphemComparator(object):

    def STK_vs_PyEphem(self):

        chdir(self.directorio_script)

        object_pyephem = Read_pyephem_data(self.index_pyephem)

        pyephem_time = object_pyephem.pyephem_simulation_time
        pyephem_time = [int(item) for item in pyephem_time]

        pyephem_alt = object_pyephem.pyephem_alt_satellite
        pyephem_alt = [float(item) for item in pyephem_alt]

        pyephem_az = object_pyephem.pyephem_az_satellite
        pyephem_az = [float(item) for item in pyephem_az]

        # Differences
        list_alt = []
        list_az = []

        time_intersected = []
        time_intersected = list(
            set(self.STK_simulation_time).intersection(pyephem_time))

        i = 0

        for i in range(len(time_intersected)):
            difference_alt = \
                float(pyephem_alt[pyephem_time.index(time_intersected[i])]) - \
                float(
                    self.STK_alt_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(pyephem_az[pyephem_time.index(time_intersected[i])]) - \
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

    def STK_vs_PyEphem_comp(self):

        # STK routine

        directorio_script = getcwd()
        self.open_STK(self.STK_dir)
        self.open_files_STK(self.index_STK, directorio_script)
        chdir(directorio_script)

        chdir(self.directorio_script)

        object_pyephem = Read_pyephem_data(self.index_pyephem)

        pyephem_time = object_pyephem.pyephem_simulation_time
        pyephem_time = [int(item) for item in pyephem_time]

        pyephem_alt = object_pyephem.pyephem_alt_satellite
        pyephem_alt = [float(item) for item in pyephem_alt]

        pyephem_az = object_pyephem.pyephem_az_satellite
        pyephem_az = [float(item) for item in pyephem_az]

        # Differences
        list_alt = []
        list_az = []

        time_intersected = []
        time_intersected = list(
            set(self.STK_simulation_time).intersection(pyephem_time))

        i = 0

        for i in range(len(time_intersected)):
            difference_alt = \
                float(pyephem_alt[pyephem_time.index(time_intersected[i])]) - \
                float(
                    self.STK_alt_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(pyephem_az[pyephem_time.index(time_intersected[i])]) - \
                float(
                    self.STK_az_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_az.append(difference_az)

            i = i + 1

        chdir(self.directorio_script)

        return time_intersected, list_alt, list_az
