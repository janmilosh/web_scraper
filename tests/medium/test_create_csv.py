import csv, glob, os, pickle, re, pprint, unittest

from bs4 import BeautifulSoup

from scrape.parse_pages_to_csv import CompanyCSV


class CompanyCSVTest(unittest.TestCase):
    def setUp(self):
        self.class_instance = CompanyCSV('Morrow')
        self.class_instance.number_of_companies = 4
        self.class_instance.csv_file_path = os.path.join('tests', 'output_files', 'csv_files', 'morrow.csv')
        self.class_instance.page_directory_path = os.path.join('tests', 'data', 'pages', 'morrow')
        self.class_instance_csv = self.class_instance.create_csv()
        self.class_instance_csv_as_list = self._read_csv_to_list(self.class_instance.csv_file_path)

        self.csv_standard_file_path = os.path.join('tests', 'data', 'csv_files', 'morrow.csv')
        self.csv_standard_as_list = self._read_csv_to_list(self.csv_standard_file_path)
        
    def _read_csv_to_list(self, file_path):
        with open(file_path, newline='') as f:
            reader = list(csv.reader(f))
            return reader

    def test_create_csv_from_page_file(self): 
        self.assertListEqual(self.class_instance_csv_as_list, self.csv_standard_as_list)      

    def tearDown(self):
        os.remove(self.class_instance.csv_file_path)


if __name__ == '__main__':
    unittest.main()