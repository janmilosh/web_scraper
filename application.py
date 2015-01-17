import time

import scrape.get_company_links as links
import scrape.get_company_pages as pages
import scrape.parse_pages as parse

def main():
    counties = ['Delaware', 'Morrow', 'Marion']

    for county in counties:
        links.get_links(county)
        pages.get_pages(county)
        parse.create_csv(county)
        time.sleep(10)

if __name__ == '__main__':
    main()