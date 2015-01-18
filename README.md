# Web Scraping and Parsing Scripts

## This is a set of three modules for scraping data from a website and parsing into csv files

### Running the modules separately:

Note: Run from a virtual environment with installed dependencies listed in ```requirements.txt```. Also, there is a secrets module not included here as these scripts can only be run by authorized users of the site that's being scraped.

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
python -m scrape.parse_pages
```

To run the whole thing in one shot (for a list of Ohio counties):

Put your counties of interest in the list, ```counties```, in ```application.py```, then run all of the scripts for the list:

```
python application.py
```