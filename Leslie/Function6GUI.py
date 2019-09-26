import Tkinter as tk
import ttk
import matplotlib
import FileController
import BaseGUIEvent
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

'''default font for labels'''
LARGE_FONT= ("Verdana", 12)
NORMAL_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 12)

'''global var'''
'''For populating the Option Menu'''
ministryList = ['Show All']
ministryList.extend(FileController.getAllMinistryList())

class Function6GUI(ttk.Frame, BaseGUIEvent.BaseGUIEvent):

    def load(self, *args, **kwargs):
        """
        Run only when on load
        Getting data for the graph and drawing it into GUI
        """
        if "someF115" in self.controller.globals:
            return
        self.controller.globals["someF115"] = True
        location = self.controller.globals["procurement_file_path"]
        self.dateLimit="Show all year"
        self.ministry="Show All"

        dateList = ["Show all year"]
        dateList.extend(FileController.getUniqueDate(location))
        self.ddlDate['menu'].delete(0,'end')
        for date in dateList:
            self.ddlDate['menu'].add_command(label=date,command=tk._setit(self.tkDateVar,date,self.updateDate))
        self.f = Figure(figsize=(6, 10), dpi=100)
        self.a = self.f.add_subplot(111)
        for tick in self.a.get_yticklabels():
            tick.set_rotation(35)
            tick.set_fontsize(5)
        yList = FileController.getAmountForAllMinistry(location)
        self.a.barh(FileController.getAllMinistryList(), yList)

        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.draw()

    def __init__(self, parent,controller):
        '''
        GUI elements only
        '''
        ttk.Frame.__init__(self, parent)
        BaseGUIEvent.BaseGUIEvent.__init__(self, controller)
        self.label = ttk.Label(self, text="Function 6 Page", font=LARGE_FONT)
        self.label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Back Home", command=lambda: controller.change_frame("Page2GUI"))
        button1.pack(pady=10)

        btn2 = ttk.Button(self, text="Create/Edit groupings",
                         command=lambda: controller.change_frame("Function6ExtGUI"))
        btn2.pack(padx=50, pady=10)

        self.tkVar = tk.StringVar(self)
        self.tkVar.set("")
        self.ddlMinistry = ttk.OptionMenu(self, self.tkVar, ministryList[0], *ministryList, command=self.updateGraph)
        self.ddlMinistry.pack(padx=10, pady=10)


        self.tkDateVar = tk.StringVar()
        self.tkDateVar.set("")
        self.ddlDate = ttk.OptionMenu(self,self.tkDateVar,"Show All Year")
        self.ddlDate.pack(padx=10,pady=10)

    def updateGraph(self,selection):
        '''
        Updating the graph whenever the user changes the option in option menu
        :param selection:
        :return:
        '''
        self.ministry = selection
        Function6GUI.animate(self)

    def updateDate(self,selection):
        '''
        Updating the date limit to only select data after the year
        :param selection:
        :return:
        '''
        self.dateLimit = selection
        Function6GUI.animate(self)

    def animate(self):
        '''
        Getting value for graph from fileController
        :param userSelection:
        :return:
        '''
        location = self.controller.globals["procurement_file_path"]
        if (FileController.fileCheck()):
            if self.dateLimit == 'Show all year':
                if self.ministry == 'Show All':
                    yList = FileController.getAmountForAllMinistry(location)
                    self.a.clear()
                    self.a.barh(FileController.getAllMinistryList(), yList)
                    for tick in self.a.get_yticklabels():
                        tick.set_rotation(35)
                        tick.set_fontsize(5)
                    self.canvas.draw()
                else:
                    xList = FileController.getSelectedAgencyByMinistry(self.ministry)
                    yList = FileController.getAmountList(location, xList)
                    self.a.clear()
                    self.a.barh(xList,yList,color="Green")
                    for tick in self.a.get_yticklabels():
                        tick.set_rotation(35)
                        tick.set_fontsize(6)
                    self.canvas.draw()
            else:
                if self.ministry == 'Show All':
                    yList = FileController.getAmountForAllMinistry(location, self.dateLimit)
                    self.a.clear()
                    self.a.barh(FileController.getAllMinistryList(), yList, color="Yellow")
                    for tick in self.a.get_yticklabels():
                        tick.set_rotation(35)
                        tick.set_fontsize(5)
                    self.canvas.draw()
                else:
                    xList = FileController.getSelectedAgencyByMinistry(self.ministry)
                    yList = FileController.getAmountList(location, xList, self.dateLimit)
                    self.a.clear()
                    self.a.barh(xList,yList,color="Orange")
                    for tick in self.a.get_yticklabels():
                        tick.set_rotation(35)
                        tick.set_fontsize(6)
                    self.canvas.draw()