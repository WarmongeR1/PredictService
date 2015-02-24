# -*- encoding: utf-8 -*-


class Read_STK_data(object):

    def __init__(self, index_satellite, directorio_datos):

        index_satellite = index_satellite
        script_dir = getcwd()

        # STK routine
        self.open_STK(directorio_datos)
        self.open_files_STK(index_satellite, script_dir)

        chdir(script_dir)

    def open_STK(self, directorio_datos):

        chdir(directorio_datos)

        self.files_STK = listdir(getcwd())
        self.files_STK.sort()

    def open_files_STK(self, index_satellite, script_dir):

        open_file = open(script_dir + '/results/PyEphem/temp')
        copy_names = open_file.readlines()
        copy_names = [item.rstrip('\n\r') for item in copy_names]
        copy_names = [item.strip() for item in copy_names]

        satellite = copy_names[index_satellite].replace(" ", "_")

        i = 0

        for i in range(len(copy_names)):
            if satellite in self.files_STK[i]:
                name = self.files_STK[i]

            i = i + 1

        try:
            self.open_file_STK(name)

        except UnboundLocalError:
            self.STK_simulation_time = []
            self.STK_alt_satellite = []
            self.STK_az_satellite = []

    def open_file_STK(self, name):

        self.STK_simulation_time = []
        self.STK_alt_satellite = []
        self.STK_az_satellite = []

        with open(name, 'rb') as open_file:
            reader = csv.reader(open_file)
            for row in reader:
                # Tengo que comprobar si la linea esta vacia
                try:
                    valor = int((float(row[0]) - 2440587.5) * 86400)
                    self.STK_simulation_time.append(valor)
                    self.STK_az_satellite.append((row[1]))
                    self.STK_alt_satellite.append((row[2]))
                except:
                    pass



