import Tkinter as Tk
import csv
import tkFileDialog
import tkMessageBox
import ttk

import BaseGUIEvent


class Function1GUI(ttk.Frame):

    def __init__(self, parent):
        """
        Display Function 1 GUI.

        :param ttk.Frame parent: Parent frame.
        :rtype: Function1GUI
        :return: Function 1 GUI.
        """
        ttk.Frame.__init__(self, parent)

        self.style = ttk.Style()
        self.style.configure('procurement_entry_button.TButton', width=20, font='Arial 14')
        self.style.configure('contractors_entry_button.TButton', width=20, font='Arial 14')
        self.style.configure('proceed_button.TButton', width=50, font='Calibri 20')

        self.procurement_analyzer_label = ttk.Label(self, anchor=Tk.CENTER, font=("Courier", 30, 'bold'),
                                                    text="Procurement Analyzer")
        self.procurement_analyzer_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=Tk.NSEW)

        self.procurement_label = ttk.Label(self, anchor=Tk.NW, text="Government Procurement File:",
                                           font=('Arial', 10, 'italic'))
        self.procurement_label.grid(row=1, column=0, columnspan=2, pady=(50, 4), sticky=Tk.NSEW)

        self.procurement_entry = ttk.Entry(self, state=Tk.DISABLED, exportselection=0)
        self.procurement_entry.grid(row=2, column=0, padx=2, sticky=Tk.NSEW)

        self.procurement_entry_button = ttk.Button(self, text="Select", style='procurement_entry_button.TButton')
        self.procurement_entry_button.grid(row=2, column=1, padx=2, sticky=Tk.NSEW)

        self.contractors_label = ttk.Label(self, anchor=Tk.NW, text="Registered Contractors File:",
                                           font=('Arial', 10, 'italic'))
        self.contractors_label.grid(row=3, column=0, columnspan=2, pady=(80, 4), sticky=Tk.NSEW)

        self.contractors_entry = ttk.Entry(self, state=Tk.DISABLED, exportselection=0)
        self.contractors_entry.grid(row=4, column=0, padx=2, sticky=Tk.NSEW)

        self.contractors_entry_button = ttk.Button(self, text="Select", style='contractors_entry_button.TButton')
        self.contractors_entry_button.grid(row=4, column=1, padx=2, sticky=Tk.NSEW)

        self.proceed_button = ttk.Button(self, text="Proceed", style='proceed_button.TButton')
        self.proceed_button.grid(row=5, column=0, columnspan=2, padx=320, pady=200, sticky=Tk.NSEW)

        self.grid_columnconfigure(0, weight=1)


class Function1GUIEvent(Function1GUI, BaseGUIEvent.BaseGUIEvent):
    def __init__(self, parent, controller):
        """
        Handle events for Function 1 GUI.

        :param ttk.Frame parent: Parent frame.
        :param MainGUI.MainGUI controller: Main controller.
        :rtype: Function1GUIEvent
        :return: Function 1 GUI.
        """
        Function1GUI.__init__(self, parent)
        BaseGUIEvent.BaseGUIEvent.__init__(self, controller)

        self.procurement_entry_button.configure(command=self.procurement_entry_button_click)

        self.contractors_entry_button.configure(command=self.contractors_entry_button_click)

        self.proceed_button.configure(command=self.proceed_button_click)

    def load(self, *args, **kwargs):
        """
        Handle on load event for this GUI.

        :param args: List of args pass from the previous frame.
        :param kwargs: Dictionary of args pass from the previous frame.
        """
        # Clear all the global variable that may be used in other screen.
        self.controller.globals.clear()

    def procurement_entry_button_click(self):
        """
        Handle government procurement file entry button on click event.
        """
        dir_name = tkFileDialog.askopenfilename(title='Please select a file', initialdir='../Dataset',
                                                filetypes=[("CSV Files", ".csv")])

        if dir_name is "":
            tkMessageBox.showerror("Error", "Please select one dataset!")
            return

        with open(dir_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            # looping through all columns to check for valid file format
            for row in csv_reader:
                if 'tender_no.' in row and 'agency' in row and 'tender_description' in row and 'award_date' in row and 'tender_detail_status' in row and 'supplier_name' in row and 'awarded_amt' in row and len(
                        row) == 7:
                    self.procurement_entry.configure(state=Tk.ACTIVE)
                    self.procurement_entry.delete(0, Tk.END)
                    self.procurement_entry.insert(0, dir_name)
                    self.procurement_entry.configure(state=Tk.DISABLED)
                    break
                else:
                    tkMessageBox.showerror("Error", "Invalid File")
                    break

    def contractors_entry_button_click(self):
        """
        Handle registered contractors file entry button on click event.
        """
        dir_name = tkFileDialog.askopenfilename(title='Please select a file', initialdir='../Dataset',
                                                filetypes=[("CSV Files", ".csv")])

        if dir_name is "":
            tkMessageBox.showerror("Error", "Please select one dataset!")
            return

        with open(dir_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            # looping through all columns to check for valid file format
            for row in csv_reader:
                if 'company_name' in row and 'uen_no' in row and 'workhead' in row and 'grade' in row and 'additional_info' in row and 'expiry_date' in row and 'street_name' in row and 'unit_no' in row and 'building_name' in row and 'postal_code' in row and 'tel_no' in row and 'building_no' in row and len(
                        row) == 12:
                    self.contractors_entry.configure(state=Tk.ACTIVE)
                    self.contractors_entry.delete(0, Tk.END)
                    self.contractors_entry.insert(0, dir_name)
                    self.contractors_entry.configure(state=Tk.DISABLED)
                    break
                else:
                    tkMessageBox.showerror("Error", "Invalid File")
                    break

    def proceed_button_click(self):
        """
        Handle proceed button on click event.
        """
        procurement_file_path = self.procurement_entry.get()
        contractors_file_path = self.contractors_entry.get()

        self.controller.globals["procurement_file_path"] = procurement_file_path
        self.controller.globals["contractors_file_path"] = contractors_file_path

        if procurement_file_path is not '' and contractors_file_path is not '':
            self.controller.change_frame("Page2GUI")
        else:
            tkMessageBox.showerror("Error", "Please choose 2 datasets")
