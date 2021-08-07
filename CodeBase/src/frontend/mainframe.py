import tkinter as tk 
from .navpanel import NavPanel
from .checkbookupload_frame import CheckbookUploadFrame
from .checkmanagement_frame import CheckManagementFrame

# create a class instance of the tkinter Frame widget 
# mainframe obejct will be the 'background' frame from which we will 
# post the navigation and content planes upon to fill out the GUI 
class MainFrame(tk.Frame):

    # tk.Frame() requires a master object which is the object the Frame is being posted on 
    # in the case of the MainFrame this should always be the root application window
    def __init__(self, master=None):
        super().__init__(master=master)

        # delcare the master of the frame
        self.master = master

        # place the frame at (0,0) on the window and align to the thop left corner 
        self.grid(row=0, column=0, sticky='nsew')

        # set to where columns configure to fill the apllication windwo accordingly
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)

        # add the navigation panel to the mainframe
        self.create_navpanel()

        # add the content frame to the mainframe
        self.create_contentframe()

    
    # a method for serring the navpanel to the mainframe
    def create_navpanel(self):
        # add the navigation panel to the mainframe
        # place frame on the master object accordingly
        # ipad = internal padding
        # sticky = alignment
        self.navpanel = NavPanel(master=self)
        self.navpanel.grid(row=0,column=0, ipadx=10, ipady=10, sticky='nsew')
        self.navpanel.grid_columnconfigure(0, weight=1)


    # a method for setting the contentpane on the mainframe
    def create_contentframe(self):
        # add the content frame to the mainframe
        self.contentframe = CheckbookUploadFrame(master=self)
        self.contentframe.grid(row=0,column=1, sticky='nsew')
        #self.contentframe.grid_columnconfigure([0,1], weight=1)


    # a method for changing the current content frame
    def change_contentframe(self, contentframe):
        # remove current frame
        self.contentframe.grid_forget()

        # add the new frame
        self.contentframe = contentframe
        self.contentframe.grid(row=0,column=1, sticky='nsew')





