import tkinter as tk
from .backend.bank import Bank
from .backend.database_helper import DataBaseHelper

# class object used to display the bank management (upload, upadte and removal)
# calls inherits its constructor from tkinter tk.frame 
# displays contents on Frame and is called to be displayed within the mainframe class
class BankManagementFrame(tk.Frame):

    # class constructor
    def __init__(self, master=None):
        super().__init__(master=master, bg='gray80', highlightthickness=1, highlightbackground='black')
        # bg = background color , highlightthickness applies a border, highlightbackground sets the borders color
        
        # delcare master object usually mainframe 
        self.master = master

        # place the widgets on the navigation panel
        self.create_widgets()
        self.grid_widgets()

        # display the banks stored within the db
        self.get_banks()

        # make the wiget expand to fill the frame accordingly
        self.columnconfigure(0, weight=1)


    
    # method to create the widgets
    def create_widgets(self):
        # some recurring data used within the method 
        btn_width=20
        bg_color = 'gray80'
        lbl_font = ('arial', 16)

        # create the lbls used within the frame 
        # create the lbl that displays above the listbox 
        self.lbl_banknames = tk.Label(master=self, text='Exisiting Banks', bg=bg_color, font=lbl_font )

        # create the lbl for adding a bank 
        self.lbl_addbank = tk.Label(master=self, text='Add a Bank', bg=bg_color, font=lbl_font )
        
        # create hte lbl for entering in bank name
        self.lbl_addbankname = tk.Label(master=self, text='Bank Name:', bg=bg_color, font=lbl_font )

        # create the lbl for entering in bank address
        self.lbl_addbankaddress = tk.Label(master=self, text='Bank Address:', bg=bg_color, font=lbl_font )

        # create the lbl for entering in bank city
        self.lbl_addbankcity = tk.Label(master=self, text='Bank City:', bg=bg_color, font=lbl_font )

        # create the lbl for entering in bank state
        self.lbl_addbankstate = tk.Label(master=self, text='Bank State:', bg=bg_color, font=lbl_font )

        # create the lbl for entering in bank zip code
        self.lbl_addbankzip = tk.Label(master=self, text='Bank Zip Code:', bg=bg_color, font=lbl_font )

        # create entry forms used within the form 
        # create entry from for accepting bank name 
        self.ent_addbankname = tk.Entry(master=self)

        # create entry for entering in bank address
        self.ent_addbankaddress = tk.Entry(master=self)

        # create entry for entering in bank city
        self.ent_addbankcity = tk.Entry(master=self)

        # create entr for entering in bank state
        self.ent_addbankstate = tk.Entry(master=self)

        # create entry for entering in bank zip code
        self.ent_addbankzip = tk.Entry(master=self)

        # create buttons used within the form
        # create button for uploading company to the database
        self.btn_addbank = tk.Button(master=self, width=btn_width, text='Add Bank', command=self.click_btn_addbank)

        # create button for removing selected bank 
        self.btn_removebank = tk.Button(master=self, width=btn_width, text='Remove Selected Bank', command=self.click_btn_removebank)

        # create button for viewing the selected bank
        self.btn_viewbank = tk.Button(master=self, width=btn_width, text='View Selected Bank', command=self.click_btn_viewbank)

        # create button for updating seleected bank
        self.btn_updatebank = tk.Button(master=self, width=btn_width, text='Update Selected Bank', command=self.click_btn_updatebank)

        # create the listbox used within the frame 
        self.list_banks = tk.Listbox(master=self, bg='white', height=20)

    
    # method used to place the widgets on the frame 
    def grid_widgets(self):
        
        # add the bank names label to the frame
        self.lbl_banknames.grid(row=0,column=0, sticky= 'nsew')

        # add the add a bank prompt to the frame
        self.lbl_addbank.grid(row=0, column=1, columnspan= 2, sticky= 'nsew')
        
        # add the bank listbox to the frame
        self.list_banks.grid(row=1,column=0, padx=30, pady=5, rowspan=5, columnspan=1, sticky='nsew')

        # add the add bank name lbl and ent
        self.lbl_addbankname.grid(row=1, column=1,padx=20, sticky='e')
        self.ent_addbankname.grid(row=1, column=2,padx=20, sticky='w')

        # add the add bank address lbl and ent 
        self.lbl_addbankaddress.grid(row=2, column=1,padx=20, sticky='e')
        self.ent_addbankaddress.grid(row=2, column=2,padx=20, sticky='w')

        # add the add bank city lbl and ent
        self.lbl_addbankcity.grid(row=3, column=1,padx=20, sticky='e')
        self.ent_addbankcity.grid(row=3, column=2,padx=20, sticky='w')

        # add the add bank state lbl and ent 
        self.lbl_addbankstate.grid(row=4, column=1,padx=20, sticky='e')
        self.ent_addbankstate.grid(row=4, column=2,padx=20, sticky='w')

        # add the add bank zip lbl and ent
        self.lbl_addbankzip.grid(row=5, column=1,padx=20, sticky='e')
        self.ent_addbankzip.grid(row=5, column=2,padx=20, sticky='w')

        # add the addbank button to the form
        self.btn_addbank.grid(row=6, column=1,padx=20, pady=10, sticky='ns', columnspan=2)

        # add the remove bank button to the form
        self.btn_removebank.grid(row=6, column=0, padx=20, pady=10, sticky='ns')

        # add the view bank button to the fomr
        self.btn_viewbank.grid(row=7, column=0, padx=20, pady=10, sticky='ns')

        # add the uppdate bank button to the fomr
        #self.btn_updatebank.grid(row=8, column=0, padx=20, pady=10, sticky='ns')

    

    
    # method used for gathering all banks from database
    # stores the reurned bank objects in the ListBox
    def get_banks(self):
        # get database connection
        db = DataBaseHelper()

        # get the list of banks
        self.banks = db.get_all_banks()

        # insure the ListBox is empty 
        self.list_banks.delete(0,'end')

        # fill ListBox with returned Banks
        for bank in self.banks:
            self.list_banks.insert('end', bank)



    # method called when user clicks add banks button
    # parses text boxes and displays an alert message for user to confrim that the information 
    # is as they want it 
    # when they click yes create a Bank object and upload it into the datbase
    def click_btn_addbank(self):
        # parse entry forms to create Bank() object
        name = self.ent_addbankname.get()
        address = self.ent_addbankaddress.get()
        city = self.ent_addbankcity.get()
        state = self.ent_addbankstate.get()
        zip_code = self.ent_addbankzip.get()
        # create a bank object
        bank = Bank(name, address, city, state, zip_code)

        # display pop-up message and await user input
        msgbox = tk.messagebox.askyesno(title='Confirm the Bank Information', message=bank.msg_alert(), parent=self)

        # if user confirms information uplaod bank into db using dbhelper class
        if msgbox == True:
            # create database conenction
            db = DataBaseHelper()

            # upload bank
            db.upload_bank(bank)

            # update ListBox
            self.get_banks()
        else: # if user selects no then do nothing
            pass

    
    # method called when remove bank button is clicked 
    # prompts user if they want to remove the selected item 
    # if yes use Datbase Helper to remove the selected Bank from the list
    def click_btn_removebank(self): 
        # get index of selected item
        index = self.list_banks.curselection()
        index = int(index[0]) # convert to int

        # find the selected bank object from the list
        bank = self.banks[index]

        msg = tk.messagebox.askokcancel(title='Are You Sure You Want to Remove This Bank?', message=bank.msg_alert(), parent=self)

        # if user selects ok then remove bank from db
        if msg == True:
            # establish db helper object (db connection)
            db = DataBaseHelper()

            # remove bank from list
            db.remove_bank(bank.bank_id)

            # update ListBox
            self.get_banks()
        else:
            pass


    # method used for viewing selected bank
    # gets index of selected bank 
    # finds bank in the list of banks at index // list[index]
    # displays that banks information in messagebox dialog
    def click_btn_viewbank(self):
        # get index of selected item
        index = self.list_banks.curselection()
        index = int(index[0]) # convert to int

        # find the selected bank object from the list
        bank = self.banks[index]

        # display selected bank using .msg_alert() method
        tk.messagebox.showinfo(title=bank.name, message=bank.msg_alert())




    # method used for updating selected bank
    def click_btn_updatebank(self):
        pass
