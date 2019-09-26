from matplotlib import pyplot as plt
from Tkinter import *
import BaseGUIEvent
import Tkinter as tk
import Function2
import MenuCommand
import pandas as pd


class Function2GUI(tk.Frame, BaseGUIEvent.BaseGUIEvent):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        BaseGUIEvent.BaseGUIEvent.__init__(self, controller)

        # back button
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.change_frame("Page2GUI"))
        button1.pack()


        # textbox
        T = Text(self, height=10, width=40)
        T.pack()
        T.insert(END, "Display a Line graph\nTo show Awarded Amt over the duration ofyears for agency selected\n")


        # button to display graph
        button = Button(self, text="Display Graph", command=self.ok)
        button.pack()

        # w = OptionMenu(self, variable, *self.companynames)
        self.w = OptionMenu(self, None, None, None)
        self.w.pack()
        self.variable = None

    def load(self, *args, **kwargs):
        """
        Handle on load event for this GUI.

        :param args: List of args pass from the previous frame.
        :param kwargs: Dictionary of args pass from the previous frame.
        """
        # prevent UI from producing duplicates records on load
        if "someROYS" in self.controller.globals:
            return
        self.controller.globals["someROYS"] = True

        # Calling of global file path procurement.csv
        path2 = self.controller.globals["procurement_file_path"]

        # drop down menu
        self.variable = StringVar(self)
        self.variable.set("Accounting And Corporate Regulatory Authority")  # default value
        self.w.configure(textvariable=self.variable)

        #calling of function to get agency name
        companyNames = Function2.fuction2Graph(path2)

        self.w["menu"].delete(0, tk.END)

        # populating widget with the data fetched from function file
        for name in companyNames:
            self.w["menu"].add_radiobutton(label=name, command=MenuCommand.MenuCommand(name, self.variable, None))


    # plotting of graph
    def ok(self):
        # para = str(variable.get())
        data = Function2.fuction2Data(self.controller.globals["procurement_file_path"])
        data = data.sort_values(by='award_date')
        name = data[data.agency == str(self.variable.get())]
        fig, ax = plt.subplots()
        name.award_date = pd.to_datetime(name.award_date).dt.strftime('%b-%y')
        ax.plot(name.award_date, name.awarded_amt)
        plt.legend({(self.variable.get())})
        fig.autofmt_xdate()
        plt.xlabel('month - year')
        plt.xticks(rotation=90)
        plt.ylabel('amount awarded')
        plt.show()
