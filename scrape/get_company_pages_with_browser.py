import os, pickle, time, pdb

from selenium import webdriver

import secrets.secrets as secrets

class CompanyPagesBrowser:
    """Use browser to log into the website and get the detailed
    company pages using links that were read from a pickle file.
    These pages are written to files inside a directory named
    for the county.
    """

    def __init__(self, county):
        self.county = county.title()
        self.driver = webdriver.Chrome()
        self.company_links = []
        self.root_dir = os.getcwd()

    def _configure(self):
        """Set the browser size and the amount of time we'll wait
        for things to happen.
        """
        width = 1280
        height = 800
        time_in_seconds = 10
        self.driver.set_window_size(width, height)
        self.driver.implicitly_wait(time_in_seconds)

    def get_pages(self):
        """The main method that calls the other methods and loops
        through the list of companies with the result of company detail
        pages being written to files.
        """
        self.company_links = self._read_list_of_pickled_company_links_from_file()
        self._configure()
        self._login_to_website()

        for index, link in enumerate(self.company_links):
            page = self._get_company_detail_page_for_company_link(index)
            self._write_page_to_file(page, index)
        self.driver.close()

    def _login_to_website(self):
        """Use webdriver to log in to the site from the login page."""
        self.driver.get(secrets.SITE_URL + '/login/')
        email = self.driver.find_element_by_name("Email")
        email.send_keys(secrets.EMAIL)
        password = self.driver.find_element_by_name("Password")
        password.send_keys(secrets.PASSWORD)
        login = self.driver.find_element_by_name("Login")
        login.click()

    def _read_list_of_pickled_company_links_from_file(self):
        """Read the company links (list) from the pickle file
        for the county and return the list of links.
        """
        pickle_file_path = os.path.join(self.root_dir, 'pickle_files', self.county)
        pickle_file = open(pickle_file_path, 'rb')
        links = pickle.load(pickle_file)
        pickle_file.close()
        return links

    def _get_company_detail_page_for_company_link(self, index):
        """Use the requests session to get the company detail page."""
        self.driver.get(secrets.SITE_URL + self.company_links[index])
        page = self.driver.find_element_by_class_name('companyshell').get_attribute('innerHTML')
        return page

    def _write_page_to_file(self, page, index):
        """Write the company detail page to a pickle file."""
        file_path = os.path.join(self.root_dir, 'pages', self.county)
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        company_page_file = os.path.join(file_path, (self.county + '_' + str(index)))
        pickle_file = open(company_page_file, 'wb')
        pickle.dump(page, pickle_file)
        pickle_file.close()
        # print('Saved file: ', company_page_file)


if __name__ == '__main__':
    county = input('Input county (i.e. Delaware) ==> ')
    pages = CompanyPagesBrowser(county)
    pages.get_pages()
