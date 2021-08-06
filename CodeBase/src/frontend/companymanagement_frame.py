import tkinter as tk
from tkinter import messagebox
from .backend.company import Company
from .backend.database_helper import DataBaseHelper


# class used to create the GUI page for adding, managaing, and removing company objects from database
# class is called via navpanel and displayed within the mainframe 
# uses database helper class to handle database interactions
class CompanyManagementFrame(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master=master, bg='gray80', highlightthickness=1, highlightbackground='black')

        # bg = background color , highlightthickness applies a border, highlightbackground sets the borders color
        
        # delcare master object usually mainframe 
        self.master = master

        # place the widgets on the navigation panel
        self.create_widgets()
        self.grid_widgets()

        # populate listbox with companies stored within the db
        self.get_companies()

        # make the wiget expand to fill the frame accordingly
        self.columnconfigure(0, weight=1)
        #self.rowconfigure([0,6], weight=1)

    
    # method used to create the widgets within the frame
    def create_widgets(self):
        # some recurring data used within the method 
        btn_width=20
        bg_color = 'gray80'
        lbl_font = ('arial', 16)

        # create the lbls used within the frame 
        # create the lbl that displays above the listbox 
        self.lbl_companynames = tk.Label(master=self, text='Exisiting Companies', bg=bg_color, font=lbl_font )

        # create the lbl for adding a compny 
        self.lbl_addcomapny = tk.Label(master=self, text='Add a Company', bg=bg_color, font=lbl_font )
        
        # create hte lbl for entering in company name
        self.lbl_addcompanyname = tk.Label(master=self, text='Company Name:', bg=bg_color, font=lbl_font )

        # create the lbl for entering in company address
        self.lbl_addcompanyaddress = tk.Label(master=self, text='Company Address:', bg=bg_color, font=lbl_font )

        # create the lbl for entering in company city
        self.lbl_addcompanycity = tk.Label(master=self, text='Company City:', bg=bg_color, font=lbl_font )

        # create the lbl for entering in company state
        self.lbl_addcompanystate = tk.Label(master=self, text='Company State:', bg=bg_color, font=lbl_font )

        # create the lbl for entering in company zip code
        self.lbl_addcompanyzip = tk.Label(master=self, text='Company Zip Code:', bg=bg_color, font=lbl_font )

        # create entry forms used within the form 
        # create entry from for accepting company name 
        self.ent_addcompanyname = tk.Entry(master=self)

        # create entry for entering in company address
        self.ent_addcompanyaddress = tk.Entry(master=self)

        # create entry for entering in company city
        self.ent_addcompanycity = tk.Entry(master=self)

        # create entr for entering in company state
        self.ent_addcompanystate = tk.Entry(master=self)

        # create entry for entering in company zip code
        self.ent_addcompanyzip = tk.Entry(master=self)

        # create buttons used within the form
        # create button for uploading company to the database
        self.btn_addcompany = tk.Button(master=self, width=btn_width, text='Add Company', command=self.click_btn_addcompany)

        # create button for removing selected company 
        self.btn_removecompany = tk.Button(master=self, width=btn_width, text='Remove Selected Company', command=self.click_btn_removecompany)

        # add button to view selected company 
        self.btn_viewcompany = tk.Button(master=self, width=btn_width, text="View Selected Company", command=self.click_btn_viewcompany)
        
        # add button to update selected company 
        self.btn_updatecompany = tk.Button(master=self, width=btn_width, text="Update Selected Company", command=self.click_btn_viewcompany)

        # create the listbox used within the frame 
        self.list_companies = tk.Listbox(master=self, bg='white', height=20)


    # method used to place the widgets on the frame 
    def grid_widgets(self):
        
        # add the company names label to the frame
        self.lbl_companynames.grid(row=0,column=0, sticky= 'nsew')

        # add the add a compnay prompt to the frame
        self.lbl_addcomapny.grid(row=0, column=1, columnspan= 2, sticky= 'nsew')
        
        # add the company listbox to the frame
        self.list_companies.grid(row=1,column=0, padx=30, pady=5, rowspan=5, columnspan=1, sticky='nsew')

        # add the add company name lbl and ent
        self.lbl_addcompanyname.grid(row=1, column=1,padx=20, sticky='e')
        self.ent_addcompanyname.grid(row=1, column=2,padx=20, sticky='w')

        # add the add company address lbl and ent 
        self.lbl_addcompanyaddress.grid(row=2, column=1,padx=20, sticky='e')
        self.ent_addcompanyaddress.grid(row=2, column=2,padx=20, sticky='w')

        # add the add company city lbl and ent
        self.lbl_addcompanycity.grid(row=3, column=1,padx=20, sticky='e')
        self.ent_addcompanycity.grid(row=3, column=2,padx=20, sticky='w')

        # add the add company state lbl and ent 
        self.lbl_addcompanystate.grid(row=4, column=1,padx=20, sticky='e')
        self.ent_addcompanystate.grid(row=4, column=2,padx=20, sticky='w')

        # add the add company zip lbl and ent
        self.lbl_addcompanyzip.grid(row=5, column=1,padx=20, sticky='e')
        self.ent_addcompanyzip.grid(row=5, column=2,padx=20, sticky='w')

        # add the add company button to the form
        self.btn_addcompany.grid(row=6, column=1,padx=20, pady=10, sticky='ns', columnspan=2)

        # add the remove company button to the form
        self.btn_removecompany.grid(row=6, column=0, padx=20, pady=10, sticky='ns')
        
        # add the view company button to the fomr
        self.btn_viewcompany.grid(row=7, column=0, padx=20, pady=10, sticky='ns')

        # add the update company button to the form
        #self.btn_updatecompany.grid(row=8, column=0, padx=20, pady=10, sticky='ns')


    # method used for gathering all comapnies from database
    def get_companies(self):
        # establish connection to database     
        db = DataBaseHelper()

        # retrun all companies stored within database
        self.companies = db.get_all_companies()

        # insure ListBox is clear
        self.list_companies.delete(0, 'end')

        for comp in self.companies:
            self.list_companies.insert('end', comp)
        


    # method called when user clicks add company button
    # parses text boxes and displays an alert message for user to confrim that the information 
    # is as they want it 
    # when they click yes create a Company object and upload it into the datbase
    def click_btn_addcompany(self):
        # parse entry forms to create company object
        name = self.ent_addcompanyname.get()
        address = self.ent_addcompanyaddress.get()
        city = self.ent_addcompanycity.get()
        state = self.ent_addcompanystate.get()       
        zip_code = self.ent_addcompanyzip.get()

        # create company object
        company = Company(name, address, city, state, zip_code)

        # display pop-up message and await user input
        msgbox = tk.messagebox.askyesno(title='Confirm the Company Information', message=company.msg_alert(), parent=self)

        # if user selects yes then uplaod to database
        if msgbox == True:
            # establish connection to db
            db = DataBaseHelper()

            # uplaod to db
            db.upload_company(company)

            # update ListBox
            self.get_companies()

        else:
            pass

    
    # method called when remove company button is clicked 
    # prompts user if they want to remove the selected item 
    # if yes use Datbase Helper to remove the selected Company from the list
    def click_btn_removecompany(self):
        # get the selected check from the listbox
        index = self.list_companies.curselection()
        index = int(index[0]) # convert from tuple to int

        # get the company object from the companies list using the index
        company = self.companies[index]

        # display warning message with selected company 
        msgbox = tk.messagebox.askokcancel(title='Confirm the Company Information', message=company.msg_alert(), parent=self)

        # determine user selection
        if msgbox == True:
            # get db connection
            db = DataBaseHelper()

            # remove company from database
            db.remove_company(company.company_id)

            # update list of companies along with listbox
            self.get_companies()
        
        else: # if user presses cacncel do nothing
            pass 


    # method for viewing the contents of a selected company 
    # displays company contents in alert pop up 
    def click_btn_viewcompany(self):
        # get seleted companies index from ListBox
        index = self.list_companies.curselection()
        index = int(index[0])

        # get the company that is selected 
        comp = self.companies[index]

        # display company information 
        tk.messagebox.showinfo(title=comp.name, message=comp.msg_alert())