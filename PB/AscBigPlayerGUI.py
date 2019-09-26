import uuid
import Tkinter as tk
import ttk
import BaseGUIEvent
import PBFunction
import tkMessageBox
import Task
from Tkinter import *


class AscBigPlayerGUI(tk.Frame, BaseGUIEvent.BaseGUIEvent):

    try:
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            BaseGUIEvent.BaseGUIEvent.__init__(self, controller)

            # Title label
            label = tk.Label(self, text="The Big Players")
            label.pack(pady=10, padx=10)

            # Back button
            button1 = tk.Button(self, text="Back",
                                command=lambda: controller.change_frame("Page2GUI"))
            button1.pack()

            # create the radio buttons Ascending and Descending
            self.var = IntVar()
            AscBtn = Radiobutton(self, text='Ascending', variable=self.var, value=1, command=self.sortList)
            AscBtn.pack(anchor=W)
            DesBtn = Radiobutton(self, text='Descending', variable=self.var, value=2, command=self.sortList)
            DesBtn.pack(anchor=W)
            # set default radio button value as 'Descending'
            self.var.set(1)

            # Setup the Tree
            self.tree = ttk.Treeview(self, columns=('Amount'), selectmode='browse')
            vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
            vsb.pack(side="right", fill="y")
            self.tree.configure(yscrollcommand=vsb.set)
            self.tree.column('Amount', width=500, anchor='center')
            self.tree.heading('Amount', text='No. of times awarded tender')
            self.tree.pack(fill=tk.BOTH, expand=1)
            self.tree.heading('#0', text='')
            self.tree.bind("<Double-1>", self.OnDoubleClick)

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
                    tree.insert(parent, 'end', uid, text=key, value=value)

        def load(self, *args, **kwargs):
            """
            Handle on load event for this GUI.

            :param args: List of args pass from the previous frame.
            :param kwargs: Dictionary of args pass from the previous frame.
            """

            # prevent UI from producing duplicates records on load
            if "someF2255" in self.controller.globals:
                return
            self.controller.globals["someF2255"] = True

            # Calling of global file path procurement.csv
            path2 = self.controller.globals["procurement_file_path"]

            # Fetch ascending order of big player data from PBFunction.py
            data = PBFunction.AscbigPlayerFunc(path2)

            # setting of tree on load
            self.j_tree(self.tree, '', data)

        # Handles Treeview Click Command
        def OnDoubleClick(self, event):
            # Get selection
            item = self.tree.selection()[0]

            # Store selection in global varaiable
            self.controller.globals["BigPlayerSelection"] = self.tree.item(item, "text")

            # Change frame
            self.controller.change_frame("BigPlayerDetailsGUI")

        # Radio button command
        def sortList(self):
            if self.var.get() == 1:
                self.controller.change_frame("AscBigPlayerGUI")

            else:
                self.controller.change_frame("BigPlayerGUI")

    # catch exception error
    except Exception as e:
        print e.__doc__
        print e.message
        tkMessageBox.showerror("Error", e.message)
