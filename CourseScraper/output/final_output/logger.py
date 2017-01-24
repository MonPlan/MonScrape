course_codes = ["3971","4520","4530","A2000","A2001","A2003","A2004","A2005","B2000","B2001","B2003","B2004","B2006","B2007","B2008","B2009","B2012","B2013","B2014","B2016","B2017","B2018","B2019","B2020","B2021","B2022","B2023","B2024","B2025","B6002","B6003","B6004","B6005","B6009","B6011","B6012","B6013","B6014","B6015","C2000","C2001","C2002","C2003","C3001","D3001","D3002","D3003","D3004","D3005","D3006","D3007","D3008","D3009","E3001","E3002","E3003","E3004","E3005","E3006","E3007","E3009","E6001","F2001","F2003","F2004","F2005","F2006","F2007","F3001","F6001","F6002","L3002","L3003","L3004","L3005","L3006","L3007","L3009","M2001","M2002","M2003","M2006","M3001","M3002","M3004","M3005","M3006","M6018","P2001","P3001","P3002","P6001","S2000","S2003","S2004","S2005","S2006","S2007","S3001","S3002","S6001","S6002"]

import requests
import csv
import json
import os
import math

def gencourseName(name, courseType):
    if(courseType == "Bachelor degree"):
        return "Bachelor of " + name
    elif(courseType == "Bachelor degree (honours)"):
        return "Bachelor of " + name + " (honours)"
    elif(courseType == "Bachelor degree (honours)/Bachelor degree" or courseType == "Bachelor degree /Bachelor degree" or courseType ==  "Bachelor degree (honours)/Bachelor degree (honours)"):
        return "Bachelor of  " + name + " (double)"
    elif(courseType == "Expert master degree" or courseType == "Master degree"):
        return "Master of " + name
    else:
        return courseType + " " + name

fullDatabase = []
for i in range(0, len(course_codes)):
    currentCourse = course_codes[i]
    complete = 0
    incrementer = 0

    targetFile = "./" + currentCourse + "-0.json"
    print(currentCourse)
    try:
        data = json.loads(open((targetFile), "r").read())
        cCode = data['courseCode']
        name = data['courseName']
        courseType = data['courseType']
        courseFac = data['faculty']
        print(name, courseType)
        courseName = gencourseName(name, courseType)
        output = {"courseCode": cCode, "courseName": courseName, "managingFaculty": courseFac, "courseAOS": []}

        while incrementer < 50:
            try:
                filestring = currentCourse + "-" + str(incrementer)
                targetFile = filestring +".json"
                aosData = json.loads(open((targetFile), "r").read())
                courseAos = aosData['courseAOS']
                aosCode = filestring
                aosSummary = {"code": filestring, "aosName": courseAos}
                output["courseAOS"].append(aosSummary)
                incrementer += 1
            except FileNotFoundError:
                #exit i
                incrementer += 1
            except json.decoder.JSONDecodeError:
                incrementer += 1

        fullDatabase.append(output)
    except FileNotFoundError:
        pass
    except:
        pass

with open("./0_output.json", "w") as json_file:
    json_file.write(json.dumps(fullDatabase, indent=4, sort_keys=True))
