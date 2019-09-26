import Tkinter as tk
from Tkinter import *
import pandas as pd
import BaseGUIEvent
import Function3
import tkMessageBox


class Function3GUI(tk.Frame, BaseGUIEvent.BaseGUIEvent):

    try:
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            BaseGUIEvent.BaseGUIEvent.__init__(self, controller)

            # create the radio buttons Ascending and Descending
            self.var = IntVar()
            AscBtn = Radiobutton(self, text='Ascending', variable=self.var, value=1, command=self.sel)
            AscBtn.pack(anchor=W)
            DesBtn = Radiobutton(self, text='Descending', variable=self.var, value=2, command=self.sel)
            DesBtn.pack(anchor=W)
            self.var.set(1)       #set default radio button value as 1

            #Back button to page 2
            back = tk.Button(self, text="Back", command=lambda: controller.change_frame("Page2GUI"))
            back.place(relx=0.42, rely=0.05, anchor=CENTER)

            #Email Button
            buttonEmail = tk.Button(self, text="Email",
                                    command=lambda: controller.change_frame("Email", data=self.text.get('1.0', 'end')))
            buttonEmail.place(relx=0.5, rely=0.05, anchor=CENTER)

            #Scrollbar
            scrollbar = Scrollbar(self)
            scrollbar.pack(side=RIGHT, fill=Y)
            self.text = Text(self, yscrollcommand=scrollbar.set)
            self.text.pack(fill=BOTH, expand=1)
            scrollbar.config(command=self.text.yview)
            self.data = None

        # converts the dictionary into a dataframe using pandas and sorts the total amount of procurement for each agency
        def dictTodf(self, column):
            asc = ''
            des = ''
            # Set the max column width
            pd.set_option('display.max_colwidth', -1)

            # create the dataframe
            df = pd.DataFrame(column)
            # convert the values in 'awarded_amt' to float
            df['awarded_amt'] = df.awarded_amt.astype(float)

            # get the total amt in ascending and descending order and return them
            procurement = df.groupby('agency').sum()
            AscendingProcurement = procurement.sort_values(by=['awarded_amt'], ascending=True)
            DesscendingProcurement = procurement.sort_values(by=['awarded_amt'], ascending=False)

            # converts the dataframe into a string and returns the strings
            a = AscendingProcurement.to_string()
            AscProc = a.encode('ascii', 'ignore')
            for line in AscProc.splitlines():
                if not line.startswith('agency'):
                    asc += line + '\n'
            asc = asc.replace('awarded_amt', 'Total Procurement')

            d = DesscendingProcurement.to_string()
            DesProc = d.encode('ascii', 'ignore')
            for line in DesProc.splitlines():
                if not line.startswith('agency'):
                    des += line + '\n'
            des = des.replace('awarded_amt', 'Total Procurement')

            return asc, des

        # the select function for the ascending and descending radio buttons
        def sel(self):
            asc, des = self.dictTodf(self.data)

            if self.var.get() == 1:
                self.text.delete('1.0', END)
                self.text.insert(END, asc)

            else:
                self.text.delete('1.0', END)
                self.text.insert(END, des)

        def load(self, *args, **kwargs):
            """
            Handle on load event for this GUI.

            :param args: List of args pass from the previous frame.
            :param kwargs: Dictionary of args pass from the previous frame.
            """

            # Prevent UI from printing duplicate records on load
            if "someFARID" in self.controller.globals:
                return
            self.controller.globals["someFARID"] = True

            # storing global variable file path in variable
            path2 = self.controller.globals["procurement_file_path"]

            # calling function CSVTodict from Function3.py and store in variable
            self.data = Function3.csvTodict(path2)

            # calling function dictTodf from Function3.py and store in variable
            asc, des = self.dictTodf(self.data)
            self.text.insert(END, asc)

    except Exception as e:  # catch exception error
        print e.__doc__
        print e.message
        tkMessageBox.showerror("Error", e.message)
