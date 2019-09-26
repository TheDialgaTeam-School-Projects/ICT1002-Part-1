import csv
from Tkinter import *
import pandas as pd

#This function reads a csv file as an argument, stores the data in a dictionary and returns the dictionary
try:
    def csvTodict(csvfile):
        try:
            #open and read the csv file
            file = open(csvfile, 'rb')
            reader = csv.reader(file)
            title = reader.next()

            #after reading the first line the values are stored in a dictionary as keys and creates and empty list as the value. The keys are also the headers
            column = {}
            for t in title:
                column[t] = []

            #stores the data as values of the key in a list
            for row in reader:
                for key, value in zip(title, row):
                    column[key].append(value)

            return column

        except Exception as e:  # catch exception error
            print e.__doc__
            print e.message

# catch exception error
except Exception as e:
    print e.__doc__
    print e.message