import Tkinter as Tk
import BaseGUIEvent
import ttk
import Task
import Function2

class buttonsPage(ttk.Frame, BaseGUIEvent.BaseGUIEvent):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        BaseGUIEvent.BaseGUIEvent.__init__(self, controller)

        self.style = ttk.Style()
        self.style.configure('Page2GUI.TButton', font=("MS Serif", 10))

        # Row 0
        self.procurement_analyzer_label = ttk.Label(self, anchor=Tk.CENTER, font=("Courier", 30, 'bold'),
                                                    text="Procurement Analyzer")
        self.procurement_analyzer_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=Tk.NSEW)

        # Row 1 Left
        self.agency_label = ttk.Label(self, anchor=Tk.CENTER, font=("MS Sans Serif", 24), text="Agency")
        self.agency_label.grid(row=1, column=0, sticky=Tk.NSEW)

        self.buttonFarid = ttk.Button(self, text="View Agency Procurement", style="Page2GUI.TButton",
                                      command=lambda: controller.change_frame("Function3GUI"))
        self.buttonFarid.grid(row=2, column=0, padx=50, pady=25, sticky=Tk.NSEW)

        self.buttonRoys = ttk.Button(self, text="View Agency Procurement Graph", style="Page2GUI.TButton",
                                     command=lambda: controller.change_frame("Function2GUI"))
        self.buttonRoys.grid(row=3, column=0, padx=50, pady=25, sticky=Tk.NSEW)

        self.buttonLeslie = ttk.Button(self, text="View Ministries", style="Page2GUI.TButton",
                                       command=lambda: controller.change_frame("Function6GUI"))
        self.buttonLeslie.grid(row=4, column=0, padx=50, pady=25, sticky=Tk.NSEW)

        # Row 1 Right
        self.contractors_label = ttk.Label(self, anchor=Tk.CENTER, font=("MS Sans Serif", 24), text="Contractors")
        self.contractors_label.grid(row=1, column=1, sticky=Tk.NSEW)

        self.buttonJM = ttk.Button(self, text="View Awarded Vendors", style="Page2GUI.TButton",
                                   command=lambda: controller.change_frame("Function4GUI"))
        self.buttonJM.grid(row=2, column=1, padx=50, pady=25, sticky=Tk.NSEW)

        self.buttonRegCon = ttk.Button(self, text="View Registered Contractors' Procurement", style="Page2GUI.TButton",
                                       command=lambda: controller.change_frame("Function5GUI"))
        self.buttonRegCon.grid(row=3, column=1, padx=50, pady=25, sticky=Tk.NSEW)

        self.buttonUnRegCon = ttk.Button(self, text="View Unregistered Contractors' Procurement",
                                         style="Page2GUI.TButton",
                                         command=lambda: controller.change_frame("Function5BGUI"))
        self.buttonUnRegCon.grid(row=4, column=1, padx=50, pady=25, sticky=Tk.NSEW)

        self.buttonTop5Con = ttk.Button(self, text="View Top 5 Contractors", style="Page2GUI.TButton",
                                        command=lambda: controller.change_frame("Top5ContractorsGUI"))
        self.buttonTop5Con.grid(row=5, column=1, padx=50, pady=25, sticky=Tk.NSEW)

        self.buttonBigPlayer = ttk.Button(self, text="View The Big Players", style="Page2GUI.TButton",
                                          command=lambda: controller.change_frame("BigPlayerGUI"))
        self.buttonBigPlayer.grid(row=6, column=1, padx=50, pady=25, sticky=Tk.NSEW)

        # Row 5 Left
        self.tenderingDetails_label = ttk.Label(self, anchor=Tk.CENTER, font=("MS Sans Serif", 24),
                                                text="Tendering Details")
        self.tenderingDetails_label.grid(row=5, column=0, pady=25, sticky=Tk.NSEW)

        self.buttonTendering = ttk.Button(self, text="View Tendering Details", style="Page2GUI.TButton",
                                          command=lambda: controller.change_frame("TenderingGUI"))
        self.buttonTendering.grid(row=6, column=0, padx=50, pady=25, sticky=Tk.NSEW)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)

    def load(self, *args, **kwargs):
        Task.Task(lambda: Function2.function2BackEnd(self.controller.globals["procurement_file_path"])).start()
