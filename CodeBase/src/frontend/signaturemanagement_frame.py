import tkinter as tk
from tkinter import ttk
from .backend.signature import Signature
from .backend.database_helper import DataBaseHelper
from shutil import copy
import os

# class will be an interface in order for the user to manage signatures on file 
class SignatureManagementFrame(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master=master,bg='gray80', highlightthickness=1, highlightbackground='black')
        # bg = background color , highlightthickness applies a border, highlightbackground sets the borders color
        
        # delcare master object usually mainframe 
        self.master = master

        # create and add widgets to the frame
        self.create_widgets()
        self.grid_widgets()

        # add items into the ListBox
        self.get_signatures()

        # have the empty space filled by ListBox widget
        self.columnconfigure(0,weight=1)


    # method for creating the frames widgets
    def create_widgets(self):
        # some recurring data used within the method 
        btn_width=20
        bg_color = 'gray80'
        lbl_font = ('arial', 16)

        # create the lbls used within the frame 
        # lbl for section header 
        self.lbl_signatureheader = tk.Label(master=self, text='Signatures', bg=bg_color, font=lbl_font )

        # lbl for adding a signature
        self.lbl_addsignatureheader = tk.Label(master=self, text='Add a Signature',bg=bg_color, font=lbl_font )

        # singature name prompt
        self.lbl_signaturename = tk.Label(master=self,text='Signature Name: ', bg=bg_color, font=lbl_font )

        # signature img prompt
        self.lbl_signatureaddpath = tk.Label(master=self, text='Upload Signature Image: ', bg=bg_color, font=lbl_font )

        # signature img path lbl 
        self.lbl_signaturepath = tk.Label(master=self,text='Image Needs to be Added', font=lbl_font, bg=bg_color)

        # entry widgets used within the forms
        # entry for account code 
        self.ent_signaturename = tk.Entry(master=self)

        # buttons used within the frame
        # button to add an image path to the newly created signatrue
        self.btn_addimage = tk.Button(master=self, width=btn_width, text='Add Signature Image', command=self.click_btn_addimage)

        # create button for uploading company to the database
        self.btn_addsignature = tk.Button(master=self, width=btn_width, text='Add Signature', command=self.click_btn_addsignature)

        # create button for removing selected signature 
        self.btn_removesignature = tk.Button(master=self, width=btn_width, text='Remove Selected Signature', command=self.click_btn_removesignature)

        # create button for viewing the selected signature
        self.btn_viewsignature = tk.Button(master=self, width=btn_width, text='View Selected Signature', command=self.click_btn_viewsignature)

        # create button for updating seleected signature
        self.btn_updatesignature = tk.Button(master=self, width=btn_width, text='Update Selected Signature', command=self.click_btn_updatesignature)
        
        # list box used within the frame 
        # existing signatures listbox
        self.list_signatures = tk.Listbox(master=self, bg='white', height=20)



    # method for adding widgets to the frame
    def grid_widgets(self):
        # add the widgets to the frame 
        # add the accounts header
        self.lbl_signatureheader.grid(row=0, column=0, sticky='nsew')

        # add the add account header 
        self.lbl_addsignatureheader.grid(row=0, column=1, columnspan=2, sticky='nsew')

        # add the accounts listbox
        self.list_signatures.grid(row=1, column=0, padx=30, pady=5, rowspan=4, columnspan=1, sticky='nsew')

        # add the signature name prompt to frame
        self.lbl_signaturename.grid(row=1,column=1, sticky='e')
        self.ent_signaturename.grid(row=1,column=2, sticky='w', padx=20)

        # add the signature path prompt to frame
        self.lbl_signatureaddpath.grid(row=2,column=1, sticky='e') 
        self.btn_addimage.grid(row=2, column=2, padx=20, pady = 10)
        self.lbl_signaturepath.grid(row=3,column=1,columnspan=2, sticky='n')
        
        # add remove btn 
        self.btn_removesignature.grid(row=5, column=0, pady=10, sticky='ns')

        # add the add btn 
        self.btn_addsignature.grid(row=5, column=1, pady = 10 , sticky='ns', columnspan=2)

        # add view btn 
        self.btn_viewsignature.grid(row=6, column=0, pady = 10, sticky='ns')

        # add update btn 
        #self.btn_updatesignature.grid(row=7, column=0 , pady = 10 , sticky='ns')


    # method for adding exisitnig signatures to ListBoc widget
    def get_signatures(self):
        # create db connection
        db = DataBaseHelper()

        # get all signatures from the db 
        self.signaturelist = db.get_all_signatures()

        # ensure the list is clear 
        self.list_signatures.delete(0,'end')

        # add signatures to ListBox
        for s in self.signaturelist:
            self.list_signatures.insert('end', s)



    # method for uplaoding an image of a signature 
    def click_btn_addimage(self):
        # get the file path of the selected file
        self.path = tk.filedialog.askopenfilename(master=self, title='Please Upload a Signature Image', filetypes=[("jpeg files","*.jpg"),("png files","*.png")])

        #  save the filename for later reference 
        self.filename = os.path.basename(self.path)

        # display the iamge path in the img path label
        self.lbl_signaturepath.config(text=('Image Added Successfully!'))


    # method for uplaoding signature to db
    def click_btn_addsignature(self):
        # parse input for information
        name = self.ent_signaturename.get()
        path = self.path

        # create signatue object
        signature = Signature(name, path)

        # ask user for validation
        msg = tk.messagebox.askyesno(title='Upload signature?', message=signature.msg_alert())

        # if user selects yes then add signature to db otherwise do nothing
        if msg == True:
            # save the file in the sub signature img file
            self.save_image(name)
            
            # update signature object to reflect new image path
            signature.path = self.path

            # create db connection
            db = DataBaseHelper()

            # uplaod signature
            db.upload_signature(signature)

            # update ListBox
            self.get_signatures()
        else:
            pass


    # method for removing signature to db
    def click_btn_removesignature(self):
        # get the index of the selected ListBox item
        index = self.list_signatures.curselection()
        index = int(index[0])

        # get the signature object from the list at the selected index
        sig = self.signaturelist[index]

        # get user validation before removing
        msg = tk.messagebox.askokcancel(title=sig , message="Remove? \n" + sig.msg_alert(), parent=self)

        # if user selects ok then remove from db else do nothing
        if msg == True:
            # establish db helper 
            db = DataBaseHelper()

            # remove signature from db 
            db.remove_signature(sig.id)

            # update ListBox
            self.get_signatures()
        else:
            pass
        

    # method for updating a signature to db
    def click_btn_updatesignature(self):
        pass

    # method for viewing signature in db
    def click_btn_viewsignature(self):
        # get the index of the selected ListBox item
        index = self.list_signatures.curselection()
        index = int(index[0])

        # get the signature object from the list at the selected index
        sig = self.signaturelist[index]

        # create msgbox to display signature object contents
        tk.messagebox.showinfo(title=sig, message=sig.msg_alert(), parent=self)

    
    # method for saving images into subfolder signature folder
    def save_image(self, signature_name):
        # save the image to the subdirectory folder
        copy(self.path, './frontend/backend/signature_img')

        # temp variable to hold new path
        temp_oldname = './frontend/backend/signature_img/' + self.filename
        temp_newname = './frontend/backend/signature_img/' + signature_name + '.png'
        
        # rename the file in the subdirectory
        os.rename(temp_oldname, temp_newname)

        # update path to relfect new directory
        self.path = temp_newname

