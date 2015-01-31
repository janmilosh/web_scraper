#!/usr/bin/env python
import time

import scrape.get_company_links as get_company_links
import scrape.get_company_pages as get_company_pages
import scrape.parse_pages_to_csv as parse_pages_to_csv

def main():
    counties = ['Monroe', 'Van Wert', 'Franklin']

    for county in counties:
        company_links = get_company_links.CompanyLinks(county)
        company_links.get_links()
        
        company_pages = get_company_pages.CompanyPages(county)
        company_pages.get_pages()

        company_csv = parse_pages_to_csv.CompanyCSV(county)
        company_csv.create_csv()

        time.sleep(10)

if __name__ == '__main__':
    main()