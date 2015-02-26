# -*- encoding: utf-8 -*-
import os
import sys

from src.gui.maingui import MainGUI


if sys.version < '3':
    import tkinter as tk
else:
    import tkinter as tk


def main():
    from optparse import OptionParser

    parser = OptionParser(usage='%prog: -i tle_file -f folder [options]')
    parser.add_option('-v', '--verbose', action='store_true')
    parser.add_option(
        '-i', '--tle_file', default=None,
        help='Filepath to file with satellites TLE')
    parser.add_option(
        '-f', '--data_folder', default=None,
        help='Path to folder with data')

    (options, args) = parser.parse_args()

    if options.tle_file is None or options.data_folder is None:
        parser.print_help()
        sys.exit(1)

    root = tk.Tk()
    interfaz = MainGUI(root, os.path.abspath(options.tle_file),
                       os.path.abspath(options.data_folder),
                       'pyephem')
    root.title('Simulaciones')
    root.geometry('1010x620')
    root.resizable(0, 0)
    root.mainloop()


if __name__ == '__main__':
    main()
