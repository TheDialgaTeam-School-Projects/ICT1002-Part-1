import Tkinter as tk
from Tkinter import *
import matplotlib
import BaseGUIEvent
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
import PBFunction
import numpy as np
import tkMessageBox
matplotlib.use('TkAgg')


class pageTendering2(tk.Frame, BaseGUIEvent.BaseGUIEvent):
    try:
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            BaseGUIEvent.BaseGUIEvent.__init__(self, controller)

            # Title label
            label = tk.Label(self, text="Tendering Details")
            label.pack(pady=10, padx=10)

            # Back Button
            button1 = tk.Button(self, text="Back",
                                command=lambda: controller.change_frame("Page2GUI"))
            button1.pack()

            # Drop down menu to select tendering amt ($)
            OPTIONS = ["View Tendering Amount"]
            variable = StringVar(self)
            variable.set(OPTIONS[0])  # default value

            # Drop down menu command
            def command(*args):
                controller.change_frame("TenderingGUI")
            w = OptionMenu(self, variable, *OPTIONS, command=command)
            w.pack()

        def load(self, *args, **kwargs):
            """
            Handle on load event for this GUI.

            :param args: List of args pass from the previous frame.
            :param kwargs: Dictionary of args pass from the previous frame.
            """

            # prevent UI from producing duplicates records on load
            if "someT2" in self.controller.globals:
                return
            self.controller.globals["someT2"] = True

            # Calling of global file path procurement.csv
            path2 = self.controller.globals["procurement_file_path"]

            # Fetch no. of tenders per year for NA tender status from PBFunction.py
            keys = PBFunction.numberT(path2)

            # Fetch no. of tenders per year for "awarded to suppliers" tender status from PBFunction.py
            keys2 = PBFunction.numberT2(path2)

            # sorted by key, return a list of tuples
            lists = sorted(keys.items())

            # unpack a list of pairs into two tuples
            x, y = zip(*lists)

            # sorted by key, return a list of tuples
            lists2 = sorted(keys2.items())

            # unpack a list of pairs into two tuples
            x2, y2 = zip(*lists2)

            f = Figure(figsize=(5, 5), dpi=100)
            ax = f.add_subplot(111)
            index = np.arange(3)
            bar_width = 0.35
            opacity = 0.4
            error_config = {'ecolor': '0.3'}

            # use fetched data and populate bars
            rects1 = ax.bar(index, y, bar_width,
                            alpha=opacity, color='b', error_kw=error_config,
                            label='Awarded')

            rects2 = ax.bar(index + bar_width, y2, bar_width,
                            alpha=opacity, color='r', error_kw=error_config,
                            label='Not Awarded')

            # Set graphs label and title header
            ax.set_xlabel('Years')
            ax.set_ylabel('No. of Tenders')
            ax.set_title('No. of Tenders awarded')
            ax.set_xticks(index + bar_width / 2)
            ax.set_xticklabels(('2015', '2016', '2017'))
            ax.legend()


            # Attach a text label above each bar displaying its height
            def autolabel(rects):

                for rect in rects:
                    height = rect.get_height()
                    ax.text(rect.get_x() + rect.get_width() / 2., 0.5 * height,
                            '%d' % int(height),
                            ha='center', va='bottom')

            autolabel(rects1)
            autolabel(rects2)

            # plotting of graph into canvas
            canvas = FigureCanvasTkAgg(f, self)
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            canvas.draw()

    # catch exception error
    except Exception as e:
        print e.__doc__
        print e.message
        tkMessageBox.showerror("Error", e.message)

