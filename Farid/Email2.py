import smtplib
import socket
import tkMessageBox
from Tkinter import *
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import dns.resolver
import BaseGUIEvent

class Email2(Frame, BaseGUIEvent.BaseGUIEvent):
    try:
        def __init__(self, master, controller):

            self.email = ''
            self.password = ''
            self.filename = ''

            Frame.__init__(self, master)
            BaseGUIEvent.BaseGUIEvent.__init__(self, controller)

            self.l1 = Label(self, text="Recipient's Email:")
            self.l1.grid(row=0, column=1, columnspan=1)

            # Email entry for input

            self.e1 = Entry(self, bd=5)
            self.e1.grid(row=0, column=2, columnspan=1)

            self.contBtn = Button(self, text='Continue', command=self.checkEmail)
            self.contBtn.grid(row=1, column=1)

            self.back = Button(self, text="Back", command=lambda: controller.change_frame("Email"))
            self.back.grid(row=1, column=2)

        def load(self, *args, **kwargs):
            if "email" in kwargs:
                self.email = kwargs["email"]

            if "password" in kwargs:
                self.password = kwargs["password"]

            if "filename" in kwargs:
                self.filename = kwargs["filename"]

        def getEmail(self):
            return self.e1.get()

        def checkEmail(self):

            # Step 1: check email matches the regular expression
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.getEmail())

            if match == None:
                tkMessageBox.showerror('Error!', 'Email does not match!')
                return

            # Step 2: Getting MX record

            # Pull domain name from email address
            domainname = self.getEmail().split('@')[1]

            # get the MX records for the domain
            records = dns.resolver.query(domainname, 'MX')
            mxRecord = records[0].exchange
            mxRecord = str(mxRecord)
            host = socket.gethostname()

            # SMTP lib setup (use debug level for full output)
            server = smtplib.SMTP()
            server.set_debuglevel(0)

            # SMTP Conversation
            server.connect(mxRecord)
            server.helo(host)
            server.mail('me@domain.com')
            code, message = server.rcpt(str(self.getEmail()))
            server.quit()

            if code == 250:
                fromAddr = self.email
                toAddr = self.getEmail()
                # sending email to myself for testing, NEED TO CHANGE WHEN INTEGRATING

                msg = MIMEMultipart()
                msg['From'] = fromAddr
                msg['To'] = toAddr
                msg['Subject'] = "Test Python email"
                message = "Hi, there is a file attached"

                # attach file and add respective headers
                file = MIMEApplication(open(self.filename, 'rb').read())  # NEED TO CHANGE WHEN INTEGRATING
                file.add_header('Content-Disposition', 'attachment', filename=self.filename)  # NEED TO CHANGE WHEN INTEGRATING

                # sender email credentials
                login = self.email
                password = self.password

                msg.attach(MIMEText(message, 'plain'))
                msg.attach(file)
                text = msg.as_string()

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(login, password)

                server.sendmail(fromAddr, toAddr, text)
                server.quit()
                tkMessageBox.showinfo('Success', 'Email sent')
                self.controller.change_frame("Function3GUI")

            else:
                tkMessageBox.showerror('Error!', 'Email does not exist!')

    except Exception as e:  # catch exception error
        print e.__doc__
        print e.message
        tkMessageBox.showerror("Error", e.message)
