import csv, glob, os, pickle, re, pprint, unittest

from bs4 import BeautifulSoup

from scrape.parse_pages_to_csv import CompanyCSV


class CompanyCSVTest(unittest.TestCase):
    def setUp(self):
        self.class_instance = CompanyCSV('Morrow')
        self.county_lower = 'morrow'
        self.fieldnames = ['Company', 'Business Description', 'Website', 'Employees on Site',
            'Phone', 'Address1', 'Address2', 'Name1', 'Title1', 'Name2', 'Title2', 'Name3',
            'Title3', 'Name4', 'Title4', 'Name5', 'Title5', 'Physical Address',
            'Mailing Address', 'Filename']

    def test_instantiates_county_as_lower_case(self):
        self.assertEqual(self.class_instance.county, self.county_lower)

    def test_instantiates_fieldnames_list(self):
        self.assertListEqual(self.class_instance.fieldnames, self.fieldnames)


if __name__ == '__main__':
    unittest.main()