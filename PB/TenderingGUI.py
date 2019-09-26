import Tkinter as tk
from Tkinter import *
import matplotlib
import BaseGUIEvent
import tkMessageBox
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
import PBFunction

matplotlib.use('TkAgg')


class pageTendering(tk.Frame, BaseGUIEvent.BaseGUIEvent):
    try:
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            BaseGUIEvent.BaseGUIEvent.__init__(self, controller)

            # Title label
            label = tk.Label(self, text="Tendering Details")
            label.pack(pady=10, padx=10)

            # Back button
            button1 = tk.Button(self, text="Back",
                                command=lambda: controller.change_frame("Page2GUI"))
            button1.pack()

            # Drop down menu to select tendering number
            OPTIONS = ["View Tendering Number"]  # etc
            variable = StringVar(self)
            variable.set(OPTIONS[0])  # default value

            # Drop down menu command
            def command(*args):
                controller.change_frame("Tendering2GUI")
            w = OptionMenu(self, variable, *OPTIONS, command=command)
            w.pack()

        def load(self, *args, **kwargs):
            """
            Handle on load event for this GUI.

            :param args: List of args pass from the previous frame.
            :param kwargs: Dictionary of args pass from the previous frame.
            """

            # prevent UI from producing duplicates records on load
            if "someT" in self.controller.globals:
                return
            self.controller.globals["someT"] = True

            # Calling of global file path procurement.csv
            path2 = self.controller.globals["procurement_file_path"]

            # Fetch  $ amount of tender per year data from PBFunction.py
            keys2 = PBFunction.amtT(path2)

            # sorted by key, return a list of tuples
            lists2 = sorted(keys2.items())

            # unpack a list of pairs into two tuples
            x, y = zip(*lists2)

            # plotting of graphs
            f = Figure(figsize=(5, 5), dpi=100)
            ax = f.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel("Year")
            ax.set_ylabel("Amt (in ten billions.)")
            ax.set_title('Amt. of Tender for Each Year')

            # place plotted graph in canvas
            canvas = FigureCanvasTkAgg(f, self)
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            canvas.draw()

    except Exception as e:  # catch exception error
        print e.__doc__
        print e.message
        tkMessageBox.showerror("Error", e.message)

