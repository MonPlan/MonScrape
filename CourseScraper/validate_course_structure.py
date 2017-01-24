import json

if __name__ == "__main__":
    teachingPeriodTypesFile = open("all_teaching_periods.json", "r")
    teachingPeriodCodes = [teachingPeriodType["code"] for teachingPeriodType in json.loads(teachingPeriodTypesFile.read())]
    teachingPeriodTypesFile.close()

    file_name = input("Enter file name: ").rstrip("\n")
    json_file = open(file_name, "r")
    json_object = json.loads(json_file.read())
    json_file.close()

    # Basic course details
    assert("courseCode" in json_object)
    assert(isinstance(json_object["courseCode"], str))

    assert("courseName" in json_object)
    assert(isinstance(json_object["courseName"], str))

    assert("courseType" in json_object)
    assert(isinstance(json_object["courseType"], str))

    assert("faculty" in json_object)
    assert(isinstance(json_object["faculty"], str))

    assert("teachingPeriods" in json_object)
    assert(isinstance(json_object["teachingPeriods"], list))

    for teachingPeriod in json_object["teachingPeriods"]:
        assert("code" in teachingPeriod)
        assert(isinstance(teachingPeriod["code"], str))
        assert(teachingPeriod["code"] in teachingPeriodCodes)

        assert("units" in teachingPeriod)
        assert(isinstance(teachingPeriod["units"], list))

        for unit in teachingPeriod["units"]:
            pass
        
        assert("year" in teachingPeriod)
        assert(isinstance(teachingPeriod["year"], int))

    print("All tests passed!")
