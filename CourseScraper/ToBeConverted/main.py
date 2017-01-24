import requests
import csv
import json
import os
import math

################################
# function unitInterperter()
# arg: @unit, @faculty
# returns: a JSON obect about the unit
# unit: the unit object
# faculty: managing faculty
# author: lorderikir
################################
def unitInterperter(unit, faculty):
    address = "http://api.monplan.tech:3000/units/"

    try:
        me = unit['type']
        notJSON = True
    except TypeError:
        #not a JSON object
        notJSON = False

    if isinstance(unit, list):
        #it an array, so optional
        options = ""
        for i in range(0, len(unit)-1):
            options += unit[i] + ","
        options += unit[-1]
        output = {"UnitCode": "Choose One", "UnitName": options, "SCABand": 0, "CreditPoints": 0, "Faculty": faculty}
    elif(unit == "Elective"):
        #ouput is an elective
        output = {"UnitCode": "Free Elective", "UnitName": "Choose from any faculty", "SCABand": 0, "CreditPoints": 0, "Faculty": "Faculty of All"}
    elif(notJSON == True):
        #its an JSON object:
        output = {"UnitCode": unit['type'], "UnitName": "", "SCABand": 0, "CreditPoints": 0, "Faculty": unit['faculty']}
    else:
        #assume its a normal unit, so do an API call
        try:
            # attempt to get a response from the API
            targetURL = address + str(unit)
            r = requests.get(targetURL)
            output = r.json()
        except:
            # in the event of Response 404, Builds a Custom Unit which States Cannot Fetch Data
            output = {"UnitCode": unit, "UnitName": "Cannot Fetch Data", "SCABand": 0, "CreditPoints": 0, "Faculty": ""}

    return output




def readme(code):
    file_name = "./output/" + code + ".json"
    with open(file_name, "w") as json_file:
        targetFile = "./" + code + ".json"
        print(targetFile)
        data = json.loads(open((targetFile), "r").read())

        teachingPeriods = data['teachingPeriods']
        code = data['courseCode']
        courseName = data['courseName']
        courseType = data['courseType']

        output = {"courseCode": code, "courseName": courseName, "courseType": courseType, "teachingPeriods": []}


        for i in range(0, len(teachingPeriods)):
            currentTeachingPeriod = teachingPeriods[i]
            units = currentTeachingPeriod["units"]
            currentYear = currentTeachingPeriod["year"]
            currenTP = currentTeachingPeriod["code"]
            numberOfUnits = len(units)
            teachingPeriodObj = {"code": currenTP, "year": currentYear, "numberOfUnits": numberOfUnits, "units": []}
            for j in range(0, numberOfUnits):
                currentUnit = unitInterperter(units[j], faculty)
                teachingPeriodObj["units"].append(currentUnit)
            output["teachingPeriods"].append(teachingPeriodObj)



        json_file.write(json.dumps(output, indent=4, sort_keys=True))

for filename in os.listdir("./"):
    if filename != "main.py" and filename != "output" and filename.endswith(".json"): #converts all the file except for the Python File
            outputDir = filename.rstrip('.json')
            readme(outputDir)
