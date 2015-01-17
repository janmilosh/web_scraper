import os
import requests
import pickle

import secrets.secrets as secrets

def get_pages(county):
    root_dir = os.getcwd()
    pickle_file_path = os.path.join(root_dir, 'pickle_files', county.lower())
    pickle_file = open(pickle_file_path, 'rb')
    company_links = pickle.load(pickle_file)
    pickle_file.close()

    with requests.Session() as s:
        url = secrets.SITE_URL + '/login/'
        s.get(url)
        login_data = dict(Username=secrets.USERNAME, Password=secrets.PASSWORD, urlforward='/main', Login='Login')
        s.post(url, data=login_data, headers={'Referer': secrets.SITE_URL})
            
        for index, link in enumerate(company_links):
            page = s.get(secrets.SITE_URL + company_links[index])
            file_path = os.path.join(root_dir, 'pages', county.lower())
            if not os.path.exists(file_path):
                os.mkdir(file_path)

            company_page_file = os.path.join(file_path, (county.lower() + '_' + str(index)))
            pickle_file = open(company_page_file, 'wb')
            pickle.dump(page, pickle_file)
            pickle_file.close()
            print('Saved file: ', company_page_file)

if __name__ == '__main__':
    county = input('Input county (i.e. Delaware) ==> ')
    get_pages(county)
