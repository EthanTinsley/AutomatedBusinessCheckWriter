# AutomatedBusinessCheckWriter
The Automated Business Check Writer is an application developed in Python, to read business check information from various file types (.csv, .xml, .json) and 
outputting a business check that is formatted to meet MICR E-13B banking specifications. Business checks formatted and printed using the python-docx library using "find and replace" methodology and can be returned as either a .docx file or .pdf file.

## Utilized Tools & Libraries 
    Python 3.9.5
    ---------------
    python-docx     
    python-num2words
    python-docx2pdf
    python-json
    python-csv
    python-os
    xml.etree.ElementTree
    ---------------
    Tkinter 
    ---------------
    SQLite3 
    MySQL
    
## Database Support 
A DatabaseHelper class is offered for both MySQL and SQLite3 depending on personel needs

## Check Object 
To read checks into system a Check object must be created which utilizes the parameters check date, check number, invoice number, invoice date, payee, account & amount

To format .csv file correctly columns should be arragned as follows(check date, check number, invoice number, invoice date, payee, account, amount)     

To format a .json file correctly JSON Check object should include following attribures: (check_date, check_num, invoice_num, invoice_date, payee, account_code , amount)

To format a .xml file correctly embed following attributes within "Check" tags (check_date, check_num, invoice_num, invoice_date, payee, account_code , amount) where each attribute listed like: <check_num name="check_num">123</check_num> -- because "name = " identifies parameter in the code


