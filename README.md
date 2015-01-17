# Web Scraping and parsing scripts

## This set of three modules for scraping some data and parsing into csv files

### Running the modules separately:

Note: Please run from a virtual environment installed dependencies listed in ```requirements.txt```.

To get the links for the companies in a given county (written into the ```link_files``` directory):

```
python -m scrape.get_company_links
```

To process links into a web page for each link (corresponding to a company and written into the ```pages``` directory):

```
python -m scrape.get_company_pages
```

To parse the web pages for a given county into a csv file containing the scraped data (written into the ```csv_files``` directory):

To run the whole thing in one shot (for a list of Ohio counties):

Put your counties of interest in the list, ```counties```, in ```application.py```, then run all of the scripts for the list:

```
python -m application
```