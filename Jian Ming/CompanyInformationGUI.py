import Queue
import Tkinter as Tk
import tkMessageBox
import ttk

import BaseGUIEvent
import Function4Model
import Task


class CompanyInformationGUI(ttk.Frame):
    def __init__(self, parent):
        """
        Display Contractor Information GUI.

        :param ttk.Frame parent: Parent frame.
        :rtype: CompanyInformationGUI
        :return: Contractor Information GUI.
        """
        ttk.Frame.__init__(self, parent)

        # To get the class information.
        # print self.company_info_label.winfo_class()

        # To get the layout information
        # print self.style.layout("TLabel")

        # To get the specific layout information
        # print self.style.element_options("Label.label")

        # Referenced from: https://tkdocs.com/tutorial/styles.html (Quite informative on how to style ttk element)

        self.style = ttk.Style()
        self.style.configure("company_info_label.TLabel", foreground="orange", font=("Arial", 15, "bold"))
        self.style.configure("company_name_label.TLabel", foreground="yellow")
        self.style.configure("registered_contractors_label.TLabel", foreground="orange", font=("Arial", 10, "bold"))
        self.style.configure("registered_contractors_tree_view.Treeview", rowheight=30)

        # Row 0
        self.top_frame = ttk.Frame(self)
        self.top_frame.grid(row=0, column=0, sticky=Tk.NSEW)
        self.top_frame.grid_columnconfigure(0, weight=1)

        self.back_button = ttk.Button(self.top_frame, text="Back")
        self.back_button.grid(row=0, column=1, padx=(2, 0), sticky=Tk.NE)

        # Row 1
        self.company_info_frame = ttk.Frame(self)
        self.company_info_frame.grid(row=1, column=0, sticky=Tk.NSEW)
        self.company_info_frame.grid_columnconfigure(0, weight=1)

        self.company_info_label = ttk.Label(self.company_info_frame, anchor=Tk.NW, text="Company Information",
                                            style="company_info_label.TLabel")
        self.company_info_label.grid(row=0, column=0, sticky=Tk.NSEW)

        self.separator = ttk.Separator(self.company_info_frame)
        self.separator.grid(row=1, column=0, pady=(0, 4), sticky=Tk.NSEW)

        self.company_name_label = ttk.Label(self.company_info_frame, anchor=Tk.NW, text="Unknown Company",
                                            style="company_name_label.TLabel")
        self.company_name_label.grid(row=2, column=0, sticky=Tk.NSEW)

        self.company_uen_no_label = ttk.Label(self.company_info_frame, anchor=Tk.NW, text="UEN No: ")
        self.company_uen_no_label.grid(row=3, column=0, sticky=Tk.NSEW)

        self.company_address_label = ttk.Label(self.company_info_frame, anchor=Tk.NW, text="Address: ")
        self.company_address_label.grid(row=4, column=0, sticky=Tk.NSEW)

        self.company_tel_label = ttk.Label(self.company_info_frame, anchor=Tk.NW, text="Tel: ")
        self.company_tel_label.grid(row=5, column=0, sticky=Tk.NSEW)

        self.separator_2 = ttk.Separator(self.company_info_frame)
        self.separator_2.grid(row=6, column=0, pady=(4, 4), sticky=Tk.NSEW)

        # Row 2
        self.registered_contractors_frame = ttk.Frame(self)
        self.registered_contractors_frame.grid(row=2, column=0, sticky=Tk.NSEW)
        self.registered_contractors_frame.grid_rowconfigure(1, weight=1)
        self.registered_contractors_frame.grid_columnconfigure(0, weight=1)

        self.registered_contractors_label = ttk.Label(self.registered_contractors_frame, anchor=Tk.NW,
                                                      text="Registered Contractors:",
                                                      style="registered_contractors_label.TLabel")
        self.registered_contractors_label.grid(row=0, column=0, sticky=Tk.NSEW)

        self.registered_contractors_tree_view = ttk.Treeview(self.registered_contractors_frame, selectmode=Tk.BROWSE,
                                                             style="registered_contractors_tree_view.Treeview",
                                                             columns=(
                                                                 "Description", "Grade", "Tendering Limit", "Expiry"))
        self.registered_contractors_tree_view.heading("#0", text="Workhead", anchor=Tk.CENTER)
        self.registered_contractors_tree_view.heading("#1", text="Description", anchor=Tk.CENTER)
        self.registered_contractors_tree_view.heading("#2", text="Grade", anchor=Tk.CENTER)
        self.registered_contractors_tree_view.heading("#3", text="Tendering Limit (SGD million)", anchor=Tk.CENTER)
        self.registered_contractors_tree_view.heading("#4", text="Expiry (DD/MM/YYYY)", anchor=Tk.CENTER)
        self.registered_contractors_tree_view.column("#0", minwidth=100, width=100, stretch=Tk.NO, anchor=Tk.CENTER)
        self.registered_contractors_tree_view.column("#1", minwidth=100, width=200, stretch=Tk.YES)
        self.registered_contractors_tree_view.column("#2", minwidth=150, width=150, stretch=Tk.NO, anchor=Tk.CENTER)
        self.registered_contractors_tree_view.column("#3", minwidth=250, width=250, stretch=Tk.NO, anchor=Tk.CENTER)
        self.registered_contractors_tree_view.column("#4", minwidth=200, width=200, stretch=Tk.NO, anchor=Tk.CENTER)
        self.registered_contractors_tree_view.grid(row=1, column=0, sticky=Tk.NSEW)

        self.registered_contractors_tree_view_scrollbar_y = ttk.Scrollbar(self.registered_contractors_frame,
                                                                          command=self.registered_contractors_tree_view.yview)
        self.registered_contractors_tree_view_scrollbar_y.grid(row=1, column=1, sticky=Tk.NSEW)

        self.registered_contractors_tree_view_scrollbar_x = ttk.Scrollbar(self.registered_contractors_frame,
                                                                          orient=Tk.HORIZONTAL,
                                                                          command=self.registered_contractors_tree_view.xview)
        self.registered_contractors_tree_view_scrollbar_x.grid(row=2, column=0, columnspan=2, sticky=Tk.NSEW)

        self.registered_contractors_tree_view.configure(
            xscrollcommand=self.registered_contractors_tree_view_scrollbar_x.set,
            yscrollcommand=self.registered_contractors_tree_view_scrollbar_y.set)

        self.separator_3 = ttk.Separator(self.registered_contractors_frame)
        self.separator_3.grid(row=3, column=0, pady=(4, 4), sticky=Tk.NSEW)

        # Row 3
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.grid(row=3, column=0, sticky=Tk.NSEW)
        self.bottom_frame.grid_columnconfigure(0, weight=1)

        self.google_map_button = ttk.Button(self.bottom_frame, text="Google Map")
        self.google_map_button.grid(row=0, column=0, sticky=Tk.NSEW)

        self.grid_columnconfigure(0, weight=1)


