# -*- encoding: utf-8 -*-

from os import listdir

import sys

if sys.version < '3':
    import tkinter as tk
    from tkinter import LabelFrame, Radiobutton, LabelFrame
else:
    import tkinter as tk
    from tkinter import LabelFrame, Radiobutton, LabelFrame

import scrolledlist


class Window(object):

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x400")
        self.root.resizable(0, 0)
        self.root.title("Configure simulations")

        self.site()
        self.time()
        self.families()

        self.root.mainloop()

    def site(self):
        site_frame = LabelFrame(
            self.root,
            height=100,
            width=150,
            text="Site settings")
        site_frame.grid(column=0, row=0, columnspan=1, rowspan=1)

        from scrolledlist import ScrolledList
        site = ScrolledList(site_frame, width=20, height=3)
        site.grid(column=0, row=0, columnspan=1, rowspan=1)

    def time(self):
        time_frame = LabelFrame(
            self.root,
            height=100,
            width=150,
            text="Time settings")
        time_frame.grid(column=1, row=0, columnspan=1, rowspan=1)

        time_now = Radiobutton(time_frame, text="Now", variable=time, value=1)
        time_now.grid(column=0, row=0, columnspan=1, rowspan=1)
        time_selection = Radiobutton(
            time_frame,
            text="Select",
            variable=time,
            value=2)
        time_selection.grid(column=0, row=1, columnspan=1, rowspan=1)

        # Actual time
        # Set time

    def families(self):
        families_frame = LabelFrame(
            self.root,
            height=100,
            width=150,
            text="Family selection")
        families_frame.grid(column=1, row=1, columnspan=1, rowspan=1)

        family = scrolledlist.ScrolledList(families_frame, width=20, height=4)

        families = listdir('/home/case/TLEs')

        for i in range(len(families)):
            family.append(families[i])

        family.grid(column=0, row=0, columnspan=1, rowspan=1)
