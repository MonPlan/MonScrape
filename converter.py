import csv
from lxml import html
import requests

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

webScraper = WebScraper()

def convsubtoarray(fileName,faculty):
    file = open(fileName,'r')
    array=[]
    for line in file:
        record=line.strip()
        record = record.split(' ',1)
        unitCode=str(record[0])
        unitName=record[1]
        print("Getting Record for " + unitCode + '(' +faculty +')')
        syp = webScraper.getSypnosis(unitCode)
        preq = webScraper.getPreq(unitCode)
        proh = webScraper.getProhibitions(unitCode)
        pair=[unitCode,unitName,faculty,syp,preq,proh]
        array.append(pair)
    return array

import csv

def toCSV(array):
    CSVfileName = 'dbUpdated.csv'
    fl = open(CSVfileName, 'w')

    writer = csv.writer(fl)
    writer.writerow(['UnitCode', 'UnitName', 'Faculty',"Sypnosis","Preqs","Proh"]) #if needed
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
