
# course_codes = ["0020","0028","0029","0047","0057","0069","0079","0100","0190","0498","1322","2098","2116","2602","2603","2625","2627","2695","2700","2710","2932","2953","2977","3111","3194","3204","3262","3291","3292","3337","3379","3438","3443","3521","3736","3863","3940","3954","3971","4066","4067","4071","4080","4086","4087","4088","4091","4102","4103","4119","4307","4308","4320","4413","4414","4415","4502","4520","4530","4533","A0001","A0501","A0502","A0503","A2000","A2001","A2003","A2004","A2005","A2006","A2007","A3701","A3702","A6001","A6002","A6003","A6004","A6006","A6007","A6008","A6009","A6010","A6011","A6012","A6013","A6014","A6015","B2000","B2001","B2003","B2004","B2006","B2007","B2008","B2009","B2012","B2013","B2014","B2015","B2016","B2017","B2018","B2019","B2020","B2021","B2022","B2023","B2024","B2025","B2026","B2027","B3701","B3702","B4001","B5001","B5002","B5003","B6001","B6002","B6003","B6004","B6005","B6006","B6007","B6009","B6010","B6011","B6012","B6013","B6014","B6015","B6016","C2000","C2001","C2002","C2003","C3001","C3701","C3702","C4006","C5003","C6001","C6002","C6003","C6004","D0001","D0501","D0502","D2002","D3001","D3002","D3003","D3004","D3005","D3006","D3007","D3008","D3009","D3701","D4001","D4004","D4005","D5002","D6001","D6002","D6003","D6004","D6005","D6006","D6007","D6008","E3001","E3002","E3003","E3004","E3005","E3006","E3007","E3008","E3009","E3010","E3011","E6001","E6002","F2001","F2002","F2003","F2004","F2005","F2006","F2007","F3001","F3701","F3702","F6001","F6002","L3001","L3002","L3003","L3004","L3005","L3006","L3007","L3009","L5001","L6001","L6002","L6003","L6004","L6005","L6006","L6007","L6011","L6012","M2001","M2002","M2003","M2004","M2006","M3001","M3002","M3003","M3004","M3005","M3006","M3007","M3701","M3702","M3703","M3704","M4002","M4006","M4017","M5003","M5004","M5007","M5010","M5013","M5017","M5018","M6001","M6002","M6003","M6004","M6005","M6006","M6007","M6008","M6009","M6010","M6011","M6012","M6014","M6015","M6016","M6017","M6018","M6021","M6022","M6023","M6024","M6025","M6026","M6027","M6028","P2001","P3001","P3002","P3701","P4001","P6001","P6002","P6003","S2000","S2003","S2004","S2005","S2006","S2007","S2008","S2009","S3001","S3002","S3701","S6001","S6002"]
course_codes = ["3971","4520","4530","A2000","A2001","A2003","A2004","A2005","B2000","B2001","B2003","B2004","B2006","B2007","B2008","B2009","B2012","B2013","B2014","B2016","B2017","B2018","B2019","B2020","B2021","B2022","B2023","B2024","B2025","B6002","B6003","B6004","B6005","B6009","B6011","B6012","B6013","B6014","B6015","C2000","C2001","C2002","C2003","C3001","D3001","D3002","D3003","D3004","D3005","D3006","D3007","D3008","D3009","E3001","E3002","E3003","E3004","E3005","E3006","E3007","E3009","E6001","F2001","F2003","F2004","F2005","F2006","F2007","F3001","F6001","F6002","L3002","L3003","L3004","L3005","L3006","L3007","L3009","M2001","M2002","M2003","M2006","M3001","M3002","M3004","M3005","M3006","M6018","P2001","P3001","P3002","P6001","S2000","S2003","S2004","S2005","S2006","S2007","S3001","S3002","S6001","S6002"]

print(len(course_codes))

import re
import os
import json
from copy import copy
unit_code = re.compile(r"[A-Z]{3}[0-9]{4}")

year_delta = re.compile(r"year [0-9]+", re.IGNORECASE)
semester_delta = re.compile(r"semester [0-9]+", re.IGNORECASE)
sem_delta = re.compile(r"sem [0-9]+", re.IGNORECASE)

number_regex = re.compile(r"[0-9+]")

from bs4 import BeautifulSoup

if not os.path.exists("output"):
    os.makedirs("output")

