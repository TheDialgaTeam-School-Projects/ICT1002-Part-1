import Queue
import Tkinter as Tk
import tkMessageBox
import ttk

import BaseGUIEvent
import Function4Model
import MenuCommand
import Task

# Constant
OPTION_MENU_OPTION_1 = "List of all registered company"
OPTION_MENU_OPTION_2 = "List of registered company that is awarded at least a procurement"

CONTEXT_MENU_OPTION_1 = "Show company information"


class RegisteredContractorsGUI(ttk.Frame):
    def __init__(self, parent):
        """
        Display Registered Contractors GUI.

        :param ttk.Frame parent: Parent frame.
        :rtype: RegisteredContractorsGUI
        :return: Registered Contractors GUI.
        """
        ttk.Frame.__init__(self, parent)

        # Row 0
        self.top_frame = ttk.Frame(self)
        self.top_frame.grid(row=0, column=0, sticky=Tk.NSEW)
        self.top_frame.grid_columnconfigure(1, weight=1)

        self.search_label = ttk.Label(self.top_frame, anchor=Tk.NW, text="Search:")
        self.search_label.grid(row=0, column=0, pady=(2, 0), sticky=Tk.NSEW)

        self.search_combobox = ttk.Combobox(self.top_frame, exportselection=0)
        self.search_combobox.grid(row=0, column=1, padx=(0, 4), sticky=Tk.NSEW)

        self.option_menu = ttk.OptionMenu(self.top_frame, None)
        self.option_menu.grid(row=0, column=2, sticky=Tk.NE)

        self.back_button = ttk.Button(self.top_frame, text="Back")
        self.back_button.grid(row=0, column=3, padx=(2, 0), sticky=Tk.NE)

        # Row 1
        self.label = ttk.Label(self, anchor=Tk.NW, text="List of registered company:")
        self.label.grid(row=1, column=0, pady=(0, 4), sticky=Tk.NSEW)

        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.grid(row=2, column=0, columnspan=2, pady=(0, 2), sticky=Tk.NSEW)
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1)

        self.registered_contractors_listbox = Tk.Listbox(self.bottom_frame, selectmode=Tk.SINGLE)
        self.registered_contractors_listbox.grid(row=0, column=0, padx=2, sticky=Tk.NSEW)

        self.registered_contractors_listbox_scrollbar_y = ttk.Scrollbar(self.bottom_frame,
                                                                        command=self.registered_contractors_listbox.yview)
        self.registered_contractors_listbox_scrollbar_y.grid(row=0, column=1, sticky=Tk.NSEW)

        self.registered_contractors_listbox.configure(
            yscrollcommand=self.registered_contractors_listbox_scrollbar_y.set)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)


