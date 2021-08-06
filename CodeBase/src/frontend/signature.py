
# class object that will house the information for the signautre to be added to the check 
# parameteres include the signee's name and the path to the image of thier signature

class Signature:

    def __init__(self, signee_name, signature_img_path, signature_id=None):
        self.name = signee_name
        self.path = signature_img_path
        self.id = signature_id

    
    # signature to string method 
    def __str__(self):
        return self.name

    
    def msg_alert(self):
        msg = "Signee Name: " + self.name + "\n\n"

        if self.path != None:
            msg += "Image Path: " + self.path + "\n\n"

        return msg

    
