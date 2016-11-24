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

    def getUnitValue(self,unit):
        targetURL = 'http://www.monash.edu.au/pubs/handbooks/units/' + unit + '.html'
        page = requests.get(targetURL)
        tree = html.fromstring(page.content)
        unitVal = tree.xpath('//h2//text()')
        print(unitVal)
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

webScraper = WebScraper()
print(webScraper.getUnitValue('AHT2530'))
