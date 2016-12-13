import csv
from lxml import html
import requests
import time

class WebScraper:
    def __init__(self):
        pass

    def interpreter(self,array):
        string = ""
        for i in range(len(array)):
            newPhrase = array[i].strip('\n')
            if(newPhrase != '\n'):
                string += newPhrase
        return string

    def getOfferings(self,unit):
        targetURL = 'http://www.monash.edu.au/pubs/handbooks/units/' + unit + '.html'
        page = requests.get(targetURL)
        tree = html.fromstring(page.content)
        offers = tree.xpath('//li[@class="pub_preamble_value_offerings"]//foo/@attribute')
        string = self.interpreter(offers)
        return string

    def getSypnosis(self,unit):
        targetURL = 'http://www.monash.edu.au/pubs/handbooks/units/' + unit + '.html'
        page = requests.get(targetURL)
        tree = html.fromstring(page.content)
        sypnosis = tree.xpath('//div[@class=" uge-synopsis-content"]//text()')
        string = self.interpreter(sypnosis)
        return string

    def getPreq(self,unit):
        targetURL = 'http://www.monash.edu.au/pubs/handbooks/units/' + unit + '.html'
        page = requests.get(targetURL)
        tree = html.fromstring(page.content)
        preq = tree.xpath('//div[@class=" uge-prerequisites-content"]//text()')
        string = self.interpreter(preq)
        return string

    def getProhibitions(self,unit):
        targetURL = 'http://www.monash.edu.au/pubs/handbooks/units/' + unit + '.html'
        page = requests.get(targetURL)
        tree = html.fromstring(page.content)
        proh = tree.xpath('//div[@class=" uge-prohibitions-content"]//text()')
        string = self.interpreter(proh)
        return string

    def getUnitValue(self,unit):
        targetURL = 'http://www.monash.edu.au/pubs/handbooks/units/' + unit + '.html'
        page = requests.get(targetURL)
        tree = html.fromstring(page.content)
        unitVal = tree.xpath('//h2//text()')
        string = self.interpreter(unitVal)
        score = unitVal[0]
        score = score.split(',')
        newarray = []
        finalarray = []
        for item in score:
            if item[0] == ' ':
                item = item[1:]
            newarray.append(item)
        finalarray.append(newarray[0].split()[0])
        finalarray.append(newarray[1].split()[-1])
        finalarray.append(newarray[2].split()[0])

        return finalarray


    def getLocations(self,unit):
        targetURL = 'http://www.monash.edu.au/pubs/handbooks/units/' + unit + '.html'
        page = requests.get(targetURL)
        tree = html.fromstring(page.content)
        lengthofIterations = len(tree.xpath('//div[@class="preamble_entry"]//div[@class="pub_preamble_value"]/*'))//2
        array = []
        print(lengthofIterations)
        for i in range(1, lengthofIterations+1):
            base = '//div[@class="preamble_entry"]//div[@class="pub_preamble_value"]'
            locStrig = base + '/p[' + str(i) + ']/a//text()'
            semester = base + '/ul[' + str(i) + ']/li//text()'

            locResult = tree.xpath(locStrig)
            semResult = tree.xpath(semester)
            pushEle = [locResult, semResult]
            array.append(pushEle)
        #location = tree.xpath('//div[@class="preamble_entry"]//div[@class="pub_preamble_value"]/p[2]/a//text()')
        #date = tree.xpath('//div[@class="preamble_entry"]//div[@class="pub_preamble_value"]/ul[2]/li//text()')
        return array

webScraper = WebScraper()

def convsubtoarray(fileName,faculty):
    if(faculty == "ada"):
        fac = "Faculty of Arts, Design and Architecture"
    elif (faculty == "arts"):
        fac = "Faculty of Arts"
    elif (faculty == "buseco"):
        fac = "Faculty of Business and Economics"
    elif (faculty == "edu"):
        fac = "Faculty of Education"
    elif (faculty == "eng"):
        fac = "Faculty of Engineering"
    elif (faculty == "it"):
        fac = "Faculty of Information Techonology"
    elif (faculty == "law"):
        fac = "Faculty of Law"
    elif(faculty == "med"):
        fac = "Faculty of Medicine, Nursing and Health Sciences"
    elif (faculty == "pha"):
        fac = "Faculty of Pharmacy and Pharmaceutical Sciences"
    elif (faculty == "sci"):
        fac = "Faculty of Sciences"
    else:
        fac =faculty #return faculty if it doesnt satisfy anythin
    file = open(fileName,'r')
    array=[]
    for line in file:
        record=line.strip()
        record = record.split(' ',1)
        unitCode=str(record[0])
        unitName=record[1]
        print("Getting Record for " + unitCode + '(' +faculty +')')
        print('waiting')
        time.sleep(5)

        syp = webScraper.getSypnosis(unitCode)
        if syp != '':
            #assume its an empty page
            preq = webScraper.getPreq(unitCode)
            proh = webScraper.getProhibitions(unitCode)
            unitScoreData = webScraper.getUnitValue(unitCode)
            locAndTime = webScraper.getLocations(unitCode)
            pair=[unitCode,unitName,fac,locAndTime,unitScoreData[0],unitScoreData[2],preq,proh,unitScoreData[1],syp]
            array.append(pair)
    return array

import csv

def toCSV(array):
    CSVfileName = 'dbUpdated.csv'
    fl = open(CSVfileName, 'w')

    writer = csv.writer(fl)
    writer.writerow(['UnitCode', 'UnitName','Faculty','LocationAndTime','CreditPoints','EFTSL',"Preqs","Proh",'SCABand',"Sypnosis"]) #if needed
    for values in array:
        writer.writerow(values)
    fl.close()

faculties = ['ada','arts','buseco','edu','eng','it','law','med','pha','sci']
newarray = []
for f in faculties:
    fileName = f + '.txt'
    array = convsubtoarray(fileName,f)
    newarray += array
newarray = sorted(newarray, key=lambda db: db[0])
toCSV(newarray)
