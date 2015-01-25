import time

import scrape.get_company_links as get_company_links
import scrape.get_company_pages as pages
import scrape.parse_pages as parse

def main():
    counties = ['Delaware', 'Morrow', 'Marion']

    for county in counties:
        company_links = get_company_links.CompanyLinks(county)
        company_links.get_links()
        pages.get_pages(county)
        parse.create_csv(county)
        time.sleep(10)

if __name__ == '__main__':
    main()