class CompanyInformationGUIEvent(CompanyInformationGUI, BaseGUIEvent.BaseGUIEvent):
    def __init__(self, parent, controller):
        """
        Handle events for Contractor Information GUI.

        :param ttk.Frame parent: Parent frame.
        :param MainGUI.MainGUI controller: Main controller.
        :rtype: CompanyInformationGUIEvent
        :return: Contractor Information GUI.
        """
        CompanyInformationGUI.__init__(self, parent)
        BaseGUIEvent.BaseGUIEvent.__init__(self, controller)

        # back_button
        self.back_button.configure(command=self.back_button_click)

        # google_map_button
        self.google_map_button.configure(command=self.google_map_button_click)

        # Contractor information
        self.contractor_information_queue = Queue.Queue()

        # Frame Required
        self.search_by = ""
        self.search_data = ""
        self.back_button_frame = ""

        self.contractor_information_initialized = False
        self.address_data = []
        self.postal_code = []
        self.company_name = ""

    def load(self, *args, **kwargs):
        """
        Handle on load event for this GUI.

        :param args: List of args pass from the previous frame.
        :param kwargs: Dictionary of args pass from the previous frame.
        """
        if "search_by" in kwargs:
            self.search_by = kwargs["search_by"]

        if "search_data" in kwargs:
            self.search_data = kwargs["search_data"]

        if "back_button_frame" in kwargs:
            self.back_button_frame = kwargs["back_button_frame"]

        self.contractor_information_initialized = False

        # Get registered contractors information in a task.
        Task.Task(self.contractor_information_task_run, self.contractor_information_queue, search_by=self.search_by,
                  search_data=self.search_data).start()

        self.after(100, self.contractor_information_task_update)

    def back_button_click(self):
        """
        Handle back button on click event.
        """
        self.controller.change_frame(self.back_button_frame)

    def google_map_button_click(self):
        """
        Handle google map button on click event.
        """
        if self.contractor_information_initialized:
            self.controller.change_frame("GoogleMapGUI", back_button_frame="CompanyInformationGUI",
                                         address_data=self.address_data,
                                         postal_code=self.postal_code,
                                         company_name=self.company_name)

    def contractor_information_task_run(self, output, *args, **kwargs):
        """
        Handle contractor information in a task.

        :param Queue.Queue output: Output information.
        :param args: Array of args to pass from the callback function.
        :param kwargs: Dictionary of args to pass from the callback function.
        """
        data = Function4Model.get_contractors_information(self.controller.globals["contractors_file_path"],
                                                          kwargs["search_by"], kwargs["search_data"])

        output.put(data)

    def contractor_information_task_update(self):
        """
        Handle contractor information task update event.
        """
        try:
            data = self.contractor_information_queue.get(False)

            if len(data) == 0:
                tkMessageBox.showerror("Error", "Unable to get the contractor information.")
                return

            self.postal_code = []
            self.address_data = []
            self.company_name = data[0]["company_name"]

            if data[0]["company_name"] != "na":
                self.address_data.append(data[0]["company_name"])

            if data[0]["building_no"] != "na":
                self.address_data.append(data[0]["building_no"])

            if data[0]["street_name"] != "na":
                self.address_data.append(data[0]["street_name"])

            if data[0]["unit_no"] != "na":
                self.address_data.append(data[0]["unit_no"])

            if data[0]["building_name"] != "na":
                self.address_data.append(data[0]["building_name"])

            if data[0]["postal_code"] != "na":
                self.address_data.append(data[0]["postal_code"])
                self.postal_code.append(data[0]["postal_code"])

            self.company_name_label.configure(text=data[0]["company_name"])
            self.company_uen_no_label.configure(text="UEN No. : %s" % (data[0]["uen_no"]))
            self.company_address_label.configure(text="Address : %s" % (str.join(" ", self.address_data)))
            self.company_tel_label.configure(text="Tel: %s" % (data[0]["tel_no"]))

            self.registered_contractors_tree_view.delete(*self.registered_contractors_tree_view.get_children())

            for item in data:
                workhead_description = Function4Model.get_workhead_description(item["workhead"])
                tendering_limits = Function4Model.get_tendering_limits(item["workhead"], item["grade"])

                self.registered_contractors_tree_view.insert("", Tk.END, text=item["workhead"],
                                                             values=[workhead_description, item["grade"],
                                                                     tendering_limits, item["expiry_date"]])

            self.contractor_information_initialized = True
        except Queue.Empty:
            self.after(100, self.contractor_information_task_update)
