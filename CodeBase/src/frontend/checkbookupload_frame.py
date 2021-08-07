import tkinter as tk
import docx2pdf 
from tkinter import filedialog
from .backend.check import Check
from .backend.check_writer import CheckWriter
from .backend.file_reader import FileReader
from .backend.database_helper import DataBaseHelper

# a frame to fill the mainframes content pane
# frame will house the file-uplaoder to uplaod checkbook for uplaod 
# will house ability to upload, or uplaod and save the checkbook being uploaded 
class CheckbookUploadFrame(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master=master, bg='gray80', highlightthickness=1, highlightbackground='black')
        # bg = background color , highlightthickness applies a border, highlightbackground sets the borders color

        self.master = master 

        # add widgets to the content frame 
        self.create_widgets()
        self.grid_widgets()

        # make the widgets expand to fill the frame accordingly
        self.columnconfigure([0,1], weight=1)


    # method for creatig widgets used within the frame
    def create_widgets(self):
        # various padding used within the method
        txt_width=80
        txt_height=35
        btn_width=20
        bg_color = 'gray80'

        # create the labels for this frame
        # label to display above the textbox 
        self.lbl_filepath = tk.Label(master=self, text='Upload a Checkbook for printing', bg=bg_color, font=('arial',16))
        # label to prompt the user to select a file
        self.lbl_selectfile = tk.Label(master=self, text='Select a File:', bg=bg_color, font=('arial', 16))

        # create textbox for use in the frame
        self.txt_filepath = tk.Text(master=self, width=txt_width, height=txt_height, wrap='none', highlightbackground='black', highlightthickness=1)

        # create the buttons used in this frame
        # create a button for selecting a file 
        self.btn_selectfilepath = tk.Button(master=self, text='Upload a file',width=btn_width, command=self.click_btn_selectfilepath )
        # create a button for uplaoding the selected file
        self.btn_uploadcheckbook = tk.Button(master=self, text='Upload Checkbook',width=btn_width, command=self.click_btn_uploadcheckbook)
        # create a button for uploading AND printing the file 
        self.btn_uploadandprint = tk.Button(master=self, text='Upload and Print Checkbook', width=btn_width, command=self.click_btn_uploadandprintcheckbook)



    # method for adding widgets to the frame 
    def grid_widgets(self):
        # various padding used within the method for labels
        lbl_pady=12 
        lbl_padx=10
        # padding for text boxes
        txt_width=25
        txt_height=10
        txt_pady=0 
        txt_padx=30 
        # padding for buttons
        btn_padx=12
        btn_pady=10
        btn_ipadx=6
        btn_ipady=6

        # add the label that displays above the textbox
        self.lbl_filepath.grid(row=0, column=0, columnspan=2, sticky='s')

        # add the text box for storing the filepath the user selects
        self.txt_filepath.grid(row=1,column=0, padx=txt_padx, pady=txt_pady, columnspan=2, rowspan=2, sticky='nsew')
        self.txt_filepath.config(state = 'disabled')

        # add the label to prompt the user to select a file for upload
        self.lbl_selectfile.grid(row=3, column=0, padx=lbl_padx,pady=lbl_pady, sticky='e')

        # add the button for uploading a file
        self.btn_selectfilepath.grid(row=3, column=1, ipadx=btn_ipadx, ipady=btn_ipady, padx=btn_padx, pady=btn_pady, sticky='w')

        # add the checkbook upload button to the frame 
        self.btn_uploadcheckbook.grid(row=4, column=0, ipadx=btn_ipadx, ipady=btn_ipady, padx=btn_padx, pady=btn_pady, sticky='e' )

        # add the checkbook uplaod and save button to the frame
        self.btn_uploadandprint.grid(row=4, column=1, ipadx=btn_ipadx, ipady=btn_ipady, padx=btn_padx, pady=btn_pady, sticky='w' )



    # command method to be called when the user clicks on select a file button
    # pull up a file selector window and have the user select the checkbook they wish to uplaod
    # display the file path in the textbox 
    def click_btn_selectfilepath(self):
        path = None
        # display file dialog 
        # store the selected file in path variable 
        path = tk.filedialog.askopenfilename( master=self, title='Select a Checkbook', filetypes=[("Commas Separated Values files", "*.csv"), ("JSON files", "*.json"), ( "XML files", "*.xml")])

        # if user selected a file display the selected file path in appropriate labels
        if ((path != '') & (path != None)):
            # make textbox editable
            self.txt_filepath.config(state='normal')

            # store the path in the frame
            self.path = path 

            # ensure that txt is empty
            self.txt_filepath.delete("1.0", "end")

            # display the file path in the appropraite text box
            self.txt_filepath.insert('1.0', (self.path + '\n\n'))

        self.txt_filepath.config(state='disabled')

        # display contnents of file 
        self.read_upload_file()

    
    # method for displaying checks stored within uploaded file
    def read_upload_file(self):
        # read the file and display the check objects within the text box 
        # creater FileReader object
        reader = FileReader(self.path)

        # read the file
        self.checkbook = reader.read_file()

        # make textbox editable
        self.txt_filepath.config(state='normal')

        # add section header
        self.txt_filepath.insert(3.0, 'Checks Exctracted From File \n\n')

        # add the extracted checks to the txt box
        for check in self.checkbook:
            
            # add check to textbox
            self.txt_filepath.insert(4.0, str(check)+'\n')
        
        # disable txt box
        self.txt_filepath.config(state='disabled')
    

    # method for parsing the uploaded file and uploading it to the database
    # store success contents in textbox 
    def click_btn_uploadcheckbook(self):
        # create db connection
        db = DataBaseHelper()

        # upload checkbook to db
        for check in self.checkbook:
            # ensure inserted check is not a duplicate
            verification = self.verify_orignal(check)
            
            if verification == True:
                db.upload_check(check)
            elif verification == False:
                continue
            else:
                return

        # update txt box to notify that checks are uploaded
        self.txt_filepath.config(state='normal')
        
        self.txt_filepath.insert('end', 'Checkbook Uploaded Successfully! \n')

        self.txt_filepath.config(state='disabled')
    


    # method for parsing the uplaoded file and uploading it to the datbase 
    # then print the files in a user selected output directory 
    # select output directory by filedialog 
    def click_btn_uploadandprintcheckbook(self):
        # upload checkbook
        self.click_btn_uploadcheckbook()

        # create check book writer object
        writer = CheckWriter()

        # ask for output directory 
        outputpath = tk.filedialog.askdirectory( master=self, title='Select an Output Directory')

        # print checkbook
        writer.print_check(self.checkbook, outputpath)

        # ask for pdf conversion
        self.convert2pdf(outputpath)
        
        # update txt box to notify that checks are uploaded
        self.txt_filepath.config(state='normal')
        
        self.txt_filepath.insert('end', 'Checkbook Printed Successfully! \n')

        self.txt_filepath.config(state='disabled')

    

    # method for checking if check has already been uploaded to db or not 
    def verify_orignal(self, check):
        # get db connection
        db = DataBaseHelper()

        # determine if check is already in db 
        duplicate = db.duplicate_check_test(check)

        if duplicate == True:
            msg = tk.messagebox.askyesnocancel(title="Duplicate Detected", message=("Duplicate Check Detected! \n\n Are you sure that you want to upload this check? \n" + check.msg_alert()))

            # if check needs to be uploaded == True
            # if move to next check == False 
            # if stop trying to uplaod checkbook = None
            return msg
        else:
            return True


    # method for determining if multiple checks should be printed together
    # IE multiple charges in the memo table belonging to a single check
    def verify_multicharge_checks(self):
        checkbook = self.checkbook
        duplicatecheck_nums = []    
        
    
    # method used for prompting the user and offering to convert their docx files to pdf files
    def convert2pdf(self, inputdir):

        # prompt user if they want docx files converted
        msg = tk.messagebox.askyesno(title="Convert to PDF format?", message="Would you like to convert printed files to pdf files?")

        if msg == True:
            docx2pdf.convert(input_path=inputdir)
        else:
            pass