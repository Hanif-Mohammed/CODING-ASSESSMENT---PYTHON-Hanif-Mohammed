class Customer:
    def __init__(self, customer_id=None, name='', email_address='', phone_number='', address='', credit_score=0):
        self.customer_id = customer_id
        self.name = name
        self.email_address = email_address
        self.phone_number = phone_number
        self.address = address
        self.credit_score = credit_score

    def __str__(self):
        return f"Customer[ID={self.customer_id}, Name={self.name}, Email={self.email_address}, " \
               f"Phone={self.phone_number}, Address={self.address}, CreditScore={self.credit_score}]"
