# monScrape
monScrape is a web scraper for units at Monash University. It is used to scrape large quantities (over 5000 records of unit data) to turn it into a CSV database

**Built with Python**

# Instructions
This will setup your runtime environment
```
sudo install python3
sudo apt-get install python-setuptools build-essential
sudo easy_install pip
sudo pip install lxml
```

To use simply run
```
python converter.py
```
The file `main.py` is used for developing purposes

# Description
This Python webscraper bascially scrapes through targetted classes, such as Prohibitions, Preqs, Name, Description of Unit, etc.

_This may or may not be abandoned as we will be talking with eSolutions_


# monCScraper
Transformation scripts and raw data for scraping course data to be used for monPlan web app.

## Sources
- `courses` holds raw html data downloaded from Monash's 2017 Handbook. 
- `raw` holds raw html data downloaded from study.monash website.

In monPlan-API's repository, we also used the course map PDF files from the handbook to manually type the course maps into JSON files. By the looks of it, the course map PDF files is more detailed than the course maps from study.monash.

## Process
1. `python3 obtain_json.py` uses raw 2017 HTML data from both the handbook and study.monash. The course maps from study.monash are HTML tables which are converted into JSON files. Since there may be multiple course maps for each course, a numerical suffix is added to the end. Currently the Monash handbook is only being used to obtain the managing faculty string.

2. `python3 main.py` transforms the JSON files so that they can be imported into monPlan web app. It fetches unit data from `api.monplan.tech` so that the client app doesn't have to.

## Validation
Before running `main.py`, a script `validate_course_structure.py` is used to check if a JSON file is valid.


# License
This is licensed under the MIT License.
