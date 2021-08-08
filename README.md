# Web Scraping and Parsing Scripts

## This is a set of three modules for scraping data from a website and parsing into csv files

### Setup:

Run from a virtual environment (Python 3.9) with installed dependencies listed in ```requirements.txt```.

[Instructions for installing using pip and virtual environments.](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Install virtual environment: ```python3 -m pip install --user virtualenv```

Create virtual environment in project: ```python3 -m venv env```

Activate virtual environment: ```source env/bin/activate```

To deactivate virtual environment: ```deactivate```

Install required dependencies in virtual environment: ```pip install -r requirements.txt```

You will need chromedriver installed and an up-to-date version of the Chrome browser.

Install chromedriver with Homebrew: ```brew install chromedriver```

Make your Mac trust chromedriver: ```xattr -d com.apple.quarantine /usr/local/bin/chromedriver```

Add the website url and credentials to the secrets module.

### Running the modules separately:

To get the links for the companies in a given county (written to the ```link_files``` directory):

```
python -m scrape.get_company_links
```

To process links into a web page for each link (corresponding to a company and written to the ```pages``` directory):

```
python -m scrape.get_company_pages
```

To parse the web pages for a given county into a csv file containing the scraped data (written to the ```csv_files``` directory):

```
python -m scrape.parse_pages_to_csv
```

### To run the whole thing in one shot (for a list of Ohio counties):

Put your counties of interest in the list, ```counties```, in ```application.py```, then run all of the scripts for the list:

```
python application.py
```
