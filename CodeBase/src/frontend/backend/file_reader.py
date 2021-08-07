import csv 
import os
import json
import xml.etree.ElementTree as ET
from .check import Check

# this file holds the FileReader object to be used in the Check-Writer program 
# the FileReader object contains a series of methods to determine the type
# of file being read and then the appropriate methods for reading each of the file
# types as denoted by their file extensions (.csv, .xml, etc.) 
# to use the FileReader object simply create an instance of it by declaring it with
# the name of the file you would like to read. If more than one file is to be read 
# refer to the set_file_name() method to change the file contained within the obejct

class FileReader:

    def __init__(self, file_path=None):
        self.file_path = file_path
        self.file_type = self.get_file_type()


    # method to determine the type of file being read 
    # returns the type of file extension IE (.csv, .xml, .json)
    def get_file_type(self):
        file_path = self.file_path
        csv_extension = '.csv'
        json_extension = '.json'
        xml_extension = '.xml'

        if (file_path.endswith(csv_extension) or file_path.endswith(csv_extension.upper())):
            return csv_extension

        elif (file_path.endswith(json_extension) or file_path.endswith(json_extension.upper())):
            return json_extension

        elif (file_path.endswith(xml_extension) or file_path.endswith(xml_extension.upper())):
            return xml_extension

        else:
            return None


    # method for reading a file 
    # based off of file type calls the appropriate file reader type
    # returns check_book to the user who called 
    def read_file(self):
        file_type = self.file_type
        csv_extension = '.csv'
        json_extension = '.json'
        xml_extension = '.xml'
        check_book = []

        if file_type == csv_extension:
            check_book = self.read_csv()

        elif file_type == json_extension:
            check_book = self.read_json()

        elif file_type == xml_extension:
            check_book = self.read_xml()       


        return check_book 


    # method for reading csv typed files 
    # uses a csv file reader object to determine the delimiter
    # and extract the check information from the file 
    # then with the check information extracted stores it in a Check() object
    # stores each Check object in a list and returns the list after the file is parsed
    def read_csv(self):
        file_path = self.file_path
        check_book = []

        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                # test to see if input parameters are legal
                if self.csv_reader_exception_test(row) == False:
                    check = Check(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
                    check_book.insert(line_count, check)
                    line_count += 1
                else:
                    continue

        return check_book

    # method for reading in data from a .json file extension 
    # uses the json library import 
    # checks for check objects contained within the file and returns a list[] of extracted check objects
    def read_json(self):
        file_path = self.file_path
        check_book = []

        with open(file_path) as json_file:
            json_data = json.load(json_file)
            
            for c in json_data['Check']:
                check = Check(c['check_date'], c['check_num'], c['invoice_num'], c['invoice_date'], c['payee'], c['account_code'], c['amount'])
                check_book.append(check)
            

        return check_book


    # mthod for reading in data from a .xml file
    # utilizes Element tree import
    def read_xml(self):
        file_path = self.file_path
        tree = ET.parse(file_path)
        root = tree.getroot()
        checkbook = []
        

        for checklist in root:
            for check in checklist:
                # intialzie check var
                check_date = None
                check_num = None
                invoice_date = None
                invoice_num = None
                payee = None
                amount = None
                account = None

                for elem in check:
                    if elem.attrib.get('name') == 'invoice_num':
                        invoice_num = elem.text
                    elif elem.attrib.get('name') == 'invoice_date':
                        invoice_date = elem.text   
                    elif elem.attrib.get('name') == 'check_date':
                        check_date = elem.text    
                    elif elem.attrib.get('name') == 'check_num':
                        check_num = elem.text      
                    elif elem.attrib.get('name') == 'payee':
                        payee = elem.text 
                    elif elem.attrib.get('name') == 'amount':
                        amount = elem.text 
                    elif elem.attrib.get('name') == 'account':
                        account = elem.text
                
                # create check and store in checkbook
                check = Check(check_date, check_num, invoice_num, invoice_date, payee, account, amount)
                checkbook.append(check)

        return checkbook



    # method for detecting invalid data in a csv_row
    # checks csv data entry for column headers and skips row if data header is found
    def csv_reader_exception_test(self, csv_row):
        row = csv_row
        exception_list = ['Check Date', 'Check #', 'Check Num', 'Check Number', 'Invoice #', 'Invoice Num', 'Invoice Number',
            'invoice date' , 'INVOICE DATE', 'Invoice Date', 'Payee', 'PAYEE', 'payee', 'Account',' ACCOUNT', 'account',
             'Amount', 'AMOUNT', 'amount']

        for item in row:
            if (item in exception_list):
                return True
            elif (item == ""):
                return True
            
        return False            