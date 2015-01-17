import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pickle

import secrets.secrets as secrets

def get_links(county):
    full_county = '{0} County, OH'.format(county.title())
    company_links = []

    driver = webdriver.Firefox()
    driver.implicitly_wait(10) # seconds
    driver.set_window_size(1280, 800)

    #log in to the website
    driver.get(secrets.SITE_URL + '/login/')

    elem = driver.find_element_by_name("Username")
    elem.send_keys(secrets.USERNAME)
    elem = driver.find_element_by_name("Password")
    elem.send_keys(secrets.PASSWORD)
    elem = driver.find_element_by_name("Login")
    elem.click()

    #on dashboard page now, input the county to search
    driver.get(secrets.SITE_URL + '/list/')

    #clear out any old selections
    elems = driver.find_elements_by_class_name('listed')
    for elem in elems:
        elem.click()

    #input the new county to search
    elem = driver.find_element_by_id('countysearch')
    elem.send_keys(county.title())
    elem = driver.find_element_by_link_text(full_county)
    elem.click()

    #navigate to the list of companies
    elem = driver.find_element_by_id('listcounttab')
    elem.click()

    def go_to_company_detail_pages():
        elems = driver.find_elements_by_class_name('listresultstabletdcompany')
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
        elem = driver.find_element_by_class_name('pagination')
        spans = elem.find_elements_by_tag_name('span')
        last_index = len(spans)-2
        for i in range(2, last_index):
            elem = driver.find_element_by_class_name('pagination')
            spans = elem.find_elements_by_tag_name('span')
            spans[i].click()
            time.sleep(2)
            go_to_company_detail_pages()
    except:
        pass

    driver.close()

    root_dir = os.getcwd()
    links_file_path = os.path.join(root_dir, 'link_files', (county.lower() + '.txt'))
    links_file = open(links_file_path, 'w')
    for link in company_links:
        links_file.write("%s\n" % link)
    links_file.close()

    pickle_file_path = os.path.join(root_dir, 'pickle_files', (county.lower()))
    pickle_file = open(pickle_file_path, 'wb')
    pickle.dump(company_links, pickle_file)
    pickle_file.close()

    print('There are {0} companies in {1} county.'.format(len(company_links), county.title()))

if __name__ == '__main__':
    county = input('Input county (i.e. Delaware) ==> ')
    get_links(county)