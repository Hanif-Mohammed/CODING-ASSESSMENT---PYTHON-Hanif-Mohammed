class InvalidLoanException(Exception):
    def __init__(self, message="Invalid Loan! Please check the loan ID or data."):
        super().__init__(message)
