import BaseGUIEvent
from Tkinter import *
import smtplib, tkMessageBox

class Email(Frame, BaseGUIEvent.BaseGUIEvent):
    try:
        def __init__(self, master, controller):

            self.data = ''
            self.filename = 'TotalProcurement.txt'

            Frame.__init__(self, master)
            BaseGUIEvent.BaseGUIEvent.__init__(self, controller)

            self.l1 = Label(self, text="Your Email:")
            self.l1.grid(row=0, column=1, columnspan=1)

            # Email entry for input

            self.e1 = Entry(self, bd=5)
            self.e1.grid(row=0, column=2, columnspan=1)

            # Password Label

            self.l2 = Label(self, text="Password:")
            self.l2.grid(row=1, column=1, columnspan=1)

            # Password Entry for input

            self.e2 = Entry(self, bd=5, show="*")
            self.e2.grid(row=1, column=2, columnspan=1)

            # continue button

            self.contBtn = Button(self, text='Login', command=self.getCredentials)
            self.contBtn.grid(row=2, column=1)

            self.back = Button(self, text="Back", command=lambda: controller.change_frame("Function3GUI"))
            self.back.grid(row=2, column=2)

        def getCredentials(self):

            f = open(self.filename, 'w')
            f.write(self.data)

            try:
                # check if email and password are correct. Email = E1.get(), password = E2.get()
                server = smtplib.SMTP()
                server.set_debuglevel(0)
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(self.e1.get(), self.e2.get())
                ret = True

            except:
                ret = False

            if ret is False:
                tkMessageBox.showerror('Error!', 'Please enter the correct username and password')

            else:
                self.controller.change_frame("Email2", email=self.e1.get(), password=self.e2.get(), filename=self.filename)

        def load(self, *args, **kwargs):
            if "data" in kwargs:
                self.data = kwargs["data"]

    except Exception as e:  # catch exception error
        print e.__doc__
        print e.message
        tkMessageBox.showerror("Error", e.message)
