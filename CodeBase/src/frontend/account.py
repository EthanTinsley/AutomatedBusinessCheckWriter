

class Account:


    def __init__(self, account_code, account_num, routing_num, company=None, bank=None, signature=None, account_id=None):
        self.account_code = account_code
        self.account_num = account_num
        self.routing_num = routing_num
        self.company = company
        self.bank = bank
        self.signature = signature
        self.account_id = account_id
        

    # account tostring method
    def __str__(self):
        return ("Account Code: " + str(self.account_code))

    
    def msg_alert(self):
        msg = "Account Code: " + str(self.account_code) + "\n\n"
        msg += "Account Num: " + str(self.account_num) + "\n\n"
        msg += "Routing Num: " + str(self.routing_num) + "\n\n"

        if self.company != None:
            msg += "Company: " +str(self.company)
        
        if self.bank != None:
            msg += "Bank: " +str(self.bank)

        if self.signature != None:
            msg += "Signature: " +str(self.signature)

        return msg
