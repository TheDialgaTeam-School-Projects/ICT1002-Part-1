import operator
import csv
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, \
    Table, TableStyle
from collections import OrderedDict
import os
import collections

try:
    def regContractor(path, path2):
        try:
            with open(path, "rb") as fp1:         #open csv file
                file2 = csv.reader(fp1)           #read csv file
                rContractors = []
                rValue = []
                for i in file2:                   #store contractor's name from csv into list
                    rContractors.append(i[0])

            with open(path2, 'rb') as f:          #open registered contractors csv file
                reader = csv.reader(f)            #read registered contractors csv file
                cList = {}

                index = 0
                for row in reader:                #loop through all coluumns and rows in csv file
                    if index == 0:                #ignoring csv header
                        header = row
                    else:
                        contractor = row[5]      #storing contractor's name
                        amt = row[6]             #storing contractor's procurement amount

                        if contractor in cList:               #check for duplicate contractor's name
                            cList[contractor] += float(amt)   #if duplicate, sum their amount up
                        else:
                            cList[contractor] = float(amt)    #if not duplicate, store their amount
                    index += 1

            cList = {i: j for i, j in cList.items() if i in rContractors}   #compare rContractors and cList for common values and store in list
            return cList

        except Exception as e:           #catch exception error
            """
                print error msg out
            """
            print e.__doc__
            print e.message


    def UnregisteredContractors(path1, path2):
        try:
            with open(path1, "rb") as fp1:          #open csv file
                file2 = csv.reader(fp1)             #read csv file
                rContractors = []
                for i in file2:
                    rContractors.append(i[0])       #store contractor's name from csv into list

            with open(path2, 'rb') as f:            #open registered contractors csv file
                reader = csv.reader(f)              #read registered contractors csv file
                cList = {}

                index = 0
                for row in reader:                  #loop through all coluumns and rows in csv file
                    if index == 0:                  #ignoring csv header
                        header = row
                    else:
                        contractor = row[5]         #storing contractor's name
                        amt = row[6]                #storing contractor's procurement amount

                        if contractor == "na":       #Prevent storing contractor's name "NA'
                            index = index
                        else:
                            if contractor in cList:                           #check for duplicate contractor's name
                                cList[contractor] += float(amt)               #if duplicate, sum their amount up
                            else:
                                cList[contractor] = float(amt)               #if not duplicate, store their amount
                    index += 1

            cList = {i: j for i, j in cList.items() if i not in rContractors}   #compare rContractors and cList for not common values and store in list
            #print cList
            return cList
        except Exception as e:         #catch exception error
            """
              print error msg out
            """
            print e.__doc__
            print e.message


    def numberT(path1):                            #this function return no. of tenders per year for NA tender status
        try:
            with open(path1, 'rb') as f:          #open govt procuremenr csv file
                reader = csv.reader(f)            #read csv file
                cList = {}
                index = 0
                for row in reader:                #loop through all coluumns and rows in csv file
                    if index == 0:                #ignoring csv header
                        header = row
                    else:
                        award_Year = row[3]             #storing contractor's award date
                        tender_status = row[4]          #storing contractor's tender status

                        if tender_status == "Awarded to No Suppliers":       #Prevent storing tender status
                            index = index
                        else:
                            if award_Year[:4] in cList:                  #check for duplicate awarded year
                                cList[award_Year[:4]] += 1               #if duplicate, sum their amount up
                            else:
                                cList[award_Year[:4]] = 1                #if not duplicate, store their amount
                    index += 1

                return cList
        except Exception as e:    #catch exception error
            print e.__doc__
            print e.message


    def numberT2(path1):                        #this function return no. of tenders per year for "awarded to suppliers" tender status
        try:
            with open(path1, 'rb') as f:        #open govt procuremenr csv file
                reader = csv.reader(f)          #read csv file
                cList = {}
                index = 0
                for row in reader:              #loop through all coluumns and rows in csv file
                    if index == 0:              #ignoring csv header
                        header = row
                    else:
                        award_Year = row[3]            #storing contractor's award date
                        tender_status = row[4]         #storing contractor's tender status

                        if tender_status == "Awarded to Suppliers":        #Prevent storing tender status
                            index = index
                        else:
                            if award_Year[:4] in cList:                   #check for duplicate awarded year
                                cList[award_Year[:4]] += 1                #if duplicate, sum their amount up
                            else:
                                cList[award_Year[:4]] = 1                  #if not duplicate, store their amount
                    index += 1

                return cList
        except Exception as e:        #catch exception error
            print e.__doc__
            print e.message


    def amtT(path1):                                      #this function return the $ amount of tender per year
        try:
            with open(path1, 'rb') as f:                  #open govt procuremenr csv file
                reader = csv.reader(f)                    #read csv file
                cList = {}
                index = 0
                for row in reader:                        #loop through all coluumns and rows in csv file
                    if index == 0:                        #ignoring csv header
                        header = row
                    else:
                        award_Year = row[3]                #storing contractor's award date
                        tender_amt = row[6]                 #storing contractor's tender status

                        if award_Year[:4] in cList:                                  #check for duplicate awarded year
                            cList[award_Year[:4]] += float(tender_amt)               #if duplicate, sum their amount up
                        else:
                            cList[award_Year[:4]] = float(tender_amt)                #if not duplicate, store their amount
                    index += 1
                return cList

        except Exception as e:         #catch exception error
            print e.__doc__
            print e.message


    def top5(path1):                                 #this function will be used for top 5 contractors graph
        try:
            with open(path1, 'rb') as f:             #open govt procuremenr csv file
                reader = csv.reader(f)               #read csv file
                cList = {}

                index = 0
                for row in reader:                     #loop through all coluumns and rows in csv file
                    if index == 0:                     #ignoring csv header
                        header = row
                    else:
                        contractor = row[5]              #storing contractor's name
                        amt = row[6]                     #storing contractor's procurement amt

                        if contractor in cList:                                 #check for duplicate contractor name
                            cList[contractor] += float(amt)                     #if duplicate, sum their amount up
                        else:
                            cList[contractor] = float(amt)                       #if not duplicate, store their amount
                    index += 1


                #cList = sorted(cList, key=cList.get, reverse=True)[:5]
                dList = sorted(cList.iteritems(), key=lambda (k, v): (v, k), reverse=True)[:5]            #sort the list by top 5
                dList = dict(dList)                                                                       #convert top 5 list to dictionary
                return dList

        except Exception as e:           #catch exception error
            print e.__doc__
            print e.message


    def top5List(path1):
        try:
            with open(path1, 'rb') as f:                     #open govt procuremenr csv file
                reader = csv.reader(f)                       #read csv file
                cList = {}

                index = 0
                for row in reader:                             #loop through all coluumns and rows in csv file
                    if index == 0:                             #ignoring csv header
                        header = row
                    else:
                        contractor = row[5]                     #storing contractor's name
                        amt = row[6]                            #storing contractor's procurement amt

                        if contractor in cList:                         #check for duplicate contractor name
                            cList[contractor] += float(amt)             #if duplicate, sum their amount up
                        else:
                            cList[contractor] = float(amt)              #if not duplicate, store their amount
                    index += 1


                #cList = sorted(cList, key=cList.get, reverse=True)[:5]
                cList = dict(cList)
                cd = sorted(cList.items(), key=operator.itemgetter(1), reverse=True)[:5]      #sort the list by top 5
                dList = OrderedDict(cd)                                                       #convert top 5 list to ordered dictionary to retain order
                return dList

        except Exception as e:       #catch exception error
            print e.__doc__
            print e.message


    def pdfRegistered(path1, path2):
        try:
            with open(path1, "rb") as fp1:                 #open reg contractors csv file
                file2 = csv.reader(fp1)                    #read csv file
                rContractors = []
                for i in file2:                            #store contractor's name in list
                    rContractors.append(i[0])

            with open(path2, 'rb') as f:                   #open govt procuremenr csv file
                reader = csv.reader(f)                     #read csv file
                cList = {}

                index = 0
                for row in reader:                          #loop through all coluumns and rows in csv file
                    if index == 0:                          #ignoring csv header
                        header = row
                    else:
                        contractor = row[5]                  #storing contractor's name
                        amt = row[6]                         #storing contractor's procurement amt

                        if contractor in cList:                               #check for duplicate contractor name
                            cList[contractor] += float(amt)                   #if duplicate, sum their amount up
                        else:
                            cList[contractor] = float(amt)                    #if not duplicate, store their amount
                    index += 1

            class DataToPdf():
                """
                Export a list of dictionaries to a table in a PDF file.
                """
                def __init__(self, field, data, title=None):
                    """
                    Arguments:
                        fields - A tuple of tuples ((fieldname/key, display_name))
                            specifying the fieldname/key and corresponding display
                            name for the table header.
                        data - The data to insert to the table formatted as a list of
                            dictionaries.
                        title - The title to display at the beginning of the document.
                    """
                    self.fields = fields
                    self.data = data
                    self.title = title

                def export(self, filename, data_align='CENTER', table_halign='CENTER'):
                    """
                    Export the data to a PDF file.

                    Arguments:
                        filename - The filename for the generated PDF file.
                        data_align - The alignment of the data inside the table (eg.
                            'LEFT', 'CENTER', 'RIGHT')
                        table_halign - Horizontal alignment of the table on the page
                            (eg. 'LEFT', 'CENTER', 'RIGHT')
                    """
                    doc = SimpleDocTemplate(filename, pagesize=letter)

                    styles = getSampleStyleSheet()
                    styleH = styles['Heading1']

                    story = []

                    if self.title:
                        story.append(Paragraph(self.title, styleH))
                        story.append(Spacer(1, 0.25 * inch))

                    converted_data = self.__convert_data()
                    table = Table(converted_data, hAlign=table_halign)
                    table.setStyle(TableStyle([
                        ('FONT', (0, 0), (-1, 0), 'Helvetica'),
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        ('ALIGN',(0, 0),(0,-1), data_align),
                        ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                    ]))

                    story.append(table)
                    doc.build(story)

                def __convert_data(self):
                    """
                    Convert the list of dictionaries to a list of list to create
                    the PDF table.
                    """
                    # Create 2 separate lists in the same order: one for the
                    # list of keys and the other for the names to display in the
                    # table header.
                    keys, names = zip(*[[k, n] for k, n in self.fields])
                    new_data = []

                    for d in self.data:
                        new_data.append([d[k] for k in keys])

                    return new_data

            cList = {i: j for i, j in cList.items() if i in rContractors}                    #compare rContractors and cList for common values and store in list
            dList = dict(cList)                                                              #convert cList into dictionary
            data = []
            for key, value in dList.iteritems():                                             #loop through the dictionary to get they keys and values
                        data.append({'Contractor': key,
                                     'Amt': '$' + '%.2f' % value})

            fields = (
                ('Contractor', 'key'),
                ('Amt', 'value'),
            )

            doc = DataToPdf(fields, data, title="List of Registered Contractors' Procurement")

            #get current file directory
            current_directory = os.getcwd()
            final_directory = os.path.join(current_directory, r'RegisteredContractors.pdf')

            #export to final file directory
            doc.export(final_directory)

        except Exception as e:                     #catch exception error
            print e.__doc__
            print e.message


    def pdfTop5(path2):
        try:
            with open(path2, 'rb') as f:                  #open govt procuremenr csv file
                reader = csv.reader(f)                    #read csv file
                cList = {}

                index = 0
                for row in reader:                         #loop through all coluumns and rows in csv file
                    if index == 0:                         #ignoring csv header
                        header = row
                    else:
                        contractor = row[5]                #storing contractor's name
                        amt = row[6]                       #storing contractor's procurement amt

                        if contractor in cList:                             #check for duplicate contractor name
                            cList[contractor] += float(amt)                 #if duplicate, sum their amount up
                        else:
                            cList[contractor] = float(amt)                  #if not duplicate, store their amount
                    index += 1


            class DataToPdf():
                """
                Export a list of dictionaries to a table in a PDF file.
                """
                def __init__(self, field, data, title=None):
                    """
                    Arguments:
                        fields - A tuple of tuples ((fieldname/key, display_name))
                            specifying the fieldname/key and corresponding display
                            name for the table header.
                        data - The data to insert to the table formatted as a list of
                            dictionaries.
                        title - The title to display at the beginning of the document.
                    """
                    self.fields = fields
                    self.data = data
                    self.title = title

                def export(self, filename, data_align='CENTER', table_halign='CENTER'):
                    """
                    Export the data to a PDF file.

                    Arguments:
                        filename - The filename for the generated PDF file.
                        data_align - The alignment of the data inside the table (eg.
                            'LEFT', 'CENTER', 'RIGHT')
                        table_halign - Horizontal alignment of the table on the page
                            (eg. 'LEFT', 'CENTER', 'RIGHT')
                    """
                    doc = SimpleDocTemplate(filename, pagesize=letter)

                    styles = getSampleStyleSheet()
                    styleH = styles['Heading1']

                    story = []

                    if self.title:
                        story.append(Paragraph(self.title, styleH))
                        story.append(Spacer(1, 0.25 * inch))

                    converted_data = self.__convert_data()
                    table = Table(converted_data, hAlign=table_halign)
                    table.setStyle(TableStyle([
                        ('FONT', (0, 0), (-1, 0), 'Helvetica'),
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        ('ALIGN',(0, 0),(0,-1), data_align),
                        ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                    ]))

                    story.append(table)
                    doc.build(story)

                def __convert_data(self):
                    """
                    Convert the list of dictionaries to a list of list to create
                    the PDF table.
                    """
                    # Create 2 separate lists in the same order: one for the
                    # list of keys and the other for the names to display in the
                    # table header.
                    keys, names = zip(*[[k, n] for k, n in self.fields])
                    new_data = []

                    for d in self.data:
                        new_data.append([d[k] for k in keys])

                    return new_data

            # cList = sorted(cList, key=cList.get, reverse=True)[:5]
            dList = sorted(cList.iteritems(), key=lambda (k, v): (v, k), reverse=True)[:5]                #sort the list by top 5
            dList = dict(dList)                                                                           #convert top 5 list to dictionary

            data = []
            for key, value in dList.iteritems():                                                          #loop through the dictionary to get they keys and values
                        data.append({'Contractor': key,
                                     'Amt': '$' + '%.2f' % value})

            fields = (
                ('Contractor', 'key'),
                ('Amt', 'Amt'),
            )

            doc = DataToPdf(fields, data, title="Top 5 Contractors with Procurement Amt")

            # get current file directory
            current_directory = os.getcwd()
            final_directory = os.path.join(current_directory, r'Top5Contractors.pdf')

            # export to final file directory
            doc.export(final_directory)

        except Exception as e:               #catch exception error
            print e.__doc__
            print e.message


    def bigPlayerFunc(path1):              #this function will be used for the displaying of descending order of big player table (default order)
        try:
            with open(path1, 'rb') as f:             #open govt procuremenr csv file
                reader = csv.reader(f)               #read csv file
                cList = {}

                index = 0
                for row in reader:                  #loop through all coluumns and rows in csv file
                    if index == 0:                  #ignoring csv header
                        header = row
                    else:
                        contractor = row[5]          #storing contractor's name
                        tenderNo = row[6]            #storing contractor's no. of tendering times

                        if contractor == "na":          #Prevent storing contractor's name of "NA"
                            index = index
                        else:
                            if contractor in cList:            #check for duplicate contractor name
                                cList[contractor] += 1         #if duplicate, sum their amount up
                            else:
                                cList[contractor] = 1          #if not duplicate, store their amount
                    index += 1

            dList = sorted(cList.items(), key=operator.itemgetter(1), reverse=True)             #sort into list of descending values
            gList = OrderedDict(dList)                                                          #onvert list into dictionary to retain order
            return gList
        except Exception as e:              #catch exception error
            print e.__doc__
            print e.message


    def AscbigPlayerFunc(path1):                   #this function will be used for the displaying of ascending order of big player table
        try:
            with open(path1, 'rb') as f:           #open govt procuremenr csv file
                reader = csv.reader(f)             #read csv file
                cList = {}

                index = 0
                for row in reader:                 #loop through all coluumns and rows in csv file
                    if index == 0:                 #ignoring csv header
                        header = row
                    else:
                        contractor = row[5]        #storing contractor's name
                        tenderNo = row[6]          #storing contractor's no. of tendering times

                        if contractor == "na":          #Prevent storing contractor's name of "NA"
                            index = index
                        else:
                            if contractor in cList:                #check for duplicate contractor name
                                cList[contractor] += 1             #if duplicate, sum their amount up
                            else:
                                cList[contractor] = 1              #if not duplicate, store their amount
                    index += 1

            dList = sorted(cList.items(), key=operator.itemgetter(1))             #sort into list of ascending values
            gList = OrderedDict(dList)                                            #onvert list into dictionary to retain order
            return gList
        except Exception as e:                #catch exception error
            print e.__doc__
            print e.message


    def bigPlayerDetails1(path1, coyName):                         #this function will be used for the displaying of no.of tender for 2 columned bar-graph
        try:
            with open(path1, 'rb') as f:                           #open govt procuremenr csv file
                reader = csv.reader(f)                             #read csv file
                cList = {"2015": 0, "2016": 0, "2017": 0}          #setting a default list values, to be overridden

                index = 0
                for row in reader:                                 #loop through all coluumns and rows in csv file
                    if index == 0:                                 #ignoring csv header
                        header = row
                    else:
                        award_Year = row[3]                        #storing contractor's awarded date
                        contractor = row[5]                        #storing contractor's name
                        amt = row[6]

                        if contractor != coyName:                  #check if contractor's name is same as companyname (from parameter)
                            index = index                          #if not, continue
                        else:
                            if award_Year[:4] in cList:            #check for duplicate contractor awarded year
                                cList[award_Year[:4]] += 1         #if duplicate, sum their amount up
                            else:
                                cList[award_Year[:4]] = 1          #if not duplicate, store their amount
                    index += 1

            print cList
            return cList
        except Exception as e:                                    #catch exception error
            print e.__doc__
            print e.message


    def bigPlayerDetails2(path1, coyName):                        #this function will be used for the displaying of ($)amt.of tender for 2 columned bar-graph
        try:
            with open(path1, 'rb') as f:                          #open govt procuremenr csv file
                reader = csv.reader(f)                            #read csv file
                cList = {"2015": 0, "2016": 0, "2017": 0}         #setting a default list values, to be overridden

                index = 0
                for row in reader:                                #loop through all coluumns and rows in csv file
                    if index == 0:                                #ignoring csv header
                        header = row
                    else:
                        award_Year = row[3]                       #storing contractor's awarded date
                        contractor = row[5]                       #storing contractor's name
                        tender_amt = row[6]                       #storing contractor's tender amt (#)

                        if contractor != coyName:                  #check if contractor's name is same as companyname (from parameter)
                            index = index                          #if not, continue
                        else:
                            if award_Year[:4] in cList:                                #check for duplicate contractor awarded year
                                cList[award_Year[:4]] += float(tender_amt)             #if duplicate, sum their amount up
                            else:
                                cList[award_Year[:4]] = float(tender_amt)              #if not duplicate, store their amount
                    index += 1
            print cList
            return cList
        except Exception as e:       #catch exception error
            print e.__doc__
            print e.message

except Exception as e:  # catch exception error
    print e.__doc__
    print e.message