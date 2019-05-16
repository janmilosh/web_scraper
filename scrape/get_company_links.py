import os, pickle, time, pdb

from selenium import webdriver

import secrets.secrets as secrets


class CompanyLinks:
    """Use selenium webdriver to go to a website and find a list of
    manufacturing company links for a specified county in Ohio
    and write them to to a human readable file and a pickle file.
    """

    def __init__(self, county):
        self.county = county.title()
        self.driver = webdriver.Chrome()
        self.company_links = []
        self.root_dir = os.getcwd()
        self.company_count = 0

    def _configure(self):
        """Set the browser size and the amount of time we'll wait
        for things to happen.
        """
        width = 1280
        height = 800
        time_in_seconds = 10
        self.driver.set_window_size(width, height)
        self.driver.implicitly_wait(time_in_seconds)

    def get_links(self):
        """The main method. Get the manufacturing company links and
        write results to text and pickle files.
        """
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
        """Use webdriver to log in to the site from the login page."""
        self.driver.get(secrets.SITE_URL + '/login/')
        email = self.driver.find_element_by_name("Email")
        email.send_keys(secrets.EMAIL)
        password = self.driver.find_element_by_name("Password")
        password.send_keys(secrets.PASSWORD)
        login = self.driver.find_element_by_name("Login")
        login.click()

    def _input_county_to_search_on_list_page(self):
        """Use webdriver to input the county that is to be searched
        from the list page.
        """
        self.driver.get(secrets.SITE_URL + '/list/geography')

        previous_counties_to_remove = self.driver.find_elements_by_class_name('listed')
        for county in previous_counties_to_remove:
            county.click()

        county_input_field = self.driver.find_element_by_id('countysearch')
        county = self.county
        county_and_state = self.county + ' County, OH'
        county_input_field.send_keys(county)
        time.sleep(2)
        js_string = "e=$('.ui-menu-item-wrapper:contains({})'); e.click()".format(county_and_state)
        self.driver.execute_script(js_string)
        self.driver.execute_script(js_string) # need to do this twice because it clicks on the first element the first time

    def _navigate_to_list_of_companies_page(self):
        """Use webdriver to click the link that results in navigation
        to the list of companies page.
        """
        time.sleep(3)
        list_of_companies_count_button = self.driver.find_element_by_id('listcounttab')
        count_str = list_of_companies_count_button.text
        self.company_count = int(''.join(filter(str.isdigit, count_str)))
        print(self.company_count)
        list_of_companies_count_button.click()

    def _scrape_links_from_paginated_list_of_companies(self):
        """Call the method that scrapes the company links for each
        paginated list of companies while using webdriver to navigate
        through the pagination.
        """
        self._scrape_links_from_single_page()
        try:
            while len(self.company_links) < self.company_count:
                js_string = "e=$('span:contains(Next)'); e.click();"
                self.driver.execute_script(js_string)
                time.sleep(2)
                self._scrape_links_from_single_page()
        except:
            pass

    def _scrape_links_from_single_page(self):
        """Use webdriver to get the company links."""
        companies = self.driver.find_elements_by_class_name('listresultstabletdcompany')

        for i in range(1, len(companies)):
            link = companies[i].find_element_by_tag_name('a')
            clean_link = self._clean_up_link(link)
            self.company_links.append(clean_link)

    def _clean_up_link(self, link):
        """Remove everything but the path that we need
        from a string that contained a link.
        """
        raw_href = link.get_attribute('href')
        left_stripped_href = raw_href.lstrip("javascript:EZOpen('")
        clean_link = left_stripped_href.rstrip("');")
        return clean_link

    def _write_links_to_human_readable_file(self):
        """Write links to a text file, one link per line.
        These files are for reference only and aren't used
        by any of the modules."""
        links_file_path = os.path.join(self.root_dir, 'link_files', (self.county.lower() + '.txt'))
        links_file = open(links_file_path, 'w')
        for link in self.company_links:
            links_file.write("%s\n" % link)
        links_file.close()

    def _write_links_to_pickle_file(self):
        """Write the whole list of links to a pickle file."""
        pickle_file_path = os.path.join(self.root_dir, 'pickle_files', (self.county.lower()))
        pickle_file = open(pickle_file_path, 'wb')
        pickle.dump(self.company_links, pickle_file)
        pickle_file.close()


if __name__ == '__main__':
    county = input('Input county (i.e. Delaware) ==> ')
    links = CompanyLinks(county)
    links.get_links()
