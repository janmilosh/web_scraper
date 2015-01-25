import os, pickle, time

from selenium import webdriver

import secrets.secrets as secrets

    
class CompanyLinks:
    def __init__(self, county):
        self.county = county.title()        
        self.driver = webdriver.Firefox() 

    def configure(self):
        width = 1280
        height = 800
        time_in_seconds = 10
        self.driver.set_window_size(width, height)
        self.driver.implicitly_wait(time_in_seconds)
    
    def get_links(self):
        self.configure()       

        full_county = '{0} County, OH'.format(self.county)
        company_links = []

        

        #log in to the website
        self.driver.get(secrets.SITE_URL + '/login/')

        elem = self.driver.find_element_by_name("Username")
        elem.send_keys(secrets.USERNAME)
        elem = self.driver.find_element_by_name("Password")
        elem.send_keys(secrets.PASSWORD)
        elem = self.driver.find_element_by_name("Login")
        elem.click()

        #on dashboard page now, input the county to search
        self.driver.get(secrets.SITE_URL + '/list/')

        #clear out any old selections
        elems = self.driver.find_elements_by_class_name('listed')
        for elem in elems:
            elem.click()

        #input the new county to search
        elem = self.driver.find_element_by_id('countysearch')
        elem.send_keys(self.county)
        elem = self.driver.find_element_by_link_text(full_county)
        elem.click()

        #navigate to the list of companies
        elem = self.driver.find_element_by_id('listcounttab')
        elem.click()

        def go_to_company_detail_pages():
            elems = self.driver.find_elements_by_class_name('listresultstabletdcompany')
            last_index = len(elems)
            for i in range(1, last_index):
                link = elems[i].find_element_by_tag_name('a')
                raw_href = link.get_attribute('href')
                left_stripped_href = raw_href.lstrip("javascript:EZOpen('")
                clean_href = left_stripped_href.rstrip("');")
                company_links.append(clean_href)

        #Do this for the initial list of companies
        go_to_company_detail_pages()

        # If there is pagination, loop through the rest of the pages
        try:
            elem = self.driver.find_element_by_class_name('pagination')
            spans = elem.find_elements_by_tag_name('span')
            last_index = len(spans)-2
            for i in range(2, last_index):
                elem = self.driver.find_element_by_class_name('pagination')
                spans = elem.find_elements_by_tag_name('span')
                spans[i].click()
                time.sleep(2)
                go_to_company_detail_pages()
        except:
            pass

        self.driver.close()

        root_dir = os.getcwd()
        links_file_path = os.path.join(root_dir, 'link_files', (self.county.lower() + '.txt'))
        links_file = open(links_file_path, 'w')
        for link in company_links:
            links_file.write("%s\n" % link)
        links_file.close()

        pickle_file_path = os.path.join(root_dir, 'pickle_files', (self.county.lower()))
        pickle_file = open(pickle_file_path, 'wb')
        pickle.dump(company_links, pickle_file)
        pickle_file.close()

        print('There are {0} companies in {1} county.'.format(len(company_links), self.county))

if __name__ == '__main__':
    county = input('Input county (i.e. Delaware) ==> ')
    links = CompanyLinks(county)
    links.get_links()