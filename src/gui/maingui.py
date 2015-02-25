# -*- encoding: utf-8 -*-

##########################################################################
# Copyright 2014 Samuel Gongora Garcia (s.gongoragarcia@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##########################################################################
# Author: s.gongoragarcia[at]gmail.com
##########################################################################
import sys

from src.gui import scrolledlist
from src.utils.common import get_cnt_satellites, get_name
from src.predict.datareader import DataReader as PredictReader
from src.pyephem.datareader import DataReader as PyEphemReader
from src.pyorbital.datareader import DataReader as PyOrbitalReader
from src.orbitron.datareader import DataReader as OrbitronReader
from src.stk.datareader import DataReader as STKReader
from src.predict.datachecker import DataChecker as PredictChecker
from src.pyephem.datachecker import DataChecker as PyEphemChecker
from src.pyorbital.datachecker import DataChecker as PyOrbitalChecker
from src.orbitron.datachecker import DataChecker as OrbitronChecker
from src.stk.datachecker import DataChecker as STKChecker
from src.comparators.comparator import compare

if sys.version < '3':
    from tkinter.filedialog import asksaveasfile
    import tkinter.messagebox
    import tkinter as tk
else:
    from tkinter.filedialog import asksaveasfile
    import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
    NavigationToolbar2TkAgg
from sys import argv