for course_code in course_codes:
    c = open("courses/" + course_code + ".html", "r")
    course_soup = BeautifulSoup(c.read(), "lxml")
    c.close()

    course_info_box = course_soup.findAll("div", class_="course-info-box")[0]

    course_info = {}

    for p in course_info_box.findAll("p"):
        if(p.get("class")[0] == "pub_highlight_heading"):
            course_key = p.getText(" ")
        elif(p.get("class")[0] == "pub_highlight_value"):
            if(course_key in course_info):
                course_info[course_key] += p.getText(" ")
            else:
                course_info[course_key] = p.getText(" ")

    f = open("raw/" + course_code, "r")
    soup = BeautifulSoup(f.read().replace("\n", " ").replace("\t", " ").replace("\r", " "), "lxml")
    f.close()

    headerCourse = soup.findAll("div", class_="page-header-courses")
    courseName = ""
    courseType = ""
    script = ""
    if headerCourse:
        try:
            script = soup.find("body").find("script").getText(" ")
            script = script[script.find("push") + 1:]
            script = script[script.find("push") + 5:]
            script = script[:len(script) - script[::-1].find("}")]
            # script = json.loads(script) # not a valid JSON object as it has an international boolean value
        except:
            print("Couldn't obtain script")
        try:
            courseName = headerCourse[0].find("h1").getText(" ")
            courseType = headerCourse[0].find("p").getText(" ")
        except:
            print("Couldn't obtain some of the header text")

    print(course_code)

    first_year = -1

    for i, table in enumerate(soup.findAll('table', {"class": "course-page__course-structure"})):
        file_name = course_code + "-" + str(i) + ".json"
        with open("output/" + file_name, "w") as json_file:
            print("Writing:", file_name)

            courseAOS = table

            while(dict(courseAOS.attrs).get("class") != ["scroll-wrapper"]):
                courseAOS = courseAOS.parent

            output_dict = {"courseCode": course_code, "courseName": courseName, "courseType": courseType, "teachingPeriods": [], "faculty": "Faculty of " + course_info["Managing faculty"], "courseAOS": courseAOS.find("h2").getText(" ")}

            rows = table.findAll('tr')
            for row in rows:
                header = row.find('th')
                course_map = {}

                if header is not None:
                    header_text = header.getText(" ")
                    year_strings = year_delta.findall(header_text)
                    semester_strings = semester_delta.findall(header_text)
                    if not semester_strings:
                        semester_strings = sem_delta.findall(header_text)

                    if year_strings:
                        year_int = int(number_regex.findall(year_strings[0])[0])

                        if first_year == -1:
                            first_year = year_int

                        # Just for Eric
                        course_map["year"] = year_int - first_year

                    if semester_strings and int(number_regex.findall(semester_strings[0])[0]) in (1, 2):
                        course_map["code"] = (None, "S1-01", "S2-01")[int(number_regex.findall(semester_strings[0])[0])]

                    if not (year_strings or semester_strings):
                        print("Couldn't get teaching period info")
                        course_map["teachingPeriod"] = header_text

                cells = row.findAll('td')

                units = []

                for cell in cells:
                    unit_string = " ".join(cell.getText(" ").replace("\r", "").replace("\n", "").strip(" ").split())

                    if(not unit_string):
                        continue

                    unit_codes = unit_code.findall(unit_string)

                    if(len(unit_codes) == 1):
                        units.append(unit_codes[0])
                    else:
                        current_units = unit_string.split(" or ")

                        if len(current_units) == 1:
                            if unit_string.lower() == "elective":
                                units.append("Elective")
                            else:
                                units.append({
                                    "type": unit_string,
                                    "faculty": ""
                                })
                        else:
                            output_current_units = []
                            for current_unit in current_units:
                                unit_codes = unit_code.findall(current_unit)

                                if(len(unit_codes) == 1):
                                    output_current_units.append(unit_codes[0])
                                else:
                                    break
                            if len(current_units) == len(output_current_units):
                                print("multiple units detected")
                                units.append(output_current_units)
                            else:
                                units.append({
                                    "type": unit_string,
                                    "faculty": ""
                                })

                if(not units):
                    continue

                course_map["units"] = units
                output_dict["teachingPeriods"].append(course_map)

            json_file.write(json.dumps(output_dict, indent=4, sort_keys=True))
    # print(tree.xpath('//*[@class="course-page__course-structure"]//text()'))
