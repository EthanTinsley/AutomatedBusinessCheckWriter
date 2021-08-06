import tkinter as tk
import docx2pdf
from .backend.database_helper import DataBaseHelper
from .backend.check_writer import CheckWriter


class CheckManagementFrame(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master=master, bg='gray80', highlightthickness=1, highlightbackground='black')
        # bg = background color , highlightthickness applies a border, highlightbackground sets the borders color
        self.master = master 

        # have the column 1 take up empty space
        self.columnconfigure(0, weight=1)

        # add widgets to the content frame 
        self.create_widgets()
        self.grid_widgets()


    
    def create_widgets(self):
        # some recurring data used within the method 
        btn_width=20
        bg_color = 'gray80'
        lbl_font = ('arial', 16)

        # create the lbls used within the frame 
        # lbl for section header 
        self.lbl_checkheader = tk.Label(master=self, text='Checks', bg=bg_color, font=lbl_font )

        # lbl for sorting the checks 
        self.lbl_sortcheckby = tk.Label(master=self, text='Sort By:' , bg=bg_color, font=lbl_font)

        # lbl for which elements to include in ListBox
        self.lbl_include = tk.Label(master=self, text='Include Check Features:', bg=bg_color, font=lbl_font)

        # list of checks
        self.list_checks = tk.Listbox(master=self, height=20, bg='white', selectmode = 'multiple')

        # checkbox for determing which elements to include in ListBox
        # Checkbox for Invoice Num
        self.var_invoicenum = tk.IntVar(value=1)
        self.chk_invoicenum = tk.Checkbutton(master=self, text='Invoice Num', bg=bg_color, variable=self.var_invoicenum, onvalue=1, offvalue=0 )

        # Checkboc for invoice date
        self.var_invoicedate = tk.IntVar(value=1)
        self.chk_invoicedate = tk.Checkbutton(master=self, text='Invoice Date',bg=bg_color, variable=self.var_invoicedate, onvalue=1, offvalue=0)

        # Checkboc for check num
        self.var_checknum = tk.IntVar(value=1)
        self.chk_checknum = tk.Checkbutton(master=self, text='Check Number',bg=bg_color, variable=self.var_checknum, onvalue=1, offvalue=0)

        # checkboc for check date
        self.var_checkdate = tk.IntVar(value=1)
        self.chk_checkdate = tk.Checkbutton(master=self, text="Check Date",bg=bg_color, variable=self.var_checkdate,onvalue=1, offvalue=0)
        # checkbox for payee
        self.var_payee = tk.IntVar(value=1)
        self.chk_payee = tk.Checkbutton(master=self, text="Payee",bg=bg_color, variable=self.var_payee,onvalue=1, offvalue=0)

        # checkbocx for account
        self.var_account = tk.IntVar(value=1)
        self.chk_account = tk.Checkbutton(master=self, text="Account",bg=bg_color,variable=self.var_account,onvalue=1, offvalue=0)

        # checkboc for amount
        self.var_amount = tk.IntVar(value=1)
        self.chk_amount = tk.Checkbutton(master=self, text="Amount",bg=bg_color,variable=self.var_amount, onvalue=1, offvalue=0)

        # checkbox for print status
        self.var_printed = tk.IntVar(value=1)
        self.chk_printed = tk.Checkbutton(master=self, text="Print Status",bg=bg_color,variable=self.var_printed,onvalue=1 , offvalue=0)

        # checkbox for upload date
        self.var_uploaddate = tk.IntVar(value=1)
        self.chk_uploaddate = tk.Checkbutton(master=self, text="Upload Date",bg=bg_color,variable=self.var_uploaddate, onvalue=1, offvalue=0)

        # btn used within the frame
        # btn for sorting by invoice number
        self.btn_orderbyinvoicenum = tk.Button(master=self, text="Invoice Number", width=btn_width, command=self.click_btn_orderbyinvoicenum)

        # btn used for sorting by invoice date
        self.btn_orderbyinvoicedate = tk.Button(master=self, text="Invoice Date", width=btn_width, command=self.click_btn_orderbyinvoicedate)

        # btn for sorting by check number
        self.btn_orderbychecknum = tk.Button(master=self, text="Check Number", width=btn_width, command=self.click_btn_orderbychecknum)

        # btn for sorting by check date
        self.btn_orderbycheckdate = tk.Button(master=self, text="Check Date", width=btn_width, command=self.click_btn_orderbycheckdate)

        # btn for sorting by payee
        self.btn_orderbypayee = tk.Button(master=self, text="Payee", width=btn_width, command=self.click_btn_orderbypayee)

        # btn for sorting by account
        self.btn_orderbyaccount = tk.Button(master=self, text="Account", width=btn_width, command=self.click_btn_orderbyaccount)

        # btn for sorting by check amount
        self.btn_orderbyamount = tk.Button(master=self, text="Amount", width=btn_width, command=self.click_btn_orderbyamount)

        # btn for sorting by print status
        self.btn_orderbyprintstatus = tk.Button(master=self, text="Print Status", width=btn_width, command= self.click_btn_orderbyprinted)

        # btn for sorting by upload date
        self.btn_orderbyuploaddate = tk.Button(master=self, text="Upload Date", width=btn_width, command=self.click_btn_orderbyuploaddate)

        # btn for printing selected Checks
        self.btn_printselectedchecks = tk.Button(master=self, text="Print Selected Checks", width=btn_width, command=self.click_btn_printselectedchecks )

        # btn for removing selected Checks 
        self.btn_removeselectedchecks = tk.Button(master=self, text="Delete Selected Checks", width=btn_width, command=self.click_btn_removeselectedchecks)

        # btn for updating selected check
        #self.btn_updateselectedcheck = tk.Button(master=self, text="Update Selected Check - Select Just One", width=btn_width , command=self.click_btn_updateselectedchecks)


    # method for adding widgets to the frame
    def grid_widgets(self):
        # add the widgets to the frame 
        # add the checks header
        self.lbl_checkheader.grid(row=0, column=0, sticky='nsew')

        # adds the include elemnt checkbox lbl to frame
        self.lbl_include.grid(row=0, column=1, sticky='nsew')

        # adds the sort by header to frame
        self.lbl_sortcheckby.grid(row=0, column=2, columnspan=1, sticky='nsew')

        # add listbox to the frame
        self.list_checks.grid(row=1, column=0, padx=30, pady=5, rowspan=9, columnspan=1, sticky='nsew')

        # add sort by buttons to frame 
        # sort by inovice number
        self.chk_invoicenum.grid(row=1, column=1, columnspan=1, padx=15, sticky='w')
        self.btn_orderbyinvoicenum.grid(row=1, column=2, columnspan=1, padx=15)

        # sort by inovice number
        self.chk_invoicedate.grid(row=2, column=1, columnspan=1, padx=15, sticky='w')
        self.btn_orderbyinvoicedate.grid(row=2, column=2, columnspan=1, padx=15)

        # sort by check number
        self.chk_checknum.grid(row=3, column=1, columnspan=1, padx=15, sticky='w')
        self.btn_orderbychecknum.grid(row=3, column=2, columnspan=1, padx=15)

        # sort by check date
        self.chk_checkdate.grid(row=4, column=1, columnspan=1, padx=15, sticky='w')
        self.btn_orderbycheckdate.grid(row=4, column=2, columnspan=1, padx=15)     

        # sort by payee
        self.chk_payee.grid(row=5, column=1, columnspan=1, padx=15, sticky='w')
        self.btn_orderbypayee.grid(row=5, column=2, columnspan=1, padx=15)     

        # sort by account
        self.chk_account.grid(row=6, column=1, columnspan=1, padx=15, sticky='w')
        self.btn_orderbyaccount.grid(row=6, column=2, columnspan=1, padx=15)     

        # sort by amount
        self.chk_amount.grid(row=7, column=1, columnspan=1, padx=15, sticky='w')
        self.btn_orderbyamount.grid(row=7, column=2, columnspan=1, padx=15)     

        # sort byprint status
        self.chk_printed.grid(row=8, column=1, columnspan=1, padx=15, sticky='w')
        self.btn_orderbyprintstatus.grid(row=8, column=2, columnspan=1, padx=15)     

        # sort by upload date
        self.chk_uploaddate.grid(row=9, column=1, columnspan=1, padx=15, sticky='w')
        self.btn_orderbyuploaddate.grid(row=9, column=2, columnspan=1, padx=15)     

        # add print seleceted Checks btn
        self.btn_printselectedchecks.grid(row=10, column=0, padx=15, pady=10)

        # add remove selected Checks btn
        self.btn_removeselectedchecks.grid(row=11, column=0, padx=15, pady=10)


    # method for adding check objects to the ListBox
    # determines which elements of the check objects to include in ListBox
    def fill_list_checks(self, checklist):
        # insure that the ListBox is Empty
        self.list_checks.delete(0,'end')

        # add the checks into ListBox 
        # add only elements of the check that are checked by the listbox
        for check in checklist:
            msg = ''   

            # determine which elements to add to the checkbox
            if self.var_checkdate.get() == 1:
                msg += 'Check Date: ' + str(check.check_date) 
            if self.var_checknum.get() == 1:
                msg += ' Check Number: ' + str(check.check_num)
            if self.var_invoicenum.get() == 1:
                msg += ' Invoice Number ' + str(check.invoice_num)
            if self.var_invoicedate.get() == 1:
                msg += ' Invoice Date ' + str(check.invoice_date)
            if self.var_payee.get() == 1:
                msg += ' Payee ' + str(check.payee)
            if self.var_account.get() == 1:
                msg += ' Account ' + str(check.account_code)
            if self.var_amount.get() == 1:
                msg += ' Amount ' + str(check.amount)
            if self.var_printed.get() == 1:
                if check.printed == True:
                    msg += 'Print Status: True '
                else:
                    msg += 'Print Status: False '
            if self.var_uploaddate.get() == 1:
                msg += ' Upload Date ' + str(check.upload_date)

            self.list_checks.insert('end', msg)

        # end method
            

    # method called when invoice num button is clicked 
    # gets all checks and sorts them by invoice number
    def click_btn_orderbyinvoicedate(self):
        # get datbase connection
        db = DataBaseHelper()

        # get the list of checks present in the frame
        self.checklist = db.get_all_checks('invoice_date')
        checklist = self.checklist


        # add the checks to the list box depending on which checkBoxes are selected
        self.fill_list_checks(checklist)

    
    def click_btn_orderbyinvoicenum(self):
        # get datbase connection
        db = DataBaseHelper()

        # get the list of checks present in the frame
        self.checklist = db.get_all_checks('invoice_num')

        # add the checks to the list box depending on which checkBoxes are selected
        self.fill_list_checks(self.checklist)

    
    def click_btn_orderbycheckdate(self):
        # get datbase connection
        db = DataBaseHelper()

        # get the list of checks present in the frame
        self.checklist = db.get_all_checks('check_date')

        # add the checks to the list box depending on which checkBoxes are selected
        self.fill_list_checks(self.checklist)
    

    def click_btn_orderbychecknum(self):
        # get datbase connection
        db = DataBaseHelper()

        # get the list of checks present in the frame
        self.checklist = db.get_all_checks('check_num')

        # add the checks to the list box depending on which checkBoxes are selected
        self.fill_list_checks(self.checklist)

    
    def click_btn_orderbypayee(self):
        # get datbase connection
        db = DataBaseHelper()

        # get the list of checks present in the frame
        self.checklist = db.get_all_checks('payee')

        # add the checks to the list box depending on which checkBoxes are selected
        self.fill_list_checks(self.checklist)

    
    def click_btn_orderbyaccount(self):
        # get datbase connection
        db = DataBaseHelper()

        # get the list of checks present in the frame
        self.checklist = db.get_all_checks('account_code')

        # add the checks to the list box depending on which checkBoxes are selected
        self.fill_list_checks(self.checklist)


    def click_btn_orderbyamount(self):
        # get datbase connection
        db = DataBaseHelper()

        # get the list of checks present in the frame
        self.checklist = db.get_all_checks('amount')

        # add the checks to the list box depending on which checkBoxes are selected
        self.fill_list_checks(self.checklist)
        

    def click_btn_orderbyprinted(self):
        # get datbase connection
        db = DataBaseHelper()

        # get the list of checks present in the frame
        self.checklist = db.get_all_checks('printed')

        # add the checks to the list box depending on which checkBoxes are selected
        self.fill_list_checks(self.checklist)

    
    def click_btn_orderbyuploaddate(self):
        # get datbase connection
        db = DataBaseHelper()

        # get the list of checks present in the frame
        self.checklist = db.get_all_checks('upload_date')

        # add the checks to the list box depending on which checkBoxes are selected
        self.fill_list_checks(self.checklist)



    # method called to print checks that are selected by the user in the ListBox
    # ask user to select a directory to export checks to
    def click_btn_printselectedchecks(self):
        # create check writer object 
        writer = CheckWriter()
        # create list to store selected checks objects
        selecetedchecks = []

        # ask for output directory 
        outputpath = tk.filedialog.askdirectory( master=self, title='Select an Output Directory')

        # get the indexes of the selected checks
        selectedchecksindex = self.list_checks.curselection()

        # create a list of selcted checks that contains Check() objcets to be printed
        for index in selectedchecksindex:
            
            # verfiy printing duplicate checks
            printed = self.verify_print_dup(self.checklist[index])

            if printed == True:
                selecetedchecks.append(self.checklist[index])
            elif printed == False:
                continue
            else:
                return

        # print the selected checks
        writer.print_check(selecetedchecks, outputpath)

        # see if user wants to convert files in that directory
        self.convert2pdf(outputpath)


    # method called to remove the slected checks from the db
    # ask user to confirm before removing
    def click_btn_removeselectedchecks(self):
        # ask for output directory 
        confirm_msg = tk.messagebox.askyesno(parent=self, title="Are you sure you want to remove selected Checks?", message="Are you sure you want to remove selected Checks?")

        if confirm_msg == True:
            # get the indexes of the selected checks
            selectedchecksindex = self.list_checks.curselection()

            # create db connection
            db = DataBaseHelper()

            # counter used in loop
            count =0

            # create a list of selcted checks that contains Check() objcets to be printed
            for index in selectedchecksindex:

                # get check object
                check = self.checklist[index-count]

                # remove check from db
                db.remove_check(check.id)

                # remove check from checklist
                self.checklist.remove(check)
                
                # use counter to account for the items being removed from list 
                count += 1
            
            self.fill_list_checks(self.checklist)
        else:
            pass


# method used for prompting the user and offering to convert their docx files to pdf files
    def convert2pdf(self, inputdir):

        # prompt user if they want docx files converted
        msg = tk.messagebox.askyesno(title="Convert to PDF format?", message="Would you like to convert printed files to pdf files?")

        if msg == True:
            docx2pdf.convert(input_path=inputdir)
        else:
            pass
    
    
    # method for detecting printing multiple checks
    def verify_print_dup(self, check):
        # determine if check has been printed
        if (check.printed == True):
            msg = tk.messagebox.askyesnocancel(title="Check Has Been Printed Previosly! ", message ="Check Has Already Been Printed! Would You Still Like to Print This Check? \n\n" + check.msg_alert())

            return msg 
        
        else:
            return True
