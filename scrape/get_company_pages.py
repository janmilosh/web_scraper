import os, pickle

import requests

import secrets.secrets as secrets


class CompanyPages:
    """Using requests, logs in to the website and gets the detailed company pages
    using links that were read from a pickle file. These pages are written to
    files inside a directory named for the county."""
    def __init__(self, county):
        self.county = county.lower()
        self.root_dir = os.getcwd()
        self.company_links = []

    def get_pages(self):
        """The main method that calls the other methods and loops through the list
        of companies with the result of company detail pages being written to files."""
        self.company_links = self._read_list_of_pickled_company_links_from_file()   

        with requests.Session() as session:
            self._login_to_site(session)                
            for index, link in enumerate(self.company_links):                
                page = self._get_company_detail_page_for_company_link(session, index)
                self._write_page_to_file(page, index)
    
    def _read_list_of_pickled_company_links_from_file(self):
        """Reads the company links (list) from the pickle file for the county 
        and returns the list of links."""
        pickle_file_path = os.path.join(self.root_dir, 'pickle_files', self.county)
        pickle_file = open(pickle_file_path, 'rb')
        links = pickle.load(pickle_file)
        pickle_file.close()
        return links

    def _login_to_site(self, session):
        """Uses the requests session to login to the site."""
        url = secrets.SITE_URL + '/login/'
        session.get(url)
        login_data = dict(Username=secrets.USERNAME, Password=secrets.PASSWORD, urlforward='/main', Login='Login')
        session.post(url, data=login_data, headers={'Referer': secrets.SITE_URL})

    def _get_company_detail_page_for_company_link(self, session, index):
        """Uses the requests session to get the company detail page."""
        return session.get(secrets.SITE_URL + self.company_links[index])

    def _write_page_to_file(self, page, index):
        """Writes the company detail page to a pickle file."""
        file_path = os.path.join(self.root_dir, 'pages', self.county)
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        company_page_file = os.path.join(file_path, (self.county + '_' + str(index)))
        pickle_file = open(company_page_file, 'wb')
        pickle.dump(page, pickle_file)
        pickle_file.close()
        print('Saved file: ', company_page_file)  


if __name__ == '__main__':
    county = input('Input county (i.e. Delaware) ==> ')
    pages = CompanyPages(county)
    pages.get_pages()
