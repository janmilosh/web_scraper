import csv, glob, os, pickle, re, pprint

from bs4 import BeautifulSoup


class CompanyCSV:
    def __init__(self, county):
        self.county = county.lower()
        self.company_dict = {}
        self.root_dir = os.getcwd()
        self.fieldnames = ['Company', 'Business Description', 'Website', 'Employees on Site', \
            'Phone', 'Address1', 'Address2', 'Name1', 'Title1', 'Name2', 'Title2', 'Name3', \
            'Title3', 'Name4', 'Title4', 'Name5', 'Title5', 'Physical Address',\
            'Mailing Address', 'Filename']

    def _configure(self):
        self.number_of_companies = len(glob.glob('pages/' + self.county + '/*'))
        self.csv_file_path = os.path.join('csv_files', (self.county + '.csv'))
        
    def create_csv(self):
        """Writes parsed pages to a csv file."""
        self._configure()

        with open(self.csv_file_path , 'w') as csvfile:            
            writer = csv.DictWriter(csvfile, dialect='excel', fieldnames=self.fieldnames)
            writer.writeheader()
            
            for index in range(self.number_of_companies):
                self.company_dict = self._parse_page(index)
                writer.writerow(self.company_dict)

    def _parse_page(self, index):
        """"""
        file_path = self._set_file_parameters(index)
        page = self._get_page_from_pickle_file(file_path)

        # make the soup from the page text
        soup = BeautifulSoup(page.text)
        print(soup.prettify())

        # get rid of spacers, images, and scripts, and break tags in the html
        spacers = soup.select('.producttabletd2') \
                + soup.select('.contactinfotabletd2') \
                + soup.select('.executivetabletdspace') \
                + soup.select('.companyinfotabletd2') \
                + soup.select('.microfont') \
                + soup.select('img') \
                + soup.select('script')

        for spacer in spacers:
            spacer.decompose() # gets rid of those items

        break_tags = soup.select('br')
        for break_tag in break_tags:
            break_tag.replace_with(',')

        self.company_dict['Company'] = soup.select('.largefont.strongtext')[0].get_text()

        # Get contact info, etc.
        keys = ['Phone', 'Website', 'Physical Address', 'Mailing Address', 'Employees on Site', 'Business Description']

        for key in keys:
            try:
                title = soup.find(text=key + ':')
                parent = title.find_parent('td')
                item = parent.find_next_sibling('td')
                self.company_dict[key] = item.get_text().strip().replace(u'\xa0', ',')
            except:
                self.company_dict[key] = ''

        # Clean up crazy whitespace in employees on site field
        self.company_dict['Employees on Site'] = re.sub(r'\s+', '', self.company_dict['Employees on Site'])
        self.company_dict['Phone'] = re.sub(r'\s+', '', self.company_dict['Phone'])

        address = list(self.company_dict['Mailing Address'].split(','))
        address1 = address[:-3]
        self.company_dict['Address1'] = ', '.join(address1)
        self.company_dict['Address2'] = '{0},{1} {2}'.format(address[-3], address[-2], address[-1])
        
        # Get the executive info
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

        return self.company_dict

    def _set_file_parameters(self, index):
        """Sets the filename on the dict for the given page, which will appear on that
        line in the csv file for the county. Returns the file_path."""
        filename = self.county + '_' + str(index)
        file_path = os.path.join('pages', self.county, filename)
        self.company_dict['Filename'] = filename
        return file_path

    def _get_page_from_pickle_file(self, file_path):
        """Opens the pickled page file for a given file path and returns the page object."""
        pickle_file = open(file_path, 'rb')
        page = pickle.load(pickle_file)
        pickle_file.close()
        return page


if __name__ == '__main__':
    county = input('Input county (i.e. Delaware) ==> ')
    company_csv = CompanyCSV(county)
    company_csv.create_csv()