class RegisteredContractorsGUIEvent(RegisteredContractorsGUI, BaseGUIEvent.BaseGUIEvent):
    def __init__(self, parent, controller):
        """
        Handle events for Registered Contractors GUI.

        :param ttk.Frame parent: Parent frame.
        :param MainGUI.MainGUI controller: Main controller.
        :rtype: RegisteredContractorsGUIEvent
        :return: Registered Contractors GUI.
        """
        RegisteredContractorsGUI.__init__(self, parent)
        BaseGUIEvent.BaseGUIEvent.__init__(self, controller)

        # search_entry
        self.search_combobox.bind("<KeyRelease>", self.search_entry_key_up)
        self.search_combobox.bind("<Key-Return>", self.search_entry_key_return_down)

        # option_menu
        self.option_menu_selected_item = Tk.StringVar()
        self.option_menu.configure(textvariable=self.option_menu_selected_item)
        self.option_menu["menu"].add_radiobutton(label=OPTION_MENU_OPTION_1,
                                                 command=MenuCommand.MenuCommand(OPTION_MENU_OPTION_1,
                                                                                 self.option_menu_selected_item,
                                                                                 self.option_menu_clicked))
        self.option_menu["menu"].add_radiobutton(
            label=OPTION_MENU_OPTION_2,
            command=MenuCommand.MenuCommand(OPTION_MENU_OPTION_2, self.option_menu_selected_item,
                                            self.option_menu_clicked))

        # back_button
        self.back_button.configure(command=self.back_button_click)

        # registered_contractors_listbox
        self.registered_contractors_listbox.bind("<Button-3>",
                                                 self.registered_contractors_listbox_right_mouse_down)

        self.registered_contractors_listbox_menu_selected_item = Tk.StringVar()
        self.registered_contractors_listbox_menu = Tk.Menu(self.registered_contractors_listbox, tearoff=0)
        self.registered_contractors_listbox_menu.add_command(label=CONTEXT_MENU_OPTION_1,
                                                             command=MenuCommand.MenuCommand(
                                                                 CONTEXT_MENU_OPTION_1,
                                                                 self.registered_contractors_listbox_menu_selected_item,
                                                                 self.registered_contractors_listbox_menu_clicked))

        self.registered_contractors_listbox_initialized = False
        self.registered_contractors_queue = Queue.Queue()

    def load(self, *args, **kwargs):
        """
        Handle on load event for this GUI.

        :param args: List of args pass from the previous frame.
        :param kwargs: Dictionary of args pass from the previous frame.
        """
        self.option_menu_selected_item.set("List of all registered company")

        self.registered_contractors_listbox_initialized = False
        self.registered_contractors_listbox.delete(0, Tk.END)
        self.registered_contractors_listbox.insert(Tk.END, "Reading dataset from file. Please wait!")

        if "registered_contractors_list" in self.controller.globals:
            self.registered_contractors_queue.put(
                self.controller.globals["registered_contractors_list"])
        else:
            Task.Task(self.registered_contractors_list_task_run,
                      self.registered_contractors_queue).start()

        self.after(100, self.registered_contractors_list_task_update)

    def search_entry_key_up(self, event):
        """
        Handle search entry on key up event.

        :param event: Event information.
        """
        if not self.registered_contractors_listbox_initialized:
            return

        top_5_matched_entries = Function4Model.get_registered_contractors_search_suggestions(
            self.controller.globals["contractors_file_path"], self.search_combobox.get())

        self.search_combobox.configure(values=top_5_matched_entries)

    def search_entry_key_return_down(self, event):
        """
        Handle search entry on key return down.

        :param event: Event information.
        """
        search_data = self.search_combobox.get()

        search_result = Function4Model.get_contractors_information(self.controller.globals["contractors_file_path"],
                                                                   "uen_no", search_data)

        if len(search_result) > 0:
            search_data = search_result[0]["company_name"]

        for i in range(0, len(self.controller.globals["registered_contractors_list"])):
            if self.controller.globals["registered_contractors_list"][i] == search_data:
                self.registered_contractors_listbox.selection_clear(0, Tk.END)
                self.registered_contractors_listbox.selection_set(i)
                self.registered_contractors_listbox.see(i)
                break

    def option_menu_clicked(self, selected_item):
        """
        Handle option menu on click event.

        :param str selected_item: Selected item on the option menu.
        """
        if selected_item == "List of all registered company":
            return
        elif selected_item == "List of registered company that is awarded at least a procurement":
            self.controller.change_frame("Function4GUI")

    def back_button_click(self):
        """
        Handle back button on click event.
        """
        self.controller.change_frame("Page2GUI")

    def registered_contractors_listbox_right_mouse_down(self, event):
        """
        Handle registered contractors listbox right mouse down event.

        :param event: Event information.
        """
        if not self.registered_contractors_listbox_initialized:
            return

        # if nothing is selected, then do nothing.
        if len(self.registered_contractors_listbox.curselection()) == 0:
            return

        try:
            self.registered_contractors_listbox_menu.tk_popup(event.x_root, event.y_root)
        finally:
            # Have to remove the grab event in case of some Tk bug such as Tk 8.0a1 version.
            self.registered_contractors_listbox_menu.grab_release()

    def registered_contractors_listbox_menu_clicked(self, selected_item):
        """
        Handle registered contractors listbox menu clicked event.

        :param str selected_item: Selected item on the listbox menu.
        """
        self.controller.change_frame("CompanyInformationGUI", search_by="company_name",
                                     search_data=self.registered_contractors_listbox.get(
                                         self.registered_contractors_listbox.curselection()),
                                     back_button_frame="RegisteredContractorsGUI")

    def registered_contractors_list_task_run(self, output, *args, **kwargs):
        """
        Get registered contractors in a task.

        :param Queue.Queue output: Output information.
        :param args: Array of args to pass from the callback function.
        :param kwargs: Dictionary of args to pass from the callback function.
        """
        data = Function4Model.get_registered_contractors(self.controller.globals["contractors_file_path"])
        self.controller.globals["registered_contractors_list"] = data

        output.put(data)

    def registered_contractors_list_task_update(self):
        """
        Handle registered contractors awarded list task update event.
        """
        try:
            data = self.registered_contractors_queue.get(False)
            self.registered_contractors_listbox.delete(0, Tk.END)

            if len(data) == 0:
                tkMessageBox.showerror("Error", "Unable to read the dataset.")
                return

            for item in data:
                self.registered_contractors_listbox.insert(Tk.END, item)

            self.registered_contractors_listbox_initialized = True
        except Queue.Empty:
            self.after(100, self.registered_contractors_list_task_update)
