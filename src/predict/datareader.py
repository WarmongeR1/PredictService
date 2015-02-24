# -*- encoding: utf-8 -*-


class Read_predict_data:

    def __init__(self, index_satellite):

        import os

        index_satellite = index_satellite + 1
        directorio_script = os.getcwd()

        # predict routine
        self.open_predict(directorio_script)
        self.open_files_predict(index_satellite)

        os.chdir(directorio_script)

    def open_predict(self, directorio_script):

        import os

        os.chdir(directorio_script + '/results/predict')

        self.files_predict = os.listdir(os.getcwd())
        self.files_predict.remove('temp')
        self.files_predict.sort()

    def open_files_predict(self, index_satellite):

        for i in range(index_satellite):
            self.open_file_predict(self.files_predict[i])

    def open_file_predict(self, name):

        self.predict_simulation_time = []
        self.predict_alt_satellite = []
        self.predict_az_satellite = []

        import csv

        with open(name) as tsv:
            for line in csv.reader(tsv, delimiter="\t"):
                if float(line[1]) >= 0:
                    self.predict_simulation_time.append(line[0])
                    self.predict_alt_satellite.append(float(line[1]))
                    self.predict_az_satellite.append(float(line[2]))

