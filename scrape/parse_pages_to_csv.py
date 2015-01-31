import csv, glob, os, pickle, re, pprint

from bs4 import BeautifulSoup


class CompanyCSV:
    def __init__(self, county):
        county = county.lower()
        self.county = county
        self.company_dict = {}
        self.fieldnames = ['Company', 'Business Description', 'Website', 'Employees on Site',
            'Phone', 'Address1', 'Address2', 'Name1', 'Title1', 'Name2', 'Title2', 'Name3',
            'Title3', 'Name4', 'Title4', 'Name5', 'Title5', 'Physical Address',
            'Mailing Address', 'Filename']
        self.number_of_companies = len(glob.glob('pages/' + county + '/*'))
        self.csv_file_path = os.path.join('csv_files', (county + '.csv'))
        self.page_directory_path = os.path.join('pages', county)   
       
    def create_csv(self):
        """Writes parsed pages to a csv file."""
        with open(self.csv_file_path , 'w') as csvfile:            
            writer = csv.DictWriter(csvfile, dialect='excel', fieldnames=self.fieldnames)
            writer.writeheader()
            
            for index in range(self.number_of_companies):
                self._parse_page(index)
                writer.writerow(self.company_dict)

    def _parse_page(self, index):
        """Call methods that do the page parsing tasks."""
        file_path = self._set_file_parameters(index)
        page = self._get_page_from_pickle_file(file_path)

        soup = BeautifulSoup(page.text)
        print(soup.prettify())

        self._clean_up_html(soup)
        self._get_contact_info_from_soup(soup)
        self._clean_up_crazy_whitespace_in_employees_on_site_field()
        self._get_address_from_soup(soup)
        self._get_executive_info_from_soup(soup)

    def _clean_up_html(self, soup):
        """Get rid of spacer elements and break tags.
        Mutates the soup object."""
        spacer_selectors = ['.producttabletd2', '.contactinfotabletd2', '.executivetabletdspace',
                            '.companyinfotabletd2', '.microfont', 'img', 'script']
        spacers = []
        for selector in spacer_selectors:
            spacers += soup.select(selector)

        for spacer in spacers:
            spacer.decompose() # gets rid of those items

        break_tags = soup.select('br')
        for break_tag in break_tags:
            break_tag.replace_with(',')

    def _get_contact_info_from_soup(self, soup):
        self.company_dict['Company'] = soup.select('.largefont.strongtext')[0].get_text()
        keys = ['Phone', 'Website', 'Physical Address', 'Mailing Address', 
                'Employees on Site', 'Business Description']

        for key in keys:
            try:
                title = soup.find(text=key + ':')
                parent = title.find_parent('td')
                item = parent.find_next_sibling('td')
                self.company_dict[key] = item.get_text().strip().replace(u'\xa0', ',')
            except:
                self.company_dict[key] = ''

    def _set_file_parameters(self, index):
        """Set the filename on the dict for the given page,
        which will appear on that line in the csv file for the county.
        Return the file_path."""
        filename = self.county + '_' + str(index)
        file_path = os.path.join(self.page_directory_path, filename)
        print('The file path', file_path)
        self.company_dict['Filename'] = filename
        return file_path

    def _get_page_from_pickle_file(self, file_path):
        """Open the pickled page file for a given file path
        and return the page object."""
        pickle_file = open(file_path, 'rb')
        page = pickle.load(pickle_file)
        pickle_file.close()
        return page

    def _clean_up_crazy_whitespace_in_employees_on_site_field(self):
        self.company_dict['Employees on Site'] = re.sub(r'\s+', '', 
                                                 self.company_dict['Employees on Site'])
        self.company_dict['Phone'] = re.sub(r'\s+', '', self.company_dict['Phone'])

    def _get_address_from_soup(self, soup):
        address = list(self.company_dict['Mailing Address'].split(','))
        address1 = address[:-3]
        self.company_dict['Address1'] = ', '.join(address1)
        self.company_dict['Address2'] = '{0},{1} {2}'.format(address[-3], address[-2], address[-1])

    def _get_executive_info_from_soup(self, soup):    
        executive_info = soup.select('.executivebox')
        executive_blocks = executive_info[0].select('a.vcardcontact')

        for index in range(5):
            try:
                name = executive_blocks[index].find_parent('td').find_next_sibling('td')
                title = name.find_next_sibling('td')
                self.company_dict['Name' + str(index + 1)] = name.get_text()
                self.company_dict['Title' + str(index + 1)] = title.get_text()
            except:
                self.company_dict['Name' + str(index + 1)] = ''
                self.company_dict['Title' + str(index + 1)] = ''
        print('----------------------------------------------')
        pprint.pprint(self.company_dict)


if __name__ == '__main__':
    county = input('Input county (i.e. Delaware) ==> ')
    company_csv = CompanyCSV(county)
    company_csv.create_csv()
