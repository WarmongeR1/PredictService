# -*- encoding: utf-8 -*-


class STKvsOrbitronComparator(object):
    pass

    def STK_vs_Orbitron(self):

        object_orbitron = Read_orbitron_data(
            self.index_orbitron,
            self.sat_selected,
            self.orbitron_dir)
        orbitron_time = object_orbitron.orbitron_time
        orbitron_time = [int(item) for item in orbitron_time]

        orbitron_alt = object_orbitron.orbitron_alt_satellite
        orbitron_alt = [float(item) for item in orbitron_alt]

        orbitron_az = object_orbitron.orbitron_az_satellite
        orbitron_az = [float(item) for item in orbitron_az]

        # Differences
        list_alt = []
        list_az = []

        time_intersected = []
        time_intersected = list(
            set(self.STK_simulation_time).intersection(orbitron_time))

        for i in range(len(time_intersected)):
            difference_alt = \
                float(orbitron_alt[orbitron_time.index(time_intersected[i])]) - \
                float(
                    self.STK_alt_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(orbitron_az[orbitron_time.index(time_intersected[i])]) - \
                float(
                    self.STK_az_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_az.append(difference_az)

        # Force mean to zero
        m = 0

        alt = numpy.asarray(list_alt)
        az = numpy.asarray(list_az)

        # Standard deviation
        std_alt = numpy.sqrt(numpy.mean((alt - m) ** 2))
        std_az = numpy.sqrt(numpy.mean((az - m) ** 2))

        return std_alt, std_az

    def STK_vs_Orbitron_comp(self):

        # STK routine
        directorio_script = getcwd()
        self.open_STK(self.STK_dir)
        self.open_files_STK(self.index_STK, directorio_script)
        chdir(directorio_script)

        chdir(self.directorio_script)

        object_orbitron = Read_orbitron_data(
            self.index_orbitron,
            self.sat_selected,
            self.orbitron_dir)
        orbitron_time = object_orbitron.orbitron_time
        orbitron_time = [int(item) for item in orbitron_time]

        orbitron_alt = object_orbitron.orbitron_alt_satellite
        orbitron_alt = [float(item) for item in orbitron_alt]

        orbitron_az = object_orbitron.orbitron_az_satellite
        orbitron_az = [float(item) for item in orbitron_az]

        # Differences
        list_alt = []
        list_az = []

        time_intersected = []
        time_intersected = list(
            set(self.STK_simulation_time).intersection(orbitron_time))

        for i in range(len(time_intersected)):
            difference_alt = \
                float(orbitron_alt[orbitron_time.index(time_intersected[i])]) - \
                float(
                    self.STK_alt_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_alt.append(difference_alt)

            difference_az = \
                float(orbitron_az[orbitron_time.index(time_intersected[i])]) - \
                float(
                    self.STK_az_satellite[
                        self.STK_simulation_time.index(
                            time_intersected[i])])

            list_az.append(difference_az)

        return time_intersected, list_alt, list_az
