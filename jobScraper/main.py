from lxml import html
import requests
import json

class WebScraper:
    def __init__(self):
        self.baseURL = "http://joboutlook.gov.au/occupation.aspx?search=alpha&code="

    def getJobName(self, jobCode):
        targetURL = self.baseURL + jobCode
        page = requests.get(targetURL)
        tree = html.fromstring(page.content)
        jobName = tree.xpath('//*[@id="content"]/h1')
        return jobName[0].text


    def getJobOutlook(self,jobCode):
        targetURL = self.baseURL + jobCode + "&tab=stats&graph=EL"
        page = requests.get(targetURL)
        tree = html.fromstring(page.content)
        joboutlook = tree.xpath('//*[@class="JobOutlookTable"]//tr')
        data = []
        for row in joboutlook:
            data.append([c.text for c in row.getchildren()])
        return data[1:]
    

    def getSummary(self,jobCode):
        targetURL = self.baseURL + jobCode + "&tab=prospects"
        page = requests.get(targetURL)
        tree = html.fromstring(page.content)
        joboutlook = tree.xpath('//*[@class="JobOutlookTable"]//tr')
        data = []
        for row in joboutlook:
            data.append([c.text for c in row.getchildren()])
        data = data[1:]
        returnArray = []
        for i in range(len(data)):
            indicator = data[i]
            print(indicator)
            if(indicator[0] == "How many workers are employed in this occupation?"):
                indicatorType = "employedPersons"
                level = indicator[1]
                decile = indicator[2]
                if not level == "n/a": level = int(level.replace(',', ''))
                if not decile == "n/a": decile = int(decile)
            elif(indicator[0] == "What are the weekly earnings for full-time workers ($ before tax)?"):
                indicatorType = "yearlyIncomePreTax"
                level = indicator[1]
                decile = indicator[2]
                if not level == "n/a": level = int(level.replace(',', '')) * 50
                if not decile == "n/a": decile = int(decile)
            elif(indicator[0] == "How does unemployment compare with other occupations?"):
                indicatorType = "unemployment"
                decile = indicator[2]
                level = indicator[1]
                if not decile == "n/a": decile = int(decile)
            elif(indicator[0] == "What has been the long-term employment growth - 10 years (%)?"):
                indicatorType = "growthTenyr"
                decile = indicator[2]
                level = indicator[1]
                if not level == "n/a": level = float(level)
                if not decile == "n/a": decile = int(decile)
            elif(indicator[0] == "What has been the medium-term employment growth - 5 years (%)?"):
                indicatorType = "growthFiveYear"
                decile = indicator[2]
                level = indicator[1]
                if not level == "n/a": level = float(level)
                if not decile == "n/a": decile = int(decile)
            elif(indicator[0] == "What has been the short-term employment growth - 2 years (%)?"):
                indicatorType = "growthTwoYear"
                decile = indicator[2]
                level = indicator[1]
                if not level == "n/a": level = float(level)
                if not decile == "n/a": decile = int(decile)
            elif(indicator[0] == "What will be the likely future employment growth for the next five years?"):
                indicatorType = "futureGrowthFiveyear"
                decile = indicator[2]
                level = indicator[1]
                if not decile == "n/a": decile = float(int(decile)/10)
            elif(indicator[0] == "What will be the level of future job openings?"):
                indicatorType = "futureGrowthJobOpeningsLevel"
                decile = indicator[2]
                level = indicator[1]
                if not decile == "n/a": decile = float(int(decile)/10)
            indicatorObject = {"indicatorType": indicatorType, "level": level, "decile": decile }
            returnArray.append(indicatorObject)
        return returnArray

    def getEarnings(self,jobCode):
        targetURL = self.baseURL + jobCode + "&tab=stats&graph=EA"
        page = requests.get(targetURL)
        tree = html.fromstring(page.content)
        joboutlook = tree.xpath('//*[@class="JobOutlookTable"]//tr')
        data = []
        for row in joboutlook:
            data.append([c.text for c in row.getchildren()])
        data = data[1:]
        return data

if __name__ == "__main__":
    ws = WebScraper()
    array = []
    for i in range(1000, 9999):
        currentNumber = str(i)
        print(currentNumber)
        career = ws.getJobName(currentNumber)
        if career != "Occupation":
            careerOutlook = ws.getJobOutlook(currentNumber)

            outlook = []
            for item in careerOutlook:
                year = int(item[0])
                rating = float(item[1])*1000
                yearOutlook = {"year": year, "employedNumbers": rating}
                outlook.append(yearOutlook)
            
            earnings = ws.getEarnings(currentNumber)
            earningsArray = []
            for i in range(len(earnings)):
                item = earnings[i]
                earnType = item[0]
                currentOccupation = item[1]
                allOccupation = item[2]
                earn = {"earnType": earnType, "currentOccupation": currentOccupation, "allOccupation": allOccupation}
                earningsArray.append(earn)

            currentCareer = {"careerName": career, "employedPeople": outlook, "averageEarnings": earningsArray}

            summary = ws.getSummary(currentNumber)
            for item in summary:
                indicator = item["indicatorType"]
                level = item["level"]
                decile = item["decile"]
                currentCareer[indicator] = {"level": level, "decile": decile}
            # outlookSummary = []
            # for item in summary:
            #     indicator = item[0]
            #     if item[1] != "n/a":
            #         level = (item[1])
            #     if item[2] != "n/a":
            #         decile = int(item[2])
            #     sumR = {"indicator": indicator, "level": level, "decile": decile}
            #     outlookSummary.append(sumR)
            
           
            array.append(currentCareer)
        


    with open("main.json", "w") as json_file:
        json_file.write(json.dumps(array, indent=4, sort_keys=True))