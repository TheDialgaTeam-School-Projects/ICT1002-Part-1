import csv
import datetime
'''
List of Ministry Avaiable
'''
defaultMinistryList = ['Ministry of Finance',"Prime Minister's Office","Ministry of National Development","Ministry of Transport",
                       "Ministry of Trade and Industry","Ministry of Culture","Ministry of Social and Family Development",
                       "Ministry of Education","Ministry of Manpower","Ministry of Home Affairs","Ministry of Defence",
                       "Ministry of the Environment and Water Resources","Ministry of Foreign Affairs","Ministry of Health",
                       "Ministry of Communication and Information","Ministry of Law","Parliament of Singapore"]

def fileCheck():
    '''
    to check for category file, if doesn't exist fail gracefully
    '''
    try:
        with open('Ministry.csv', 'r') as file:
            return True
    except IOError:
        return False

def createdefaultFile(agency, ministry):
    '''
    Create the category file according with user input
    '''
    if(fileCheck()):
        updateValue(agency,ministry)
    else:
        with open('Ministry.csv', "w") as file:
            file.write('agency,Ministry\n')
            file.write('%s,%s\n' % (agency, ministry))
        open("Ministry.csv")

def getAllMinistryList():
    '''
    return all default list
    '''
    return defaultMinistryList

def updateValue(agency,ministry):
    '''
    Update the ministry value inside the file
    :param agency:
    :param ministry:
    :return:
    '''
    lineAgency = []
    lineMinistry = []
    exist = False
    with open("Ministry.csv","r") as file:
        reader = csv.DictReader(file, delimiter=',', skipinitialspace=True)
        for row in reader:
            if row["agency"] == agency:
                row["Ministry"] = ministry
                exist = True
            lineAgency.append(row["agency"])
            lineMinistry.append(row["Ministry"])
    with open('Ministry.csv', "w") as file:
        file.write('agency,Ministry\n')
        for count in range(len(lineAgency)):
            file.write('%s,%s\n' % (lineAgency[count], lineMinistry[count]))
        if not exist:
            file.write('%s,%s\n' % (agency, ministry))

def getSelectedAgencyByMinistry(ministryWord):
    '''
    return a list of agency by their ministry from ministry.csv
    :param ministryWord:
    :return:
    '''
    with open("Ministry.csv") as csvfile: #need CSV file to be around
        data= csv.DictReader(csvfile, delimiter=',', skipinitialspace=True)
        category = []
        for row in data:
            if row['Ministry'] == ministryWord:
                category.append(row['agency'])
        return category

def getAllAgency(fileLoc):
    '''
    get all agency from the csvfile
    :param fileLoc:
    :return:
    '''
    with open(fileLoc) as csvfile:
        data = csv.DictReader(csvfile, delimiter=',', skipinitialspace=True)
        agencyList =[]
        for row in data:
            if row['agency'] not in agencyList:
                agencyList.append(row['agency'])
        return agencyList

def getAmountByAgency(fileLoc,agency,year=None):
    '''
    get all amount spend by agency with overloaded in case there is a year variable
    :param fileLoc:
    :param agency:
    :param year:
    :return:
    '''
    amount =0
    if year is None:
        with open(fileLoc) as csvfile:
            data = csv.DictReader(csvfile, delimiter=',', skipinitialspace=True)
            for row in data:
                if row['agency'] == agency:
                    amount += float(row['awarded_amt'])
    else:
        dateStart = datetime.datetime.strptime('1/1/' + year, '%m/%d/%Y')
        dateEnd = datetime.datetime.strptime('1/1/' + str(int(year) + 1), '%m/%d/%Y')
        with open(fileLoc) as csvfile:
            data = csv.DictReader(csvfile, delimiter=',', skipinitialspace=True)
            for row in data:
                if row['agency'] == agency and \
                        datetime.datetime.strptime(row['award_date'], '%Y-%m-%d') > dateStart and \
                        datetime.datetime.strptime(row['award_date'], '%Y-%m-%d') < dateEnd:
                    amount += float(row['awarded_amt'])
    return amount

def getAmountList(fileLoc,agencyList, year=None):
    '''
    Overloaded method for year
    :param fileLoc:
    :param agencyList:
    :return:
    '''
    amountList = []
    for count in range(len(agencyList)):
        amountList.append(getAmountByAgency(fileLoc,agencyList[count],year))
    return amountList

def getAmountForAllMinistry(fileLoc,year=None):
    '''
    Overloaded method to do for both year and no year
    :param fileLoc:
    :param date:
    :return:
    '''
    amount = []
    ministryList = getAllMinistryList()
    for ministry in ministryList:
        amount.append(getAmountByMinistry(ministry,fileLoc,year))
    return amount

def getAmountByMinistry(ministry,fileLoc,year=None):
    '''
    Overloaded to allow for year variable if given
    :param ministry:
    :param fileLoc:
    :param year:
    :return:
    '''
    amount = 0
    agencyList = getSelectedAgencyByMinistry(ministry)
    with open(fileLoc) as csvfile:
        data = csv.DictReader(csvfile,delimiter=',',skipinitialspace= True)
        for agency in agencyList:
            for row in data:
                if year is None:
                    if row['agency'] ==agency:
                        amount += float(row['awarded_amt'])
                else:
                    dateStart = datetime.datetime.strptime('1/1/' + year, '%d/%m/%Y')
                    dateEnd = datetime.datetime.strptime('1/1/' + str(int(year) + 1), '%d/%m/%Y')
                    if row['agency'] == agency and \
                            datetime.datetime.strptime(row['award_date'],'%Y-%m-%d')>dateStart and \
                            datetime.datetime.strptime(row['award_date'],'%Y-%m-%d') < dateEnd:
                        amount += float(row['awarded_amt'])
    return amount

def getUniqueDate(fileLoc):
    '''
    Get the range of years for the file
    :param fileLoc:
    :return:
    '''
    dateList = []
    with open(fileLoc) as csvfile:
        data = csv.DictReader(csvfile, delimiter=',', skipinitialspace=True)
        for row in data:
            if row['award_date'][:4] not in dateList:
                dateList.append(row['award_date'][:4])
    return dateList
