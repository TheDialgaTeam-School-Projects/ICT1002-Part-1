import Queue
import Tkinter as Tk
import platform
import ttk
import pyautogui
import tkMessageBox
from cefpython3 import cefpython as cef
from geopy.geocoders import Nominatim

import BaseGUIEvent
import Task
import errno

# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")


class GoogleMapGUI(ttk.Frame):
    def __init__(self, parent):
        """
        Display Google Map GUI.

        :param ttk.Frame parent: Parent frame.
        :rtype: GoogleMapGUI
        :return: Google Map GUI.
        """
        ttk.Frame.__init__(self, parent)

        # Row 0
        self.top_frame = ttk.Frame(self)
        self.top_frame.grid(row=0, column=0, sticky=Tk.NSEW)
        self.top_frame.grid_columnconfigure(0, weight=1)

        self.company_label = ttk.Label(self.top_frame, anchor=Tk.NW, text="Unknown", style="company_name_label.TLabel")
        self.company_label.grid(row=0, column=0, padx=(2, 0), sticky=Tk.NSEW)

        self.img_button = ttk.Button(self.top_frame, text="Save")
        self.img_button.grid(row=0, column=1, padx=(2, 0), pady=(0, 4), sticky=Tk.NE)

        self.back_button = ttk.Button(self.top_frame, text="Back")
        self.back_button.grid(row=0, column=2, padx=(2, 0), pady=(0, 4), sticky=Tk.NE)

        # Row 1
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.grid(row=1, column=0, sticky=Tk.NSEW)
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1)

        self.browser_frame = BrowserFrame(self.bottom_frame)
        self.browser_frame.grid(row=0, column=0, sticky=Tk.NSEW)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)


class GoogleMapGUIEvent(GoogleMapGUI, BaseGUIEvent.BaseGUIEvent):
    def __init__(self, parent, controller):
        """
        Handle events for Google Map GUI.

        :param ttk.Frame parent: Parent frame.
        :param MainGUI.MainGUI controller: Main controller.
        :rtype: GoogleMapGUIEvent
        :return: Contractor Information GUI.
        """
        GoogleMapGUI.__init__(self, parent)
        BaseGUIEvent.BaseGUIEvent.__init__(self, controller)

        # back_button
        self.back_button.configure(command=self.back_button_click)

        # screenshot_button
        self.img_button.configure(command=self.image_button_click)

        # This Frame Required
        self.back_button_frame = ""
        self.address_data = []
        self.postal_code = []
        self.company_name = ""

        self.location_data_queue = Queue.Queue()

    def back_button_click(self):
        """
        Handle back button on click event.
        """
        self.controller.change_frame(self.back_button_frame)

    def image_button_click(self):
        """
        Screenshot the map on click event and save it into a file.
        """
        # part of the screen
        im = pyautogui.screenshot(region=(self.winfo_rootx(), self.winfo_rooty(), self.winfo_width(), self.winfo_height()))

        # save to filepath
        try:
            im.save('ImageGmap/' + 'GMap.png')
            tkMessageBox.showinfo("Success", "Location image has been saved.")

        # error msg if filepath is invalid
        except IOError as e:
            if e.errno == errno.EACCES:
                tkMessageBox.showerror("Error", "file exists, but isn't readable")
            elif e.errno == errno.ENOENT:
                tkMessageBox.showerror("Error", "files isn't readable because it isn't there")

    def load(self, *args, **kwargs):
        """
        Handle on load event for this GUI.

        :param args: List of args pass from the previous frame.
        :param kwargs: Dictionary of args pass from the previous frame.
        """
        if "back_button_frame" in kwargs:
            self.back_button_frame = kwargs["back_button_frame"]

        if "address_data" in kwargs:
            self.address_data = kwargs["address_data"]

        if "postal_code" in kwargs:
            self.postal_code = kwargs["postal_code"]

        if "company_name" in kwargs:
            self.company_name = kwargs["company_name"]

        self.company_label.configure(text=self.company_name)

        self.browser_frame.browser.LoadUrl(
            cef.GetDataUrl("<html><body><p>Loading Google Map... Please wait!</p></body></html>"))

        Task.Task(self.load_location_task_run, self.location_data_queue).start()

        self.after(100, self.load_location_task_update)

    def load_location_task_run(self, output, *args, **kwargs):
        """
        Handle geo location in a task.

        :param Queue.Queue output: Output information.
        :param args: Array of args to pass from the callback function.
        :param kwargs: Dictionary of args to pass from the callback function.
        """

        #Get longitude and latitude
        geolocator = Nominatim(user_agent="GoogleMap.py")
        getLocation = geolocator.geocode("%s, SG" % str.join(" ", self.address_data[1:3]))
        print self.address_data[0:1]
        print getLocation
        print getLocation.latitude, getLocation.longitude

        output.put(getLocation)

    def load_location_task_update(self):
        """
        Handle geo location task update event.
        """
        try:
            #retrieving data from dataset and converting it to string
            getLocation = self.location_data_queue.get(False)
            getLocationPostal = str(self.postal_code)
            getLocationAddr = str(self.address_data[0:1])
            getLocationAddr = getLocationAddr.replace(" ", "+")
            #open the url in the tkinter gui
            if getLocation is not None:
                self.browser_frame.browser.StopLoad()
                self.browser_frame.browser.LoadUrl(cef.GetNavigateUrl("https://www.google.com/maps/search/?api=1&map_action=map&query="+getLocationAddr+"+"+getLocationPostal+"&zoom=18"))

                self.browser_frame.on_mainframe_configure(self.winfo_width(), self.winfo_height())

            #error msg if google map didnt read
            else:
                self.browser_frame.browser.LoadUrl(
                    cef.GetDataUrl(
                        "<html><body><p>Unable to locate from the google map. Please try again later.</p></body></html>"))

        except Queue.Empty:
            self.after(100, self.load_location_task_update)


