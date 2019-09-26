
import Tkinter as tk
import matplotlib
import BaseGUIEvent
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
import PBFunction
import numpy as np
import tkMessageBox
matplotlib.use('TkAgg')


class BigPlayerDetailsGUI(tk.Frame, BaseGUIEvent.BaseGUIEvent):

    try:
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            BaseGUIEvent.BaseGUIEvent.__init__(self, controller)

            # Title label
            label = tk.Label(self, text="The Big Players")
            label.pack(pady=10, padx=10)

            # Back button
            button1 = tk.Button(self, text="Back",
                                command=lambda: controller.change_frame("BigPlayerGUI"))
            button1.pack()

            #Graph
            self.f = Figure(figsize=(5, 5), dpi=100)
            self.canvas = FigureCanvasTkAgg(self.f, self)
            self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        def load(self, *args, **kwargs):
            """
            Handle on load event for this GUI.

            :param args: List of args pass from the previous frame.
            :param kwargs: Dictionary of args pass from the previous frame.
            """
             # Calling of global selection from BigPlayerGUI.py table selection
            details = self.controller.globals["BigPlayerSelection"]

            # Calling of global file path procurement.csv
            path2 = self.controller.globals["procurement_file_path"]

            # Fetch no.of tender from PBFunction.py
            keys = PBFunction.bigPlayerDetails1(path2, details)

            # Fetch ($)amt.of tender from PBFunction.py
            keys2 = PBFunction.bigPlayerDetails2(path2, details)

            # sorted by key, return a list of tuples
            lists = sorted(keys2.items())

            # unpack a list of pairs into two tuples
            xYear, yAmt = zip(*lists)

            # sorted by key, return a list of tuples
            lists2 = sorted(keys.items())

            # unpack a list of pairs into two tuples
            x2Year, y2Num = zip(*lists2)

            self.f.clear()
            ax = self.f.add_subplot(111)
            index = np.arange(3)
            bar_width = 0.35
            opacity = 0.4
            error_config = {'ecolor': '0.3'}

            # use fetched data and populate bars
            rects2 = ax.bar(index, yAmt, bar_width,
                            alpha=opacity, color='r', error_kw=error_config,
                            label='Amount Awarded')

            rects1 = ax.bar(index + bar_width, y2Num, bar_width,
                            alpha=opacity, color='w', error_kw=error_config,
                            label='Number of Times Awarded')

            # Set graphs label and title header
            ax.set_xlabel('Years')
            ax.set_ylabel('Amt ($)')
            ax.set_title('No. of Tenders awarded')
            ax.set_xticks(index + bar_width / 2)
            ax.set_xticklabels(('2015', '2016', '2017'))
            ax.legend()

            # Attach a text label above each bar displaying its height (amt.$ awarded)
            def autolabel(rects):

                for rect in rects:
                    height = rect.get_height()
                    ax.text(rect.get_x() + rect.get_width() / 2.00, 0.5 * height,
                            '%0.2f' % float(height),
                            ha='center', va='bottom')

            # Attach a text label above each bar displaying its height (no. of times awarded)
            def autolabel2(rects):

                for rect in rects:
                    height = rect.get_height()
                    ax.text(rect.get_x() + rect.get_width() / 2.00, 0.5 * height,
                            '%d' % int(height),
                            ha='center', va='bottom')

            autolabel(rects2)
            autolabel2(rects1)

            # drawing of canvas
            self.canvas.draw()

    # catch exception error
    except Exception as e:
        print e.__doc__
        print e.message
        tkMessageBox.showerror("Error", e.message)
