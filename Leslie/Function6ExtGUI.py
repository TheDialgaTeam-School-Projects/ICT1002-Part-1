import Tkinter as tk
import ttk
import FileController
import BaseGUIEvent
import tkMessageBox

"Default Font standards"
LARGE_FONT= ("Verdana", 12)
NORMAL_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 12)
agengcyList= ["---- Select Agency ----"]

class Function6ExtGUI(ttk.Frame, BaseGUIEvent.BaseGUIEvent):
    def load(self, *args, **kwargs):
        '''
        Variables to run when loading, e.g. adding stuff to the option menu
        :param args:
        :param kwargs:
        :return:
        '''
        global location
        location = self.controller.globals["procurement_file_path"]
        agencyList = FileController.getAllAgency(location)
        self.fileAgency = agengcyList[0]
        self.fileMinistry= FileController.getAllMinistryList()[0]
        self.ddlAgency['menu'].delete(0,'end')
        for agency in agencyList:
            self.ddlAgency['menu'].add_command(label=agency,command=tk._setit(self.agencyVar,agency,self.updateFileAgency))

    def __init__(self, parent, controller):
        '''
        GUI elements
        :param parent:
        :param controller:
        '''
        ttk.Frame.__init__(self, parent)
        BaseGUIEvent.BaseGUIEvent.__init__(self, controller)
        label = ttk.Label(self, text="Editing", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back To Graph", command=lambda: self.controller.change_frame("Function6GUI"))
        button1.pack()

        lblAgency = ttk.Label(self, text="Select Agency")
        lblAgency.pack(pady=10)
        self.agencyVar = tk.StringVar(self)
        self.ddlAgency = ttk.OptionMenu(self, self.agencyVar,agengcyList[0],*agengcyList, command=self.updateFileAgency)
        self.ddlAgency.pack(pady=20)

        lblMinistry = ttk.Label(self, text = "Select Ministry")
        lblMinistry.pack(pady=10)
        ministryVar = tk.StringVar(self)
        allMinList = FileController.getAllMinistryList()
        ddlMinistry = ttk.OptionMenu(self,ministryVar,allMinList[0],*allMinList, command= self.updateFileMinstry)
        ddlMinistry.pack(pady=30)


        btnUpdate = ttk.Button(self, text= 'Update',command = self.popupconfirm)
        btnUpdate.pack()

    def popupconfirm(self):
        '''
        To show the user the 2 option select and let the user check
        :return:
        '''
        result = tkMessageBox.askyesno("Confirm?","Are you sure of the following: "+self.fileAgency+" in "+self.fileMinistry)
        if result:
            FileController.createdefaultFile(self.fileAgency, self.fileMinistry)

    def updateFileAgency(self,selection):
        '''
        Get selection when option menu is change
        :param selection:
        :return:
        '''
        self.fileAgency = selection

    def updateFileMinstry(self,selection):
        '''
        Get selection when Ministry option menu is change
        :param selection:
        :return:
        '''
        self.fileMinistry = selection