class BrowserFrame(Tk.Frame):
    # This code is from the library itself. However import aren't available for this hence the code is copied here.

    def __init__(self, master):
        Tk.Frame.__init__(self, master)

        self.closing = False
        self.browser = None

        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Configure>", self.on_configure)
        self.focus_set()

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info,
                                             url=cef.GetDataUrl(
                                                 "<html><body><p>Loading Google Map... Please wait!</p></body></html>"))
        assert self.browser
        self.message_loop_work()

    def get_window_handle(self):
        if self.winfo_id() > 0:
            return self.winfo_id()
        elif MAC:
            # On Mac window id is an invalid negative value (Issue #308).
            # This is kind of a dirty hack to get window handle using
            # PyObjC package. If you change structure of windows then you
            # need to do modifications here as well.
            # noinspection PyUnresolvedReferences
            from AppKit import NSApp
            # noinspection PyUnresolvedReferences
            import objc
            # Sometimes there is more than one window, when application
            # didn't close cleanly last time Python displays an NSAlert
            # window asking whether to Reopen that window.
            # noinspection PyUnresolvedReferences
            return objc.pyobjc_id(NSApp.windows()[-1].contentView())
        else:
            raise Exception("Couldn't obtain window handle")

    def message_loop_work(self):
        cef.MessageLoopWork()
        self.after(100, self.message_loop_work)

    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()

    def on_root_configure(self):
        # Root <Configure> event will be called when top window is moved
        if self.browser:
            self.browser.NotifyMoveOrResizeStarted()

    def on_mainframe_configure(self, width, height):
        if self.browser:
            if WINDOWS:
                WindowUtils.OnSize(self.get_window_handle(), 0, 0, 0)
            elif LINUX:
                self.browser.SetBounds(0, 0, width, height)
            self.browser.NotifyMoveOrResizeStarted()

    def on_focus_in(self, _):
        if self.browser:
            self.browser.SetFocus(True)

    def on_focus_out(self, _):
        if self.browser:
            self.browser.SetFocus(False)

    def on_root_close(self):
        if self.browser:
            self.browser.CloseBrowser(True)
            self.clear_browser_references()
        self.destroy()

    def clear_browser_references(self):
        # Clear browser references that you keep anywhere in your
        # code. All references must be cleared for CEF to shutdown cleanly.
        self.browser = None
