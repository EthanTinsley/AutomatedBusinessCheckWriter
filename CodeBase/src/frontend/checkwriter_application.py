import tkinter as tk 
from .mainframe import MainFrame

# class for displaying the interactive gui 
# inherits the tk.Tk() constructor 
# tk.Tk() mainloop() function displays the GUI window 
# utilizes mainframe object to display content within applciation
class CheckWriterApplication(tk.Tk):

    def __init__(self):
        super().__init__()

        # method for changing application specifications 
        self.set_features()        
        
        # method for intializing content on Tk window 
        self.create_mainframe()

        
    
    # method utilzied to customize frame dimensions/ features
    def set_features(self):
        
        # set frame size
        self.geometry('1000x600')

        # set row and column configuration to enable widget scaling
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # set application window title 
        self.title('Check Writer Application')

    
    # method for adding the mainframe to the applicatio window
    def create_mainframe(self):
        # create MainFrame object
        self.mainframe = MainFrame(master=self)

