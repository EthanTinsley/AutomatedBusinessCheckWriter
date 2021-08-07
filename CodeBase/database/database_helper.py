import sqlite3
from .check import *
from .account import *
from .company import *
from .bank import *
from datetime import datetime
from .signature import Signature
import mysql.connector

# class is used to handle the database interactions that occur within the system.
# the DataBaseHelper object can be called without any input variables. It will create an
# instance of the object that can establish a connection to the server, upload checks, and other
# information, and recall those items when they are needed during the printing phase in 
# class CheckWriter

class DataBaseHelper:

    # object creation method 
    # this method creates an instance of the DataBaseHelper class and when it is created it 
    # calls the on_create() method in order to create the database if it dosent already exist 
    # and if it does it allows the user to pass and retrive information from the database 
    def __init__(self):
        # get datbase file location
        self.path = "./frontend/backend/database/CheckWriter.db"
        # create the database
        self.on_create()


    # SQLITE3 
    # get_connection() method establishes a connection to the database and 
    # returns ths connection to be used to interact with database 
    def get_connection(self):
        conn = sqlite3.connect(self.path)
        return conn


    # on_create() method creates the database whenever it is called 
    # if the database already contains the desired tables then this method will 
    # not alter any of the data within the database 
    def on_create(self):
        conn = self.get_connection()
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS Company(
            company_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            company_name VARCHAR(255) NOT NULL ,
            address VARCHAR(255) ,
            city VARCHAR(255) ,
            state VARCHAR(255) ,
            zip VARCHAR(255) 
            ); """)

        conn.commit()

        c.execute("""CREATE TABLE IF NOT EXISTS Bank (
            bank_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            bank_name VARCHAR(255) NOT NULL,
            address VARCHAR(255) ,
            city VARCHAR(255) ,
            state VARCHAR(255) ,
            zip VARCHAR(255) 
            ); """)

        c.execute("""CREATE TABLE IF NOT EXISTS Signature(
            signature_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            signature_name VARCHAR(255) NOT NULL,
            signature_imgpath VARCHAR(255) NOT NULL
            ); """)


        c.execute("""CREATE TABLE IF NOT EXISTS Account(
            account_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            account_code VARCHAR(255) NOT NULL UNIQUE,
            account_num VARCHAR(255) NOT NULL,
            routing_num VARCHAR(255) NOT NULL ,
            company_id INTEGER NOT NULL,
            bank_id INTEGER NOT NULL ,
            signature_id INTEGER NOT NULL,
            FOREIGN KEY (company_id) REFERENCES Company(company_id),
            FOREIGN KEY (bank_id) REFERENCES Bank (bank_id),
            FOREIGN KEY (signature_id) REFERENCES Signature (signature_id)
            ); """)

        c.execute("""CREATE TABLE IF NOT EXISTS CheckTemplate(
            check_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            printed BOOLEAN ,
            upload_date DATE NOT NULL,
            check_num VARCHAR(255) NOT NULL,
            check_date DATE NOT NULL,
            invoice_num VARCHAR(255) NOT NULL,
            invoice_date DATE NOT NULL,
            payee VARCHAR(255) NOT NULL,
            amount FLOAT NOT NULL,
            account_code VARCHAR(255) NOT NULL,
            FOREIGN KEY (account_code) REFERENCES Account (account_code)); """)

        conn.commit()
        conn.close()

    
    # upload_company() method allows the program to store company information within the database 
    # uses a dictonary in order to pass the company information to the database to preserve data integrity 
    def upload_company(self, company):
        conn = self.get_connection()
        c = conn.cursor()
        company = company

        c.execute("INSERT INTO Company VALUES( :company_id , :company_name, :address, :city , :state , :zip )",
            {'company_id': None ,'company_name': company.name ,'address': company.address ,'city': company.city ,'state': company.state ,'zip': company.zip})

        conn.commit() # commit SQL statements
        conn.close() # close database connection
    


    def get_company_id(self, company):
        company_name = company.name

        conn = self.get_connection()
        c = conn.cursor()

        c.execute("SELECT company_id FROM Company WHERE company_name = :name " , {'name': company_name})

        conn.commit() # commit SQL statements

        company_id = c.fetchone() # returns a tuple of (n,)
        company_id = company_id[0] # sets company_id as n within the tuple 

        conn.close() # close database connection

        return company_id

        
    # method for gathering a company and it's information based off of a account code 
    # used when printing checks
    # check object has account code which passes that infomration to this method to get the 
    # corresponding comapny that goes with the check
    # returns a Company() object
    def get_company(self, account_code):
        code = account_code 
        conn = self.get_connection()
        c = conn.cursor()
        company = None

        # pass SQL query to the database in order to return the appropriate informaiton 
        c.execute("""SELECT company_name, address, city, state, zip FROM Company WHERE company_id IN
                    (SELECT company_id FROM Account WHERE account_code = :account_code);""", 
                    {'account_code': code})

        conn.commit() # execute the query

        # iterate through the results and build and Bank() object
        for comp in c.fetchall():
            company = Company(comp[0], comp[1], comp[2], comp[3], comp[4])
        
        conn.close()

        return company

    
    # database query to return all companies stored within db 
    def get_all_companies(self):
        conn = self.get_connection()
        c = conn.cursor()

        # database query 
        c.execute('SELECT company_name, address, city, state, zip, company_id FROM Company ORDER BY company_id')

        # commit query 
        conn.commit()

        complist = []
        # convert results into comapny objects and store within a list
        for comp in c.fetchall():
            company = Company(comp[0], comp[1], comp[2], comp[3], comp[4], comp[5])
            complist.append(company)

        conn.close() # close db connection

        return complist


    # database query for removing a company 
    # uses companies company_id to drop from table 
    def remove_company(self, id):
        conn = self.get_connection()
        c = conn.cursor()

        # sql statement
        c.execute("""DELETE FROM Company WHERE company_id = :id""" , {'id': id})

        # commit statement
        conn.commit()

        #close connection
        conn.close()

    
    # uplaods a bank object to the db
    # autoincrements the bank_id
    def upload_bank(self, Bank):
        bank = Bank
        id = None
        conn = self.get_connection()
        c = conn.cursor()

        c.execute("INSERT INTO Bank VALUES(:bank_id, :bank_name, :address, :city , :state , :zip )" , 
        {'bank_id': id, 'bank_name': bank.name, 'address':bank.address, 'city': bank.city , 'state': bank.state, 'zip': bank.zip})

        conn.commit() # commit SQL statements
        conn.close() # close database connection


    # method for returning the bank_id of a bank object
    def get_bank_id(self, bank):
        bank_name = bank.name

        conn = self.get_connection()
        c = conn.cursor()

        c.execute("SELECT bank_id FROM Bank WHERE bank_name = :name " , {'name': bank_name})

        conn.commit() # commit SQL statements

        bank_id = c.fetchone()# returns a tuple of (n,)
        bank_id = bank_id[0]  # sets the bank_id equal to n within the tuple 

        conn.close() # close database connection

        return bank_id

    
    # method for gathering a bank and it's information based off of a account code 
    # used when printing checks
    # check object has account code which passes that infomration to this method to get the 
    # corresponding bank that goes with the check
    # returns a Bank() object
    def get_bank(self, account_code):
        code = account_code 
        conn = self.get_connection()
        c = conn.cursor()
        bank = None

        # pass SQL query to the database in order to return the appropriate informaiton 
        c.execute("""SELECT bank_name, address, city, state, zip FROM Bank WHERE bank_id IN
                    (SELECT bank_id FROM Account WHERE account_code = :account_code)""", 
                    {'account_code': code})

        conn.commit() # execute the query

        # iterate through the results and build and Bank() object
        for b in c.fetchall():
            bank = Bank(b[0], b[1], b[2] , b[3], b[4])
        
        conn.close()

        return bank


    # method used to return all Banks within db 
    # returns list of Bank objects 
    def get_all_banks(self):
        conn = self.get_connection()
        c = conn.cursor()
        banklist = []

        # sql query statement
        c.execute('SELECT bank_name, address, city, state, zip, bank_id FROM Bank ORDER BY bank_id')

        # commit query 
        conn.commit()

        # get the results
        for b in c.fetchall():
            bank = Bank(b[0],b[1],b[2],b[3],b[4], b[5])
            banklist.append(bank)
        
        # close db connection
        conn.close()

        # return list 
        return banklist


    # method for removing a bank form the db using the bank's bank_id
    def remove_bank(self, bank_id):
        conn = self.get_connection()
        c = conn.cursor()

        # SQL delete query
        c.execute("""DELETE FROM Bank WHERE bank_id = :id""", {'id': bank_id})

        # commit query 
        conn.commit()

        # close connection
        conn.close()


    # uploads an account object to the db
    def upload_account(self, account, company, bank, signature):
        account = account
        company_id = company.company_id
        bank_id = bank.bank_id
        signature_id = signature.id


        conn = self.get_connection()
        c = conn.cursor()
        
        c.execute("INSERT INTO Account VALUES ( :account_id , :account_code , :account_num , :routing_num , :company_id , :bank_id, :signature_id );", 
            {'account_id': None , 'account_code': account.account_code , 'account_num': account.account_num
            ,'routing_num': account.routing_num, 'company_id': company_id , 'bank_id': bank_id, 'signature_id': signature_id})

        conn.commit() # commit SQL statements
        conn.close() # close database connection


    # method for gathering an account and it's information based off of a account code 
    # used when printing checks
    # check object has account code which passes that infomration to this method to get the 
    # corresponding account that goes with the check
    # returns an Account() object
    def get_account(self, account_code):
        code = account_code 
        conn = self.get_connection()
        c = conn.cursor()
        account = None

        # pass SQL query to the database in order to return the appropriate informaiton 
        c.execute("SELECT account_code, account_num, routing_num, account_id FROM Account WHERE account_code = :account_code",
         {'account_code': code })

        conn.commit() # execute the query

        # iterate through the results and build and Account() object
        for acc in c.fetchall():
            account = Account(acc[0], acc[1], acc[2], account_id=acc[3])
        
        conn.close()

        return account

    
    # method for returning all accounts 
    def get_all_accounts(self):
        conn = self.get_connection()
        c = conn.cursor()
        allaccounts = []

        # execute the SQL statemetn
        c.execute("""SELECT account_code, account_num, routing_num, account_id FROM Account ORDER BY account_code""")

        for acct in c.fetchall():
            account = Account(acct[0], acct[1],acct[2], account_id=acct[3])
            allaccounts.append(account)

        conn.close()

        return allaccounts


    # method for removing accounts from the db
    def remove_account(self, account_code):
        conn = self.get_connection()
        c = conn.cursor()

        c.execute("DELETE FROM Account WHERE account_code = :code", {'code': account_code})

        conn.commit()

        conn.close()


    # method for uploading a signute method to the db
    def upload_signature(self, signature):
        signature = signature
        conn = self.get_connection()
        c = conn.cursor()

        # query for inserting signature into db
        c.execute("INSERT INTO Signature VALUES( :id , :name, :path)", {'id': None, 'name': signature.name, 'path': signature.path})

        # commit insert statement 
        conn.commit()

        # close connection to db 
        conn.close()

    
    # method for retruning all signaututes stored within the db
    def get_all_signatures(self):
        conn = self.get_connection()
        c = conn.cursor()
        signaturelist = []

        # create appropriate db query
        c.execute("""SELECT signature_name, signature_imgpath, signature_id From Signature ORDER BY signature_id""")

        # commit sql call
        conn.commit()

        # get results
        for sig in c.fetchall():
            sign = Signature(sig[0], sig[1], signature_id=sig[2])
            signaturelist.append(sign)

        conn.close()

        return signaturelist

    
    # method for retrieving a signature object from a check account_code atrribute
    def get_signature(self, account_code):
        conn = self.get_connection()
        c = conn.cursor()
        code = account_code
        signature = None

        # execute query for retriving signature object 
        c.execute("SELECT signature_name, signature_imgpath, signature_id FROM Signature WHERE signature_id IN (SELECT signature_id FROM Account WHERE account_code = :code ) ;", 
        {'code': account_code})

        conn.commit()

        # get results and build signatue objects
        for signee in c.fetchall():
            signature = Signature(signee[0],signee[1], signee[2])

        conn.close()

        return signature

    

    # method for removing signature from the db
    def remove_signature(self, signature_id):
        conn = self.get_connection()
        c = conn.cursor()

        c.execute("""DELETE FROM Signature WHERE signature_id = :id ;""" , {'id': signature_id})

        conn.commit()

        conn.close()


    # method for uploading a check into the db
    def upload_check(self, Check, printed=False):
        check_id = None
        check = Check
        printed = printed
        upload_time = datetime.now()

        conn = self.get_connection() 
        c = conn.cursor()

        c.execute("INSERT INTO CheckTemplate VALUES( :check_id, :printed, :upload_date, :check_num, :check_date, :invoice_num, :invoice_date, :payee, :amount, :account_code )" ,
            { 'check_id': check_id, 'printed': printed, 'upload_date': upload_time, 'check_num': check.check_num, 'check_date': check.check_date,
            'invoice_num':check.invoice_num , 'invoice_date': check.invoice_date , 'payee': check.payee , 'amount': check.amount , 'account_code': check.account_code })

        conn.commit() # commit SQL statements
        conn.close() # close database connection

        
    # method to retrieve and print all unprinted checks 
    # can be called with the DatabaseHelper class object
    # does not require any input information
    def get_unprinted_checks(self):
        checklist = [] # holds the uprinted checks
        conn = self.get_connection() # connection to the database 
        c = conn.cursor() # cursor used ot pass and retrieve information from queries 
        
        # call method to return all the unprinted checks whihch only contain a single invoice 
        checklist = self.get_unprinted_single_charge_checks(conn, c, checklist) 

        # call a method to return all the unprinted checks which habe multiple charges belonging 
        # to a single check number 
        checklist = self.get_unprinted_multi_charge_checks(conn, c, checklist)

        conn.close() # close datbase conenction 

        return checklist


    # method to get all the checks that have yet to be printed 
    # inludes a filter to prevent gathering checks that have duplicates/ multiple charges 
    def get_unprinted_single_charge_checks(self, database_connection, cursor, check_list):
        # localize variables
        conn = database_connection
        c = cursor
        checklist = check_list

        # execute query to return all unprinted checks whihch only have a single charge 
        c.execute("SELECT check_date, check_num, invoice_num, invoice_date, payee, account_code, amount FROM CheckTemplate WHERE printed = 0 AND check_num NOT IN(SELECT check_num FROM CheckTemplate GROUP BY check_num HAVING COUNT(*) > 1) ORDER BY check_num;")

        conn.commit() # execute query 

        for x in c.fetchall():
            # build Check object
            check = Check(x[0], x[1], x[2], x[3], x[4] , x[5] , x[6])

            checklist.append(check) # add the check object to the check_list

        return checklist


    # TODO  optimize method
    # method to get checks that have multiple invoices but are being printed to one check
    # input parameters pass a list of checks that have already been gathered 
    # runs a query to get the check numbers of checks that havent been printed and have multiple charges 
    # runs a query to get the checks that have multiple charges
    # using those two queries creates lists of checks to add to the list of checks 
    # yes returns [ check , [check, check]]
    def get_unprinted_multi_charge_checks(self, database_connection, cursor, check_list):
        # localize variables 
        conn = database_connection
        c = cursor
        checklist = check_list
        dup_check_num = []

        # execute query to retrieve all the check numbers of the checks whihc have multiple charges
        c.execute("SELECT check_num FROM CheckTemplate GROUP BY check_num HAVING COUNT(*) > 1;")

        conn.commit() # execute query

        # iterate through the list and store the duplicate check numbers in the dup_check_list list
        for duplicate in c.fetchall():
            dup_check_num.append(duplicate[0])

        # determine if the list is empty IE no duplicate values 
        # if so then return the checklist now and break out of the method 
        if dup_check_num: # not empty then continue the method
            pass
        else: # if duplicate list is empty then break out of method
            return checklist
        
        # if method continues then the duplicate check number list is not empty so retrieve the duplicate checks via query 
        c.execute("SELECT check_date, check_num, invoice_num, invoice_date, payee, account_code, amount FROM CheckTemplate WHERE printed = 0 AND check_num IN(SELECT check_num FROM CheckTemplate GROUP BY check_num HAVING COUNT(*) > 1) ORDER BY check_num;")

        conn.commit() # execute the query

        # iterate through the numbers in the dup_check_list 
        # for each check in the return statement test to see if the check_num matches the number in the dup_check_list
        # if a match is found then store in a list and store this list in the checklist (yes a list inside a list)
        for duplicate in dup_check_num:
            duplicate_checks = []

            for x in c.fetchall():
                check = Check(x[0], x[1], x[2], x[3], x[4] , x[5] , x[6])

                if check.check_num == duplicate:
                    duplicate_checks.append(check)
            
            if duplicate_checks: # check to see if list is not empty add the list to the check list if
                 checklist.append(duplicate_checks)
            else: # if empty then don't add to list 
                continue

        return checklist


    # method for getting all checks from the db
    def get_all_checks(self, sort_parameter):
        checklist = []
        conn = self.get_connection()
        c = conn.cursor()
        para = sort_parameter

        # create query outside execute() to make sure that ORDER BY works correctly
        query = """SELECT check_date, check_num, invoice_num, invoice_date, payee, account_code, amount,
            check_id, printed, upload_date FROM CheckTemplate ORDER BY """  + sort_parameter + """;"""

        # execute sql query
        c.execute(query)

        # commit sql query
        conn.commit()

        # get the results and store in list of check
        for item in c.fetchall():
            check = Check(item[0], item[1], item[2], item[3], item[4], item[5], item[6],check_id=item[7], printed=item[8],upload_date=item[9])
            print(check.printed)
            checklist.append(check)
        
        conn.close()

        return checklist


    # method for removing a check form the db 
    def remove_check(self,check_id):
        conn = self.get_connection()
        c = conn.cursor()
        check_id = check_id
        
        c.execute("DELETE FROM CheckTemplate WHERE check_id = :id", {'id': check_id})

        conn.commit()

        conn.close()

    
    # method for testing to see if a check is already in db or not
    def duplicate_check_test(self, check):
        conn = self.get_connection()
        c = conn.cursor()

        # sql query 
        c.execute("SELECT COUNT(*) FROM CheckTemplate WHERE check_num = :num AND amount = :amount ;", {'num': check.check_num, 'amount': check.amount})

        conn.commit()

        count = c.fetchone()
        count = int(count[0])

        # determine if check exists 
        if count != int(0) :
            conn.close()
            return True
        else:
            conn.close()
            return False 


        # Method for updating a checks printed status
    def update_check_printed(self, check, printed=True):
        conn = self.get_connection()
        c = conn.cursor()

            # execute update query
        c.execute("UPDATE CheckTemplate SET printed = :print WHERE check_num = :num ;", {'print':printed , 'num': check.check_num})

        conn.commit()

        conn.close()

            