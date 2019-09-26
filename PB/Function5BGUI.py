import uuid
import Tkinter as tk
import ttk
import BaseGUIEvent
import PBFunction
import tkMessageBox

class PageUnregisteredC(tk.Frame, BaseGUIEvent.BaseGUIEvent):
    try:
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            BaseGUIEvent.BaseGUIEvent.__init__(self, controller)

            # Title label
            label = tk.Label(self, text="Procurement Awarded to Unregistered Contractors")
            label.pack(pady=10, padx=10)

            # Back button
            button1 = tk.Button(self, text="Back",
                                command=lambda: controller.change_frame("Page2GUI"))
            button1.pack()


            # Setup the Tree
            self.tree = ttk.Treeview(self, columns=('Amount'), selectmode='browse')
            vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
            vsb.pack(side="right", fill="y")
            self.tree.configure(yscrollcommand=vsb.set)
            self.tree.column('Amount', width=500, anchor='center')
            self.tree.heading('Amount', text='Amount ($)')
            self.tree.pack(fill=tk.BOTH, expand=1)
            self.tree.heading('#0', text='')

        # populate tree based on data fetched from PBFunction.py
        def j_tree(self, tree, parent, dic):
            for key in sorted(dic.keys()):
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
            if "some5B" in self.controller.globals:
                return
            self.controller.globals["some5B"] = True

            # Calling of global file path contractors.csv
            path = self.controller.globals["contractors_file_path"]

            # Calling of global file path procurement.csv
            path2 = self.controller.globals["procurement_file_path"]

            # Fetch reg contractor data from PBFunction.py
            data = PBFunction.UnregisteredContractors(path, path2)

            # setting of tree on load
            self.j_tree(self.tree, '', data)

    # catch exception error
    except Exception as e:
        print e.__doc__
        print e.message
        tkMessageBox.showerror("Error", e.message)
