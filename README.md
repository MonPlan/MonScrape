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



# License
This is licensed under the MIT License.
