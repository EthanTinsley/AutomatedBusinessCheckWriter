

class Bank:

    def __init__(self, bank_name, address, city, state, zip_code, bank_id=None):
        self.name = bank_name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip_code
        self.bank_id = bank_id


    # bank's toString() method
    def __str__(self):
        return self.name


    # bank object alert message
    def msg_alert(self):
        msg =  'Bank Name: ' + self.name + '\n\n'
        msg += 'Bank Address: ' + self.address + '\n\n'
        msg += 'Bank City: ' + self.city + '\n\n'
        msg += 'Bank State: ' + self.state + '\n\n'
        msg += 'Bank Zip Code: ' + str(self.zip) + '\n\n'

        return msg