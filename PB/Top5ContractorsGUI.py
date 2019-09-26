import uuid
import Tkinter as tk
import ttk
import matplotlib, numpy
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import PBFunction
import BaseGUIEvent
import Task
import tkMessageBox
import errno
import os

matplotlib.use('TkAgg')


class pageTop5Contractors(tk.Frame, BaseGUIEvent.BaseGUIEvent):
    try:
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            BaseGUIEvent.BaseGUIEvent.__init__(self, controller)

            # Title label
            label = tk.Label(self, text="Top 5 Contractors")
            label.pack(pady=10, padx=10)

            # Back Button
            button1 = tk.Button(self, text="Back",
                                command=lambda: controller.change_frame("Page2GUI"))
            button1.pack()

            # Convert PDF Button
            button2 = tk.Button(self, text="Convert to PDF",
                                command=self.convertPDF)
            button2.pack()

            # Setup the Tree
            self.tree = ttk.Treeview(self, columns=('Amount'), selectmode='browse')
            vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=vsb.set)
            self.tree.column('Amount', width=500, anchor='center')
            self.tree.heading('Amount', text='Procurement Amount ($)')
            self.tree.pack(fill=tk.BOTH, expand=1)
            self.tree.heading('#0', text='')

        # populate tree based on data fetched from PBFunction.py
        def j_tree(self, tree, parent, dic):
            for key in dic.keys():
                uid = uuid.uuid4()
                if isinstance(dic[key], dict):
                    tree.insert(parent, 'end', uid, text=key)
                    self.j_tree(tree, uid, dic[key])
                elif isinstance(dic[key], tuple):
                    tree.insert(parent, 'end', uid, text=str(key) + '()')
                    self.j_tree(tree, uid, dict([(i2, x) for i2, x in enumerate(dic[key])]))
                elif isinstance(dic[key], list):
                    tree.insert(parent, 'end', uid, text=str(key) + '[]')
                    self.j_tree(tree, uid, dict([(i2, x) for i2, x in enumerate(dic[key])]))
                else:
                    value = dic[key]
                    if isinstance(value, str):
                        value = value.replace(' ', '_')
                    tree.insert(parent, 'end', uid, text=key, value='%.2f' % value)

        def load(self, *args, **kwargs):
            """
            Handle on load event for this GUI.

            :param args: List of args pass from the previous frame.
            :param kwargs: Dictionary of args pass from the previous frame.
            """

            # prevent UI from producing duplicates records on load
            if "some" in self.controller.globals:
                return
            self.controller.globals["some"] = True

            # Calling of global file path procurement.csv
            path2 = self.controller.globals["procurement_file_path"]

            # Fetch top 5 contractors list data from PBFunction.py
            data = PBFunction.top5List(path2)

            # Fetch top 5 contractors graph data from PBFunction.py
            keys = PBFunction.top5(path2)

            # Generate bar graphs using data fetched from PBFunction.py
            self.f = Figure(figsize=(5, 4), dpi=100)
            self.ax = self.f.add_subplot(111)
            for key, value in keys.iteritems():
                self.ax.bar(key, value)

            #Graph
            ind = numpy.arange(5)  # the x locations for the groups
            width = .5
            plt.setp(self.ax.get_xticklabels(), rotation=30, horizontalalignment='right')
            self.ax.set_yticklabels([])
            self.ax.set_ylabel('')
            self.ax.set_title("Overall Trend of Top 5 Contractors' Procurement")

            #Draw Graph Canvas
            canvas = FigureCanvasTkAgg(self.f, self)
            self.f.tight_layout()
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            canvas.draw()

            #tree
            self.j_tree(self.tree, '', data)

        def convertPDF(self):

            # store global variable file path of reg contractors csv
            path = self.controller.globals["contractors_file_path"]

            # store global variable file path of procurement csv
            path2 = self.controller.globals["procurement_file_path"]

            try:
                # make the pdf conversion run in background
                Task.Task(lambda: PBFunction.pdfTop5(self.controller.globals["procurement_file_path"])).start()

                # get current file directory
                current_directory = os.getcwd()
                final_directory = os.path.join(current_directory, r'Top5Contractors.pdf')

                # show dialog box
                tkMessageBox.showinfo("Info",
                                      "File is stored at: " + final_directory)

            # error catching of invalid file
            except IOError as e:

                if e.errno == errno.EACCES:
                    tkMessageBox.showerror("Error", "file exists, but isn't readable")

                elif e.errno == errno.ENOENT:
                    tkMessageBox.showerror("Error", "files isn't readable because it isn't there")

    # catch exception error
    except Exception as e:
        print e.__doc__
        print e.message
        tkMessageBox.showerror("Error", e.message)