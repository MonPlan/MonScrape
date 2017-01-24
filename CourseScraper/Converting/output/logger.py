import requests
import csv
import json
import os
import math

def readme(code):
    targetFile = "./" + code + ".json"
    print(code)
    data = json.loads(open((targetFile), "r").read())

    cCode = data['courseCode']
    courseName = data['courseName']
    courseType = data['courseType']
    aos = data['courseAOS']
    courseName += " (" + str(aos) + ")"

    output = {"courseCode": code, "courseName": courseName, "courseType": courseType}

    return output

fullDatabase = []
for filename in os.listdir("."):
    if filename != "python2.py" and filename != "python.py" and  filename != "output" and filename != "updated" and filename.endswith('.json'): #converts all the file except for the Python File
        outputDir = filename.rstrip('.json')
        output = readme(outputDir)
        fullDatabase.append(output)

with open("./0_output.json", "w") as json_file:
    json_file.write(json.dumps(fullDatabase, indent=4, sort_keys=True))
