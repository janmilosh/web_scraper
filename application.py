#!/usr/bin/env python
import time

import scrape.get_company_links as get_company_links
import scrape.get_company_pages_with_browser as get_company_pages
import scrape.parse_pages_to_csv as parse_pages_to_csv

def main():
    counties = ['Adams', 'Allen', 'Ashland', 'Ashtabula', 'Athens', 'Auglaize', 'Belmont', 'Brown', 'Butler', 'Carroll', 'Champaign', 'Clark', 'Clermont', 'Clinton', 'Columbiana', 'Coshocton', 'Crawford', 'Cuyahoga', 'Darke', 'Defiance', 'Delaware', 'Erie', 'Fairfield', 'Fayette', 'Franklin', 'Fulton', 'Gallia', 'Geauga', 'Greene', 'Guernsey', 'Hamilton', 'Hancock', 'Hardin', 'Harrison', 'Henry', 'Highland', 'Hocking','Holmes', 'Huron', 'Jackson', 'Jefferson', 'Knox', 'Lake', 'Lawrence', 'Licking', 'Logan', 'Lorain', 'Lucas', 'Madison', 'Mahoning', 'Marion', 'Medina', 'Meigs', 'Mercer', 'Miami', 'Monroe', 'Montgomery', 'Morgan', 'Morrow', 'Muskingum', 'Noble', 'Ottawa', 'Paulding', 'Perry', 'Pickaway', 'Pike', 'Portage', 'Preble', 'Putnam', 'Richland', 'Ross', 'Sandusky', 'Scioto', 'Seneca', 'Shelby', 'Stark', 'Summit', 'Trumbull', 'Tuscarawas', 'Union', 'Van Wert', 'Vinton', 'Warren', 'Washington', 'Wayne', 'Williams', 'Wood', 'Wyandot']
    # counties = ['Paulding', 'Perry', 'Pickaway', 'Pike', 'Portage', 'Preble', 'Putnam', 'Richland', 'Ross', 'Sandusky', 'Scioto', 'Seneca', 'Shelby', 'Stark', 'Summit', 'Trumbull', 'Tuscarawas', 'Union', 'Van Wert', 'Vinton', 'Warren', 'Washington', 'Wayne', 'Williams', 'Wood', 'Wyandot']

    for county in counties:
        company_links = get_company_links.CompanyLinks(county)
        company_links.get_links()

        company_pages = get_company_pages.CompanyPagesBrowser(county)
        company_pages.get_pages()

        company_csv = parse_pages_to_csv.CompanyCSV(county)
        company_csv.create_csv()

        time.sleep(10)

if __name__ == '__main__':
    main()
