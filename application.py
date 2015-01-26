import time

import scrape.get_company_links as get_company_links
import scrape.get_company_pages as get_company_pages
import scrape.parse_pages as parse_pages

def main():
    counties = ['Delaware', 'Morrow', 'Marion']

    for county in counties:
        company_links = get_company_links.CompanyLinks(county)
        company_links.get_links()
        company_pages = get_company_pages.CompanyPages(county)
        company_pages.get_pages()
        parse_pages.create_csv(county)
        time.sleep(10)

if __name__ == '__main__':
    main()