class MainGUI(object):

    def __init__(self):
        self.index = 0
        self.cur_sat = ''
        self.index_pyephem = 0
        self.index_predict = 0
        self.index_pyorbital = 0
        self.index_stk = 0
        self.index_orbitron = 0
        self.data_folder = ''

        self.progs = [
            {
                'name': 'PyEphem',
                'reader': PyEphemReader,
                'checker': PyEphemChecker,
                'index': self.index_pyephem,
                'plot_alt': None,
                'plot_az': None,
                'color': 'b',
                'std_alt_value': None,
                'std_az_value': None,
            },
            {
                'name': 'predict',
                'reader': PredictReader,
                'checker': PredictChecker,
                'index': self.index_predict,
                'color': 'r',
                'std_alt_value': None,
                'std_az_value': None,
            },
            {
                'name': 'orbitron',
                'reader': OrbitronReader,
                'checker': OrbitronChecker,
                'index': self.index_orbitron,
                'plot_alt': None,
                'plot_az': None,
                'color': 'y',
                'std_alt_value': None,
                'std_az_value': None,
            },
            {
                'name': 'pyorbital',
                'reader': PyOrbitalReader,
                'checker': PyOrbitalChecker,
                'index': self.index_pyorbital,
                'plot_alt': None,
                'plot_az': None,
                'color': 'm',
                'std_alt_value': None,
                'std_az_value': None,
            },
            {
                'name': 'STK',
                'reader': STKReader,
                'checker': STKChecker,
                'index': self.index_stk,
                'plot_alt': None,
                'plot_az': None,
                'color': 'g',
                'std_alt_value': None,
                'std_az_value': None,

            }
        ]

        self.length = get_cnt_satellites(self.data_folder) - 1

        # self.widgets()
        self._init_view()

    def _init_view(self):
        self._init_plot()
        self._init_data()
        self._init_legend()
        self._init_canvas()
        self._init_comparation_plot()
        self._init_labels()
        self._init_control_frame()

    def _init_plot(self):
        # Plot
        self.f = Figure(figsize=(6, 7), dpi=80)
        self.text = self.f.suptitle(self.cur_sat, fontsize=16)

        # Subplots altitude & azimuth
        self.plot_altitude = self.f.add_subplot(211)
        self.plot_azimuth = self.f.add_subplot(212)

    def _init_legend(self):
        self.plot_altitude.legend(loc=2, borderaxespad=0., prop={'size': 12})
        self.plot_altitude.set_ylabel('Degrees')
        # Grid is on
        self.plot_altitude.grid(True)

        self.plot_azimuth.legend(loc=2, borderaxespad=0., prop={'size': 12})
        self.plot_azimuth.set_ylabel('Degrees')

        # Grid is on
        self.plot_azimuth.grid(True)

    def _init_canvas(self):
        left_frame = tk.Frame(root, height=800, width=500, padx=5, pady=5)
        left_frame.grid(column=0, row=0, columnspan=1, rowspan=3)

        # Figure controls
        self.canvas = FigureCanvasTkAgg(self.f, master=left_frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)

        toolbar = NavigationToolbar2TkAgg(self.canvas, left_frame)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=0)

    def _init_data(self):

        for program in self.progs:
            if program.get('checker')(program.get('index'), self.cur_sat,
                                      self.data_folder) == 'yes':
                data = program.get('reader')(self.data_folder,
                                             program.get('index'))
                alt_plot, = self.plot_altitude.plot(
                    data.get_sim_time(), data.get_alts(), program.get('color'),
                    label=program.get('name'))

                az_plot, = self.plot_azimuth.plot(
                    data.get_sim_time(), data.get_azs(), program.get('color'),
                    label=program.get('name'))

                program['plot_alt'] = alt_plot
                program['plot_az'] = az_plot

    def _init_comparation_plot(self):

        # Plot g
        self.plot_comparation = Figure(figsize=(6, 4), dpi=80)
        self.plot_comparation.suptitle('Comparation', fontsize=16)

        # Subplot c
        self.c = self.plot_comparation.add_subplot(111)

        right_frame = tk.Frame(root, height=330, width=500, bd=0)
        right_frame.grid(
            column=1,
            row=0,
            columnspan=1,
            rowspan=1,
            padx=5,
            pady=5)
        right_frame.grid_propagate(0)

        self.canvas2 = FigureCanvasTkAgg(self.plot_comparation,
                                         master=right_frame)
        self.canvas2.show()
        self.canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)

    def _init_data_frame(self):
        self.data_frame = tk.LabelFrame(
            root,
            text='Data',
            height=215,
            width=500,
            padx=5,
            pady=5)
        self.data_frame.grid(column=1, row=1, columnspan=1, rowspan=1)
        self.data_frame.columnconfigure(0, minsize=110)
        self.data_frame.columnconfigure(1, minsize=65)
        self.data_frame.columnconfigure(2, minsize=110)
        self.data_frame.columnconfigure(3, minsize=110)
        self.data_frame.rowconfigure(0, minsize=25)
        self.data_frame.rowconfigure(1, minsize=25)
        self.data_frame.rowconfigure(2, minsize=20)
        self.data_frame.rowconfigure(3, minsize=20)
        self.data_frame.rowconfigure(4, minsize=20)
        self.data_frame.rowconfigure(5, minsize=20)
        self.data_frame.rowconfigure(6, minsize=20)
        self.data_frame.rowconfigure(7, minsize=20)

        self.data_frame.grid_propagate(0)

    def _init_labels(self):
        # Name
        label_name = tk.Label(self.data_frame, text='Name')
        label_name.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=tk.W)

        self.text_name = tk.StringVar()
        object_name = get_name(self.index, self.data_folder)
        self.text_name.set(object_name.name)

        name = tk.Label(self.data_frame, textvariable=self.text_name)
        name.grid(column=1, row=0, columnspan=1, rowspan=1, sticky=tk.E)

        # Inclination
        elements = get_elements.Get_elements(argv[1], self.index)
        label_incl = tk.Label(self.data_frame, text='Inclination')
        label_incl.grid(column=2, row=0, columnspan=1, rowspan=1, sticky=tk.W)

        self.text_incl = tk.DoubleVar()
        self.text_incl.set(elements.inclination)

        incl = tk.Label(self.data_frame, textvariable=self.text_incl)
        incl.grid(column=3, row=0, columnspan=1, rowspan=1, sticky=tk.E)

        # File
        file_name = tk.Label(self.data_frame, text='File')
        file_name.grid(column=0, row=1, columnspan=1, rowspan=1, sticky=tk.W)

        self.file_name = tk.StringVar()
        self.file_name.set(argv[1])

        file_ = tk.Label(self.data_frame, textvariable=self.file_name)
        file_.grid(column=1, row=1, columnspan=1, rowspan=1, sticky=tk.E)

        # Mean motion
        label_motion = tk.Label(self.data_frame, text='Mean motion')
        label_motion.grid(
            column=2,
            row=1,
            columnspan=1,
            rowspan=1,
            sticky=tk.W)

        self.text_motion = tk.DoubleVar()
        self.text_motion.set(elements.mean_motion)

        motion = tk.Label(self.data_frame, textvariable=self.text_motion)
        motion.grid(column=3, row=1, columnspan=1, rowspan=1, sticky=tk.E)

        label_sims = tk.Label(self.data_frame, text='Simulations availables')
        label_sims.grid(column=0, row=2, columnspan=2, rowspan=1, sticky=tk.W)

        # Generate data

        sims_availables = scrolledlist.ScrolledList(
            self.data_frame,
            width=16,
            height=3,
            callback=self.pick_simulation)
        sims_availables.grid(
            column=0,
            row=3,
            columnspan=1,
            rowspan=3,
            sticky=tk.W)

        # Generate list of simulations
        self.sims_availables(
            available_predict,
            available_pyephem,
            available_pyorbital,
            available_orbitron,
            available_STK)

        for i in range(len(self.list_of_simulations)):
            sims_availables.append(self.list_of_simulations[i])

        # STD
        label_std = tk.Label(self.data_frame, text='Standard desviation')
        label_std.grid(column=2, row=2, columnspan=1, rowspan=1, sticky=tk.W)

        std_button = tk.Button(
            self.data_frame,
            text='Get data',
            command=self.std_simulations)
        std_button.grid(column=3, row=2, columnspan=1, rowspan=1, sticky=tk.E)

        label_std_alt = tk.Label(self.data_frame, text='Altitude')
        label_std_alt.grid(
            column=2,
            row=3,
            columnspan=1,
            rowspan=1,
            sticky=tk.E)

        label_std_az = tk.Label(self.data_frame, text='Azimuth')
        label_std_az.grid(
            column=3,
            row=3,
            columnspan=1,
            rowspan=1,
            sticky=tk.E)

        row_cnt = 3
        for program in self.progs:
            row_cnt += 1

            text_std = tk.Label(self.data_frame, text=program.get('name'))
            text_std.grid(
                column=1,
                row=row_cnt,
                columnspan=1,
                rowspan=1,
                sticky=tk.E)

            program['std_alt_value'] = tk.DoubleVar()
            program['std_alt_value'].set('%s alt.' % program.get('name'))

            std_alt = tk.Label(
                self.data_frame,
                textvariable=program.get('std_alt_value'))
            std_alt.grid(
                column=2,
                row=row_cnt,
                columnspan=1,
                rowspan=1,
                sticky=tk.E)

            program['std_az_value'] = tk.DoubleVar()
            program['std_az_value'].set('%s az.' % program.get('name'))

            std_pyephem_az = tk.Label(
                self.data_frame,
                textvariable=program.get('std_az_value'))
            std_pyephem_az.grid(
                column=3,
                row=row_cnt,
                columnspan=1,
                rowspan=1,
                sticky=tk.E)

        # Boton para realizar de nuevo las simulaciones
        save = tk.Button(
            self.data_frame,
            text='Save sims',
            command=self.save_routine)
        save.grid(column=0, row=6, columnspan=1, rowspan=2, sticky=tk.W)

    def _init_control_frame(self):

        # Control frame
        control_frame = tk.LabelFrame(
            root,
            text='Controls',
            height=55,
            width=500,
            padx=5,
            pady=5)
        control_frame.grid(column=1, row=2, columnspan=1, rowspan=1)
        control_frame.grid_propagate(0)

        control_frame.columnconfigure(0, minsize=40)
        control_frame.columnconfigure(1, minsize=40)
        control_frame.columnconfigure(2, minsize=350)

        self.next = tk.Button(
            master=control_frame,
            text='Next',
            command=self.next)
        self.next.grid(column=0, row=0, columnspan=1, rowspan=1)

        self.forward = tk.Button(
            master=control_frame,
            text='Forward',
            command=self.forward)
        self.forward.grid(column=1, row=0, columnspan=1, rowspan=1)

        button = tk.Button(
            master=control_frame,
            text='Quit',
            command=self._quit)
        button.grid(column=2, row=0, columnspan=1, rowspan=1, sticky=tk.E)

        # Check buttons state
        if self.index == 0:
            self.forward.configure(state=tk.DISABLED)
            self.next.configure(state=tk.NORMAL)
        elif self.index == self.length:
            self.forward.configure(state=tk.NORMAL)
            self.next.configure(state=tk.DISABLED)
        else:
            self.forward.configure(state=tk.NORMAL)
            self.next.configure(state=tk.NORMAL)


    def _step_action(self):
        self.cur_sat = get_name(self.index, self.data_folder)
        for program in self.progs:
            if program.get('checker')(program.get('index'), self.cur_sat,
                                      self.data_folder) == 'yes':
                program['index'] = program.get('index') + 1

        self.cur_sat = get_name(self.index, self.data_folder)
        self.text.set_text(self.cur_sat)

        # Check if data is available and print it

        for program in self.progs:
            if program.get('checker')(program.get('index'), self.cur_sat,
                                      self.data_folder) == 'yes':
                data = program.get('reader')(program.get('index'), self.cur_sat,
                                             self.data_folder)

                program.get('plot_alt').set_xdata(data.get_sim_time())
                program.get('plot_alt').set_ydata(data.get_alts())

                program.get('plot_az').set_xdata(data.get_sim_time())
                program.get('plot_az').set_ydata(data.get_azs)
        self.f.canvas.draw()

        # Subplot c
        self.c.clear()

        # Check buttons state
        if self.index == 0:
            self.forward.configure(state=tk.DISABLED)
            self.next.configure(state=tk.NORMAL)
        elif self.index == self.length:
            self.forward.configure(state=tk.NORMAL)
            self.next.configure(state=tk.DISABLED)
        else:
            self.forward.configure(state=tk.NORMAL)
            self.next.configure(state=tk.NORMAL)

    def _redraw(self):
        self.f.canvas.draw()

        # Subplot c
        self.c.clear()

        # Check buttons state
        if self.index == 0:
            self.forward.configure(state=tk.DISABLED)
            self.next.configure(state=tk.NORMAL)
        elif self.index == self.length:
            self.forward.configure(state=tk.NORMAL)
            self.next.configure(state=tk.DISABLED)
        else:
            self.forward.configure(state=tk.NORMAL)
            self.next.configure(state=tk.NORMAL)

    def __next__(self):
        self.index += 1
        self._step_action()
        self._redraw()

    def forward(self):

        self.index -= 1
        self._step_action()
        self._redraw()

    def sims_availables(self, available_predict, available_pyephem,
                        available_pyorbital, available_orbitron, available_STK):

        list_of_simulations = []
        if available_STK == 'yes':
            if available_predict == 'yes':
                list_of_simulations.append('STK vs. predict Alt.')
                list_of_simulations.append('STK vs. predict Azi.')
            if available_pyephem == 'yes':
                list_of_simulations.append('STK vs. PyEphem Alt.')
                list_of_simulations.append('STK vs. PyEphem Azi.')
            if available_pyorbital == 'yes':
                list_of_simulations.append('STK vs. PyOrbital Alt.')
                list_of_simulations.append('STK vs. PyOrbital Azi.')
            if available_orbitron == 'yes':
                list_of_simulations.append('STK vs. Orbitron Alt.')
                list_of_simulations.append('STK vs. Orbitron Azi.')
        else:
            list_of_simulations.append('STK not available')

        self.list_of_simulations = list_of_simulations

    def pick_simulation(self, index):

        comparation = Read_data(self.pyephem, self.predict, self.pyorbital,
                                self.orbitron, self.object_name.name, self.STK, argv[3], argv[4])

        if self.list_of_simulations[index][8:12] == 'pred' and\
                self.list_of_simulations[index][16:19] == 'Alt':
            (time, list_alt, list_az) = comparation.STK_vs_predict_comp()

            self.c.clear()

            self.c.plot(time, list_alt, 'ys', label='Difference')
            self.c.legend(loc=2, borderaxespad=0., prop={'size': 12})
            self.c.set_ylabel('Altitude - Degrees')
            self.c.grid(True)

            self.plot_comparation.canvas.draw()

        elif self.list_of_simulations[index][8:12] == 'pred' and\
                self.list_of_simulations[index][16:19] == 'Azi':
            (time, list_alt, list_az) = comparation.STK_vs_predict_comp()

            self.c.clear()

            self.c.plot(time, list_az, 'ys', label='Difference')
            self.c.legend(loc=2, borderaxespad=0., prop={'size': 12})
            self.c.set_ylabel('Azimuth - Degrees')
            self.c.grid(True)

            self.plot_comparation.canvas.draw()

        elif self.list_of_simulations[index][8:12] == 'PyEp' and\
                self.list_of_simulations[index][16:19] == 'Alt':
            (time, list_alt, list_az) = comparation.STK_vs_PyEphem_comp()

            self.c.clear()

            self.c.plot(time, list_alt, 'rs', label='Difference')
            self.c.legend(loc=2, borderaxespad=0., prop={'size': 12})
            self.c.set_ylabel('Altitude - Degrees')
            self.c.grid(True)

            self.plot_comparation.canvas.draw()

        elif self.list_of_simulations[index][8:12] == 'PyEp' and\
                self.list_of_simulations[index][16:19] == 'Azi':
            (time, list_alt, list_az) = comparation.STK_vs_PyEphem_comp()

            self.c.clear()

            self.c.plot(time, list_az, 'rs', label='Difference')
            self.c.legend(loc=2, borderaxespad=0., prop={'size': 12})
            self.c.set_ylabel('Azimuth - Degrees')
            self.c.grid(True)

            self.plot_comparation.canvas.draw()

        elif self.list_of_simulations[index][8:12] == 'PyOr' and\
                self.list_of_simulations[index][18:21] == 'Alt':
            (time, list_alt, list_az) = comparation.STK_vs_PyOrbital_comp()

            self.c.clear()

            self.c.plot(time, list_az, 'bs', label='Difference')
            self.c.legend(loc=2, borderaxespad=0., prop={'size': 12})
            self.c.set_ylabel('Altitude - Degrees')
            self.c.grid(True)

            self.plot_comparation.canvas.draw()

        elif self.list_of_simulations[index][8:12] == 'PyOr' and\
                self.list_of_simulations[index][18:21] == 'Azi':
            (time, list_alt, list_az) = comparation.STK_vs_PyOrbital_comp()

            self.c.clear()

            self.c.plot(time, list_az, 'bs', label='Difference')
            self.c.legend(loc=2, borderaxespad=0., prop={'size': 12})
            self.c.set_ylabel('Azimuth - Degrees')
            self.c.grid(True)

            self.plot_comparation.canvas.draw()

        elif self.list_of_simulations[index][8:12] == 'Orbi' and\
                self.list_of_simulations[index][17:20] == 'Alt':
            (time, list_alt, list_az) = comparation.STK_vs_Orbitron_comp()

            self.c.clear()

            self.c.plot(time, list_alt, 'gs', label='Difference')
            self.c.legend(loc=2, borderaxespad=0., prop={'size': 12})
            self.c.set_ylabel('Altitude - Degrees')
            self.c.grid(True)

            self.plot_comparation.canvas.draw()

        elif self.list_of_simulations[index][8:12] == 'Orbi' and\
                self.list_of_simulations[index][17:20] == 'Azi':
            (time, list_alt, list_az) = comparation.STK_vs_Orbitron_comp()

            self.c.clear()

            self.c.plot(time, list_az, 'gs', label='Difference')
            self.c.legend(loc=2, borderaxespad=0., prop={'size': 12})
            self.c.set_ylabel('Azimuth - Degrees')
            self.c.grid(True)

            self.plot_comparation.canvas.draw()

    def save_routine(self):

        f = asksaveasfile(mode='w', defaultextension='.txt')
        # asksaveasfile return `None` if dialog closed with "cancel".
        if f is None:
            return

        text = self.save_data()

        f.writelines(('%s\n' % line for line in text))
        f.close()

    def save_data(self):

        tkinter.messagebox.showinfo(
            'Wait until simulations end.',
            'This could take a while.')

        index = 0
        i = 0

        text = []
        text.append('==================================')
        text.append(' Family %s' % (argv[1]))
        text.append('==================================')

        for i in range(self.length):

            object_name = get_name(i, self.data_folder)

            text.append(' Satellite: %s' % (object_name.name))

            actual_available = Check_data(
                index,
                object_name.name,
                argv[3],
                argv[4])
            available_STK = actual_available.STK

            if available_STK == 'yes':

                available_predict = actual_available.predict
                available_pyephem = actual_available.pyephem
                available_pyorbital = actual_available.pyorbital
                available_orbitron = actual_available.orbitron

                data = Read_data(index, index, index,
                                 index, self.object_name.name, index, argv[3], argv[4])

                if available_predict == 'yes':

                    (std_predict_alt, std_predict_az) = data.STK_vs_predict()

                    std_predict_alt = round(float(std_predict_alt), 7)
                    std_predict_az = round(float(std_predict_az), 7)

                    text.append(' predict data')
                    text.append(
                        ' Alt: %s Az: %s' %
                        (std_predict_alt, std_predict_az))

                if available_pyephem == 'yes':

                    (std_pyephem_alt, std_pyephem_az) = data.STK_vs_PyEphem()

                    std_pyephem_alt = round(float(std_pyephem_alt), 7)
                    std_pyephem_az = round(float(std_pyephem_az), 7)

                    text.append(' PyEphem data')
                    text.append(
                        ' Alt: %s Az: %s' %
                        (std_pyephem_alt, std_pyephem_az))

                if available_pyorbital == 'yes':

                    (std_pyorbital_alt,
                     std_pyorbital_az) = data.STK_vs_PyOrbital()

                    std_pyorbital_alt = round(float(std_pyorbital_alt), 7)
                    round(float(std_pyorbital_az), 7)

                    text.append(' PyOrbital data')
                    text.append(
                        ' Alt: %s Az: %s' %
                        (std_pyorbital_alt, std_pyorbital_az))

                if available_orbitron == 'yes':

                    (std_orbitron_alt,
                     std_orbitron_az) = data.STK_vs_Orbitron()

                    std_orbitron_alt = round(float(std_orbitron_alt), 7)
                    std_orbitron_az = round(float(std_orbitron_az), 7)

                    text.append(' Orbitron data')
                    text.append(
                        ' Alt: %s Az: %s' %
                        (std_orbitron_alt, std_orbitron_az))

            elif available_STK == 'no':

                print(("Data don't available %s" % (i)))

            else:

                pass
                # pass

            i = i + 1
            index = index + 1
            text.append('')

        return text

        # save in pdf file

    def std_simulations(self):
        for program in self.progs:
            if program.get('name') != 'STK':
                std_predict_alt, std_predict_az = compare(
                    program.get('name'), self.index_stk, program.get('index'),
                    self.data_folder
                )
                program.get('std_alt_value').set(
                    round(float(std_predict_alt), 7))
                program.get('std_az_value').set(
                    round(float(std_predict_alt), 7))

    def _quit(self):
        root.quit()     # stops mainloop


if __name__ == '__main__':
    root = tk.Tk()
    interfaz = MainGUI()
    root.title('Simulaciones')
    root.geometry('1010x620')
    root.resizable(0, 0)
    root.mainloop()
