import os
import sys

"""
INSTALLATION CODE:
This is the last resort installation check. It is recommended to follow the instruction in ReadMe.md

If you have not done what I have specified in ReadMe.md, this installation code will install for you.
It is recommended to include all the folder into the python path environment variable or it may fail.
If you changed the folder names, this installation check will not work. Please include them yourself.
"""
module_path = os.path.dirname(os.path.abspath(__file__))

if os.path.abspath(module_path) not in sys.path:
    sys.path.insert(0, os.path.abspath(module_path))

if os.path.abspath(module_path + "/Jian Ming") not in sys.path:
    sys.path.insert(0, os.path.abspath(module_path + "/Jian Ming"))

if os.path.abspath(module_path + "/PB") not in sys.path:
    sys.path.insert(0, os.path.abspath(module_path + "/PB"))

if os.path.abspath(module_path + "/Farid") not in sys.path:
    sys.path.insert(0, os.path.abspath(module_path + "/Farid"))

if os.path.abspath(module_path + "/Leslie") not in sys.path:
    sys.path.insert(0, os.path.abspath(module_path + "/Leslie"))

if os.path.abspath(module_path + "/Weiye") not in sys.path:
    sys.path.insert(0, os.path.abspath(module_path + "/Weiye"))

if os.path.abspath(module_path + "/Roysten") not in sys.path:
    sys.path.insert(0, os.path.abspath(module_path + "/Roysten"))
"""
END OF INSTALLATION CODE
"""

import Tkinter as Tk
import ttk

from CompanyInformationGUI import CompanyInformationGUIEvent
from Function1GUI import Function1GUIEvent
from Function4GUI import Function4GUIEvent
from RegisteredContractorsGUI import RegisteredContractorsGUIEvent
from Function5BGUI import PageUnregisteredC
from Function5GUI import PageRegisteredC
from Page2GUI import buttonsPage
from Top5ContractorsGUI import pageTop5Contractors
from TenderingGUI import pageTendering
from Tendering2GUI import pageTendering2
from BigPlayerGUI import BigPlayerGUI
from AscBigPlayerGUI import AscBigPlayerGUI
from BigPlayerDetailsGUI import BigPlayerDetailsGUI
from Function3GUI import Function3GUI
from Function6GUI import Function6GUI
from Function6ExtGUI import Function6ExtGUI
from Email import Email
from Email2 import Email2
from Function2GUI import Function2GUI
from GoogleMapGUI import GoogleMapGUIEvent

from cefpython3 import cefpython as cef

class MainGUI(Tk.Tk):
    """
    Reference from:
    https://pythonprogramming.net/change-show-new-frame-tkinter/
    """

    # Definition of all the GUI available. This is a key value pair that points to the correct class when invoked.
    GUI = {
        "Function1GUI": Function1GUIEvent,
        "Function4GUI": Function4GUIEvent,
        "RegisteredContractorsGUI": RegisteredContractorsGUIEvent,
        "CompanyInformationGUI": CompanyInformationGUIEvent,
        "Page2GUI": buttonsPage,
        "Function5GUI": PageRegisteredC,
        "Function5BGUI": PageUnregisteredC,
        "Top5ContractorsGUI": pageTop5Contractors,
        "TenderingGUI": pageTendering,
        "Tendering2GUI": pageTendering2,
        "BigPlayerGUI": BigPlayerGUI,
        "AscBigPlayerGUI": AscBigPlayerGUI,
        "BigPlayerDetailsGUI": BigPlayerDetailsGUI,
        "Function6GUI": Function6GUI,
        "Function6ExtGUI": Function6ExtGUI,
        "Function3GUI": Function3GUI,
        "Email": Email,
        "Email2": Email2,
        "Function2GUI": Function2GUI,
        "GoogleMapGUI": GoogleMapGUIEvent,
    }

    def __init__(self):
        """
        Display Main GUI.

        :rtype: MainGUI
        :return: Main GUI.
        """
        # Initialize Tk
        Tk.Tk.__init__(self)

        # Set the window title:
        self.title("Procurement Analyzer")

        # Set the window size and position:
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width / 2) - (960 / 2)
        y = (screen_height / 2) - (720 / 2)

        self.geometry("960x720+%d+%d" % (x, y))

        # Set the minimum window size:
        self.minsize(960, 720)

        # Set the global background style:
        self.style = ttk.Style()
        self.style.configure('.', background="#4295f4")
        self.style.configure('TButton', relief='flat', background="#000", foreground='black')

        # Set the master frame:
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=Tk.BOTH, expand=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # This are the frames of windows that we want to show :)
        self.frames = {}

        """
        LIST OF GLOBALS USED IN THIS SOURCE CODE:
        Note: Refactor is not possible once used. Please do not repeat them :P
        
        Syntax:
        type variable: description
        
        Function 1 GUI:
        str procurement_file_path: Containing procurement file path.
        str contractors_file_path: Containing contractors file path.
        
        Registered Contractors GUI:
        list[str] registered_contractors_list: Contains all the registered contractors company names.
        
        Function 4 GUI:
        list[str] registered_contractors_awarded_list: Contains all the awarded registered contractors company names.
        """
        self.globals = {}

        # Preload all the available GUI. Data models will not be loaded here.
        for key, value in MainGUI.GUI.items():
            frame = value(self.frame, self)
            frame.grid(row=0, column=0, padx=4, pady=4, sticky=Tk.NSEW)

            self.frames[key] = frame

        # Start with the first frame :)
        self.change_frame("Function1GUI")

    def change_frame(self, name, *args, **kwargs):
        """
        Display a GUI by providing the name of the GUI.

        :param str name: The name of the GUI to display. Refer to MainGUI.GUI variable for the available GUI.
        :param args: Array of args to pass into the next frame.
        :param kwargs: Dictionary of args to pass into the next frame.
        """
        frame = self.frames[name]

        # Raise this frame in the stacking order.
        frame.tkraise()

        # Call the onload event for the GUI to load the data models.
        frame.load(*args, **kwargs)


# CEF ERROR HANDLER: It is better to handle the CEF error so that it won't be left running in the background eating your resources.
sys.excepthook = cef.ExceptHook

app = MainGUI()
cef.Initialize()
app.mainloop()
cef.Shutdown()
