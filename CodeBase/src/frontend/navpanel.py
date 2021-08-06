import tkinter as tk
from .checkmanagement_frame import CheckManagementFrame
from .checkbookupload_frame import CheckbookUploadFrame
from .companymanagement_frame import CompanyManagementFrame
from .bankmanagement_frame import BankManagementFrame
from .accountmanagement_frame import AccountManagementFrame
from .signaturemanagement_frame import SignatureManagementFrame

# class to create the navigation panel present throughtout 
# most of the applications GUI pages 
# navigation panel enables the user to navigate throught the application
class NavPanel(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master=master, bg='gray64', highlightthickness=1, highlightbackground='black')
        # bg = background color , highlightthickness applies a border, highlightbackground sets the borders color
        
        # delcare master object usually mainframe 
        self.master = master

        # place the widgets on the navigation panel
        self.create_widgets()
        self.grid_widgets()

    
    def create_widgets(self):
        btn_pady=12
        btn_padx=10
        btn_ipady=None
        btn_ipadx=None

        # create the checkbook upload window button
        # pad = external padding 
        # ipad = internal padding
        # create the button for viewing the checkbook uplaod frame
        self.btn_checkbookupload = tk.Button(master=self, text='Checkbook upload', command=self.click_btn_checkbookupload )
        
        # create the button for viewing the check management frame
        self.btn_checkmanagement = tk.Button(master=self, text='Check Management', command=self.click_btn_checkmanagement)
        
        # create the button for managing uplaoded company information
        self.btn_companymanagement = tk.Button(master=self, text='Company Management', command=self.click_btn_companymanagement)

        # create the button for managing uplaoded bank information
        self.btn_bankmanagement = tk.Button(master=self, text='Bank Management', command=self.click_btn_bankmanagement)

        # create the button for managing uplaoded company information
        self.btn_accountmanagement = tk.Button(master=self, text='Account Management', command=self.click_btn_accountmanagement)
        
        # create the button for managing uplaoded signature information
        self.btn_signaturemanagement = tk.Button(master=self, text='Signature Management', command=self.click_btn_signaturemanagement)
        
        

    
    #method to add the created widgets to the panel
    def grid_widgets(self):
        btn_pady=12
        btn_padx=10
        btn_ipady=None
        btn_ipadx=None

        # pad = external padding 
        # ipad = internal padding
        # add the checkbookupload_btn to the frame
        self.btn_checkbookupload.grid(row=0, column=0, padx=btn_padx, pady=btn_pady,sticky='nsew')

        # add the check management btn to the frame
        self.btn_checkmanagement.grid(row=1, column=0, padx=btn_padx, pady=btn_pady,sticky='nsew')

        # add the company managemnet btn to the frame 
        self.btn_companymanagement.grid(row=2, column=0, padx=btn_padx, pady=btn_pady,sticky='nsew')

        # add the bank managemnet btn to the frame 
        self.btn_bankmanagement.grid(row=3, column=0, padx=btn_padx, pady=btn_pady,sticky='nsew')

        # add the signature menagement btn to the Frame
        self.btn_signaturemanagement.grid(row=4, column=0, padx=btn_padx, pady=btn_pady,sticky='nsew')

        # add the company managemnet btn to the frame 
        self.btn_accountmanagement.grid(row=5, column=0, padx=btn_padx, pady=btn_pady, sticky='nsew')


    # a method called by the checkbookupload_btn Button 
    # changes the current content frame to the check upload frame
    # calls the master change_frame method 
    def click_btn_checkbookupload(self):
        # if current pane is not checkbook upload frame then change the content frame to the checkbook uplaod 
        if isinstance(self.master.contentframe , CheckbookUploadFrame):
            pass
        else:
            # create frame to set the content frame to
            contentframe = CheckbookUploadFrame(master=self.master)
            #contentframe.columnconfigure([0,1], weight=1)

            # change the current contnet frame to the new one 
            self.master.change_contentframe(contentframe)

    
    # a method called by the checkmanagement_btn Button 
    # changes the current content frame to the check management frame
    # calls the master change_frame method 
    def click_btn_checkmanagement(self):
        # if current pane is not checkmanagement frame then change the content frame to the checkbook uplaod 
        if isinstance(self.master.contentframe , CheckManagementFrame):
            pass
        else:
            # create frame to set the content frame to
            contentframe = CheckManagementFrame(master=self.master)

            # change the current contnet frame to the new one 
            self.master.change_contentframe(contentframe)
        
    
    # a method called by the btn_companymanagemnet Button 
    # changes the current content frame to the comapny management frame
    # calls the master change_frame method 
    def click_btn_companymanagement(self):
        # if current pane is not checkmanagement frame then change the content frame to the checkbook uplaod 
        if isinstance(self.master.contentframe , CompanyManagementFrame):
            pass
        else:
            # create frame to set the content frame to
            contentframe = CompanyManagementFrame(master=self.master)

            # change the current contnet frame to the new one 
            self.master.change_contentframe(contentframe)
        
    
    # a method called by the btn_bankmanagemnet Button 
    # changes the current content frame to the bank management frame
    # calls the master change_frame method 
    def click_btn_bankmanagement(self):
         # if current pane is not checkmanagement frame then change the content frame to the checkbook uplaod 
        if isinstance(self.master.contentframe , BankManagementFrame):
            pass
        else:
            # create frame to set the content frame to
            contentframe = BankManagementFrame(master=self.master)

            # change the current contnet frame to the new one 
            self.master.change_contentframe(contentframe)


    # a method called by the btn_accountanagemnet Button 
    # changes the current content frame to the account management frame
    # calls the master change_frame method 
    def click_btn_accountmanagement(self):
        # if current pane is not checkmanagement frame then change the content frame to the checkbook uplaod 
        if isinstance(self.master.contentframe , AccountManagementFrame):
            pass
        else:
            # create frame to set the content frame to
            contentframe = AccountManagementFrame(master=self.master)

            # change the current contnet frame to the new one 
            self.master.change_contentframe(contentframe)

    
    # method for displaying signature management frame
    def click_btn_signaturemanagement(self):
        # if current pane is signature frame then do nothing, otherwise switch to the appropriate frame
        if isinstance(self.master.contentframe , SignatureManagementFrame):
            pass
        else:
            # create new frame to pass to master
            contentframe = SignatureManagementFrame(master=self.master)

            # change the frame to the newlu created signature frame
            self.master.change_contentframe(contentframe)

