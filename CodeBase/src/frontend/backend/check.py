
class Check:

    def __init__(self, check_date, check_num, invoice_num, invoice_date, payee, account_code, check_amount , check_id=None, printed=None, upload_date=None ):
        self.check_date = check_date
        self.check_num = check_num
        self.invoice_num = invoice_num
        self.invoice_date = invoice_date
        self.payee = payee
        self.account_code = account_code
        self.amount = check_amount
        self.upload_date = upload_date
        self.id = check_id
        self.printed = printed


    # method for displaying check information on ListBox
    def __str__(self):
        msg = 'Check Date-- ' + self.check_date 
        msg += ' Check Num-- ' + self.check_num
        msg += ' Invoice Num-- ' + self.invoice_num
        msg += ' Invoice Date-- ' + self.invoice_date
        msg += ' Payee-- ' + self.payee
        msg += ' Account-- ' + self.account_code
        msg += ' Amount-- ' + str(self.amount)

        return msg

    
    def msg_alert(self):
        msg = 'Check Date: ' + self.check_date  + '\n\n'
        msg += ' Check Num: ' + self.check_num + '\n\n'
        msg += ' Invoice Num: ' + self.invoice_num + '\n\n'
        msg += ' Invoice Date: ' + self.invoice_date + '\n\n'
        msg += ' Payee: ' + self.payee + '\n\n'
        msg += ' Account: ' + self.account_code + '\n\n'
        msg += ' Amount: ' + str(self.amount)

        return msg

        
        