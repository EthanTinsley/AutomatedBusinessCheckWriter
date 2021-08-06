import tkinter as tk 
from .backend.database_helper import DataBaseHelper
from .backend.account import Account
from .backend.company import Company
from .backend.signature import Signature
from .backend.bank import Bank

# frame to be dsiplayed within mainframe 
# gives user an interface to add, update, and remove account information 
# inherits constructor from tkinter frame object 
class AccountManagementFrame(tk.Frame):

    # class constructor 
    def __init__(self, master=None):
        super().__init__(master=master, bg='gray80', highlightthickness=1, highlightbackground='black')
        # bg = background color , highlightthickness applies a border, highlightbackground sets the borders color
        
        # delcare master object usually mainframe 
        self.master = master

        # fill lists with stored objects to be used in optionox widgets
        self.storedbanks = self.get_banks()
        self.storedcomps = self.get_companies()
        self.storedsignees = self.get_signees()

        # place the widgets on the navigation panel
        self.create_widgets()
        self.grid_widgets()

        # place accounts in listbox
        self.get_accounts()

        # make the wiget expand to fill the frame accordingly
        self.columnconfigure(0, weight=1)



    # method used to create frame widgets 
    def create_widgets(self):
        # some recurring data used within the method 
        btn_width=20
        bg_color = 'gray80'
        lbl_font = ('arial', 16)

        # create the lbls used within the frame 
        # lbl for section header 
        self.lbl_accountheader = tk.Label(master=self, text='Accounts', bg=bg_color, font=lbl_font )

        # lbl for adding an account
        self.lbl_addaccountheader = tk.Label(master=self, text='Add an Account',bg=bg_color, font=lbl_font )

        # account code lbl
        self.lbl_accountcode = tk.Label(master=self,text='Account Code: ', bg=bg_color, font=lbl_font )

        # account number lbl
        self.lbl_accountnum = tk.Label(master=self, text='Account Number: ', bg=bg_color, font=lbl_font )

        # account routing number 
        self.lbl_routingnum = tk.Label(master=self, text='Routing Number: ', bg=bg_color, font=lbl_font )

        # account signee 
        self.lbl_accountsignee = tk.Label(master=self, text='Account Signee: ', bg=bg_color, font=lbl_font )

        # account company 
        self.lbl_company = tk.Label(master=self, text='Account Company: ', bg=bg_color, font=lbl_font )

        # account bank
        self.lbl_bank = tk.Label(master=self, text='Account Bank: ', bg=bg_color, font=lbl_font )

        # entry widgets used within the forms
        # entry for account code 
        self.ent_accountcode = tk.Entry(master=self)

        # entry for account number 
        self.ent_accountnum = tk.Entry(master=self)

        # entry for routing number 
        self.ent_routingnum = tk.Entry(master=self)

        # options menu for the form
        # option memu to select a signee
        self.selectedsignee_stringvar = tk.StringVar(master=self)
        self.opt_singee = tk.OptionMenu(self, self.selectedsignee_stringvar, *self.storedsignees)

        # option menu to select a company for the account
        self.selectedcompany_stringvar = tk.StringVar(master=self)
        self.opt_company = tk.OptionMenu(self, self.selectedcompany_stringvar, *self.storedcomps)

        # optionmenu to select a bank
        self.selectedbank_stringvar = tk.StringVar(master=self)
        self.opt_bank = tk.OptionMenu(self, self.selectedbank_stringvar, *self.storedbanks)

        # list box used within the frame 
        # existing accounts listbox
        self.list_accounts = tk.Listbox(master=self, bg='white', height=20)

        # buttons used within the frame
        # add account button
        self.btn_addaccount = tk.Button(master=self,width=btn_width, text='Add Selected Account', command=self.click_btn_addaccount)
    
        # remove account button 
        self.btn_removeaccount = tk.Button(master=self, width=btn_width, text='Remove Selected Account', command=self.click_btn_removeaccount)

        # view account button 
        self.btn_viewaccount = tk.Button(master=self, width=btn_width, text='View Selected Account', command=self.click_btn_viewaccount)

        # update account button
        self.btn_updateaccount = tk.Button(master=self, width=btn_width, text='Update Selected Account', command=self.click_btn_updateaccount)

    
    # method for adding the widgets to the frame accordingly 
    def grid_widgets(self):
        # add the widgets to the frame 
        # add the accounts header
        self.lbl_accountheader.grid(row=0, column=0, sticky='nsew')

        # add the add account header 
        self.lbl_addaccountheader.grid(row=0, column=1, columnspan=2, sticky='nsew')

        # add the accounts listbox
        self.list_accounts.grid(row=1, column=0, padx=30, pady=5, rowspan=6, columnspan=1, sticky='nsew')

        # add the add account code label and entry box
        self.lbl_accountcode.grid(row=1,column=1, padx=20, sticky='e')
        self.ent_accountcode.grid(row=1,column=2,padx=20, sticky='w')

        # add the account number label and entry box
        self.lbl_accountnum.grid(row=2,column=1, padx=20, sticky='e')
        self.ent_accountnum.grid(row=2,column=2, padx=20, sticky='w')

        # add the account routing number label and rentry bo
        self.lbl_routingnum.grid(row=3,column=1, padx=20, sticky='e')
        self.ent_routingnum.grid(row=3,column=2, padx=20, sticky='w')

        # add the signature optionsbox and label
        self.lbl_accountsignee.grid(row=4,column=1, padx=20, sticky='e')
        self.opt_singee.grid(row=4, column=2, padx=20,sticky='ew')

        # add the company label and optionsbox
        self.lbl_company.grid(row=5, column=1, padx=20, sticky='e')
        self.opt_company.grid(row=5, column=2, padx=20, sticky='ew')

        # add the bank label and optionsbox
        self.lbl_bank.grid(row=6, column=1, padx=20, sticky='e')
        self.opt_bank.grid(row=6, column=2,padx=20,sticky='ew')

        # add the addbank button to the form
        self.btn_addaccount.grid(row=7, column=1,padx=20, pady=10, sticky='ns', columnspan=2)

        # add the remove bank button to the form
        self.btn_removeaccount.grid(row=7, column=0, padx=20, pady=10, sticky='ns')

        # add the view bank button to the fomr
        self.btn_viewaccount.grid(row=8, column=0, padx=20, pady=10, sticky='ns')

        # add the uppdate bank button to the fomr
        #self.btn_updateaccount.grid(row=9, column=0, padx=20, pady=10, sticky='ns')


    # method for retrieving all stored signees 
    def get_signees(self):
        # create db connection
        db = DataBaseHelper()

        # create and fill list of all signatures stored with the db
        storedsignatures = db.get_all_signatures()

        # if not uploaded signature notify user
        if storedsignatures == []:
            storedsignatures.append('No Uploaded Signature Present')
            

        return storedsignatures


    # method for retrieving all stored companies
    def get_companies(self):
        # create database connection
        db = DataBaseHelper()

        # create and fill list with stored comapnies
        storedcomps = db.get_all_companies()

        # if no uploaded company notify user
        if storedcomps == []:
            storedcomps.append('No Uploaded Companies Present')

        return storedcomps

    
    # method for retreving all stored banks
    def get_banks(self):
        # create database connection
        db = DataBaseHelper()

        # create and fill list with stored banks
        storedbanks = db.get_all_banks()

        # if no uploaded banks notify user
        if storedbanks == []:
            storedbanks.append('No Uploaded Banks Present')

        return storedbanks


    # method for getting the accounts form the db and putting them in the ListBox
    def get_accounts(self):
        # get database connection
        db = DataBaseHelper()

        # get the list of banks
        self.accounts = db.get_all_accounts()

        # insure the ListBox is empty 
        self.list_accounts.delete(0,'end')

        # fill ListBox with returned Banks
        for acct in self.accounts:
            self.list_accounts.insert('end', acct)
    

    # method called when add account button called 
    def click_btn_addaccount(self):
        # get the account code 
        code = self.ent_accountcode.get()

        # get the account number
        acctnum = self.ent_accountnum.get()

        # get the routing number
        routnum = self.ent_routingnum.get()

        # get the account signature 
        signature = self.get_selectedsignature()

        # get the account company 
        company = self.get_selectedcompany()

        # get the account bank
        bank = self.get_selectedbank()

        # ensure that user selected each of the ddl items
        if isinstance(signature, Signature)==False | isinstance(company, Company)==False | isinstance(bank, Bank)==False:
            return 

        account = Account(code, acctnum, routnum, company, bank, signature)

        msg = tk.messagebox.askyesno(title='Upload Account?', message =account.msg_alert(), parent=self )

        if msg == True:
            db = DataBaseHelper()

            db.upload_account(account, account.company, account.bank, account.signature)

            self.get_accounts()
        else:
            pass


    # method called when remove account button is called
    def click_btn_removeaccount(self):
        # get index of selected item
        index = self.list_accounts.curselection()
        index = int(index[0]) # convert to int

        # find the selected bank object from the list
        account = self.accounts[index]

        msg = tk.messagebox.askokcancel(title='Are You Sure You Want to Remove This Account?', message=account.msg_alert(), parent=self)

        # if user selects ok then remove account from db
        if msg == True:
            # establish db helper object (db connection)
            db = DataBaseHelper()

            # remove account from list
            db.remove_account(account.account_id)

            # update ListBox
            self.get_accounts()
        else:
            pass


    # method called when view account button is called 
    def click_btn_viewaccount(self):
        # get index of selected item
        index = self.list_accounts.curselection()
        index = int(index[0]) # convert to int

        # find the selected bank object from the list
        account = self.accounts[index]

        # display selected bank using .msg_alert() method
        tk.messagebox.showinfo(title=account.account_code, message=account.msg_alert())



    # method called when update account button is called 
    def click_btn_updateaccount(self):
        pass


    # method for getting the currently selected signature
    # signatures in ddl are stored in tk.StringVar so we need to search 
    # the appropriate stored signatures to find a signature name match
    def get_selectedsignature(self):

        # find a match between stored signatuers and signature selected in ddl
        for sig in self.storedsignees:
            if self.selectedsignee_stringvar.get() == sig.name:
                return sig
        
        # if no mathc found return null to handle exception
        return None


    # method for getting the currently selected company
    # companies in ddl are stored in tk.StringVar so we need to search 
    # the appropriate stored companies to find a signature name match    
    def get_selectedcompany(self):

        # find a match between stored companise and company from ddl
        for comp in self.storedcomps:
            if self.selectedcompany_stringvar.get() == comp.name:
                return comp

        # if no match found return null to handle exception
        return None

    
    # method for getting the currently selected bank
    # banks in ddl are stored in tk.StringVar so we need to search 
    # the appropriate stored banks to find a signature name match    
    def get_selectedbank(self):

        # find a match between stored bank and bank from ddl
        for bank in self.storedbanks:
            if self.selectedbank_stringvar.get() == bank.name:
                return bank
                
        # if no match found return null to handle exception
        return None