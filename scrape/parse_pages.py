import csv, glob, os, pickle, re, pprint

from bs4 import BeautifulSoup


def parse_page(index, county):
    # create the dict that data will be stuffed into
    company_dict = {}
    root_dir = os.getcwd()
    filename = county.lower() + '_' + str(index)
    file_path = os.path.join('pages', county.lower(), filename)
    company_dict['Filename'] = filename

    pickle_file = open(file_path, 'rb')
    page = pickle.load(pickle_file)
    pickle_file.close()

    # make the soup
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

    company_dict['Company'] = soup.select('.largefont.strongtext')[0].get_text()

    # Get contact info, etc.
    keys = ['Phone', 'Website', 'Physical Address', 'Mailing Address', 'Employees on Site', 'Business Description']

    for key in keys:
        try:
            title = soup.find(text=key + ':')
            parent = title.find_parent('td')
            item = parent.find_next_sibling('td')
            company_dict[key] = item.get_text().strip().replace(u'\xa0', ',')
        except:
            company_dict[key] = ''

    # Clean up crazy whitespace in employees on site field
    company_dict['Employees on Site'] = re.sub(r'\s+', '', company_dict['Employees on Site'])
    company_dict['Phone'] = re.sub(r'\s+', '', company_dict['Phone'])

    address = list(company_dict['Mailing Address'].split(','))
    address1 = address[:-3]
    company_dict['Address1'] = ', '.join(address1)
    company_dict['Address2'] = '{0},{1} {2}'.format(address[-3], address[-2], address[-1])
    
    # Get the executive info
    executive_info = soup.select('.executivebox')
    executive_blocks = executive_info[0].select('a.vcardcontact')

    for index in range(5):
        try:
            name = executive_blocks[index].find_parent('td').find_next_sibling('td')
            title = name.find_next_sibling('td')
            company_dict['Name' + str(index + 1)] = name.get_text()
            company_dict['Title' + str(index + 1)] = title.get_text()
        except:
            company_dict['Name' + str(index + 1)] = ''
            company_dict['Title' + str(index + 1)] = ''
    print('----------------------------------------------')
    pprint.pprint(company_dict)

    return company_dict

def create_csv(county):
    number_of_companies = len(glob.glob('pages/' + county.lower() + '/*'))
    
    csv_file_path = os.path.join('csv_files', (county.lower() + '.csv'))

    with open(csv_file_path , 'w') as csvfile:
        fieldnames = ['Company', 'Business Description', 'Website', 'Employees on Site', \
        'Phone', 'Address1', 'Address2', 'Name1', 'Title1', 'Name2', 'Title2', 'Name3', \
        'Title3', 'Name4', 'Title4', 'Name5', 'Title5', 'Physical Address',\
        'Mailing Address', 'Filename']
        writer = csv.DictWriter(csvfile, dialect='excel', fieldnames=fieldnames)
        writer.writeheader()
        
        for index in range(number_of_companies):
            company_dict = parse_page(index, county)
            writer.writerow(company_dict)


if __name__ == '__main__':
    county = input('Input county (i.e. Delaware) ==> ')
    create_csv(county)
    

