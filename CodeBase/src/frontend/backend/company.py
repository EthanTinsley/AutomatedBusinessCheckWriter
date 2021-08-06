

class Company:
    


    def __init__(self, company_name, address, city, state, zip_code, id=None):
        self.name = company_name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip_code
        self.company_id = id

    

    # python toString() method
    def __str__(self):
        return self.name

    
    # method to display company information into a warning message before deletion
    def msg_alert(self):
        msg = 'Company Name: ' + self.name + '\n\n'
        msg += 'Company Address: ' + self.address + '\n\n'
        msg += 'Company City: ' + self.city + '\n\n'
        msg += 'Company State: ' + self.state + '\n\n'
        msg += 'Company Zip Code: ' + str(self.zip) + '\n\n'

        return msg

        