import os, pickle, time

from selenium import webdriver

import secrets.secrets as secrets

    
class CompanyLinks:
    def __init__(self, county):
        self.county = county.title()        
        self.driver = webdriver.Firefox()
        self.company_links = []
        self.root_dir = os.getcwd()

    def _configure(self):
        width = 1280
        height = 800
        time_in_seconds = 10
        self.driver.set_window_size(width, height)
        self.driver.implicitly_wait(time_in_seconds)
    
    def get_links(self):
        self._configure()
        self._login_to_website()
        self._input_county_to_search_on_list_page()
        self._navigate_to_list_of_companies_page()
        self._scrape_links_from_paginated_list_of_companies()
        self.driver.close()

        self._write_links_to_human_readable_file()
        self._write_links_to_pickle_file()
        print('There are {0} companies in {1} county.'.format(len(self.company_links), self.county))

    def _login_to_website(self):
        self.driver.get(secrets.SITE_URL + '/login/')
        username = self.driver.find_element_by_name("Username")
        username.send_keys(secrets.USERNAME)
        password = self.driver.find_element_by_name("Password")
        password.send_keys(secrets.PASSWORD)
        login = self.driver.find_element_by_name("Login")
        login.click()

    def _input_county_to_search_on_list_page(self):    
        self.driver.get(secrets.SITE_URL + '/list/')

        previous_counties_to_remove = self.driver.find_elements_by_class_name('listed')
        for county in previous_counties_to_remove:
            county.click()

        county_input_field = self.driver.find_element_by_id('countysearch')
        county_input_field.send_keys(self.county)
        county_and_state = self.county + ' County, OH'
        county_to_search = self.driver.find_element_by_link_text(county_and_state)
        county_to_search.click()

    def _navigate_to_list_of_companies_page(self):
        list_of_companies_count_button = self.driver.find_element_by_id('listcounttab')
        list_of_companies_count_button.click()

    def _scrape_links_from_paginated_list_of_companies(self):
        self._scrape_links_from_single_page()
        try:
            pagination = self.driver.find_element_by_class_name('pagination')
            spans = pagination.find_elements_by_tag_name('span')
            last_index = len(spans)-2
            for i in range(2, last_index):
                pagination = self.driver.find_element_by_class_name('pagination')
                spans = pagination.find_elements_by_tag_name('span')
                spans[i].click()
                time.sleep(2)
                self._scrape_links_from_single_page()
        except:
            pass

    def _scrape_links_from_single_page(self):
        companies = self.driver.find_elements_by_class_name('listresultstabletdcompany')
        
        for i in range(1, len(companies)):
            link = companies[i].find_element_by_tag_name('a')
            raw_href = link.get_attribute('href')
            left_stripped_href = raw_href.lstrip("javascript:EZOpen('")
            clean_href = left_stripped_href.rstrip("');")
            self.company_links.append(clean_href)

    def _write_links_to_human_readable_file(self):    
        links_file_path = os.path.join(self.root_dir, 'link_files', (self.county.lower() + '.txt'))
        links_file = open(links_file_path, 'w')
        for link in self.company_links:
            links_file.write("%s\n" % link)
        links_file.close()

    def _write_links_to_pickle_file(self):    
        pickle_file_path = os.path.join(self.root_dir, 'pickle_files', (self.county.lower()))
        pickle_file = open(pickle_file_path, 'wb')
        pickle.dump(self.company_links, pickle_file)
        pickle_file.close()


if __name__ == '__main__':
    county = input('Input county (i.e. Delaware) ==> ')
    links = CompanyLinks(county)
    links.get_links()