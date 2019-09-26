import csv
import os.path
import pandas as pd

try:
    def function2BackEnd(procurement_file_path):

        try:
            # get current directory file path and create a folder inside the current directory
            current_directory = os.getcwd()
            final_directory = os.path.join(current_directory, r'agencies')
            if not os.path.exists(final_directory):
                os.makedirs(final_directory)

            # write a new file with agency as its header write all its respective rows into each agency file
            with open(procurement_file_path, "r") as csvfile:
                reader = csv.reader(csvfile, dialect='excel')
                csvfile.readline()
                for row in reader:
                    fname = str(row[1])
                    f = open('agencies/%s.txt' % fname, 'a+')
                    row_str = str(row).strip('[').strip(']')
                    f.write(row_str + '\n')
                    f.close()

        # catch exception error
        except Exception as e:
            print e.__doc__
            print e.message

    def fuction2Graph(path):

        try:
            data = pd.read_csv(path, encoding="ISO-8859-1", engine='python')
            companynames = set(data['agency'])
            return companynames

        # catch exception error
        except Exception as e:
            print e.__doc__
            print e.message


    # return file path
    def fuction2Data(path):

        try:
            return pd.read_csv(path, encoding="ISO-8859-1", engine='python')

        # catch exception error
        except Exception as e:
            print e.__doc__
            print e.message

 # catch exception error
except Exception as e:
    print e.__doc__
    print e.message