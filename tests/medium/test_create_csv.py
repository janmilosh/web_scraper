import csv, glob, os, pickle, re, pprint, unittest

from bs4 import BeautifulSoup

from scrape.parse_pages_to_csv import CompanyCSV


class CompanyCSVTest(unittest.TestCase):
    def setUp(self):
        self.class_instance = CompanyCSV('Morrow')
        self.class_instance.number_of_companies = 3
        self.class_instance.csv_file_path = os.path.join('tests', 'output_files', 'csv_files', 'morrow.csv')
        self.class_instance.page_directory_path = os.path.join('tests', 'data', 'pages', 'morrow')
        
    def test_create_csv_from_page_file(self):       
        self.class_instance.create_csv()
        self.assertEqual(1, 1)

    def tearDown(self):
        os.remove(self.class_instance.csv_file_path)


if __name__ == '__main__':
    unittest.main()