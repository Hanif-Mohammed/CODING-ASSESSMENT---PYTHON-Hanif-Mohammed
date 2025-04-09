import pymysql
from dao.iloan_repository import ILoanRepository
from util.db_conn_util import DBConnUtil
from entity.home_loan import HomeLoan
from entity.car_loan import CarLoan
from exception.invalid_loan_exception import InvalidLoanException

class LoanRepositoryImpl(ILoanRepository):

    def __init__(self):
        self.conn = DBConnUtil.get_connection('db.properties')

    def apply_loan(self, loan):
        try:
            cursor = self.conn.cursor()

            confirm = input("Do you want to proceed with applying the loan? (Yes/No): ").strip().lower()
            if confirm != 'yes':
                print("Loan application cancelled.")
                return

            insert_loan_sql = """
                INSERT INTO loan (customer_id, principal_amount, interest_rate, loan_term, loan_type, loan_status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            loan_data = (
                loan.customer.customer_id,
                loan.principal_amount,
                loan.interest_rate,
                loan.loan_term,
                loan.loan_type,
                loan.loan_status
            )
            cursor.execute(insert_loan_sql, loan_data)
            self.conn.commit()

            loan_id = cursor.lastrowid
            loan.loan_id = loan_id

            if isinstance(loan, HomeLoan):
                cursor.execute("""
                    INSERT INTO home_loan (loan_id, property_address, property_value)
                    VALUES (%s, %s, %s)
                """, (loan_id, loan.property_address, loan.property_value))
            elif isinstance(loan, CarLoan):
                cursor.execute("""
                    INSERT INTO car_loan (loan_id, car_model, car_value)
                    VALUES (%s, %s, %s)
                """, (loan_id, loan.car_model, loan.car_value))

            self.conn.commit()
            print(f"Loan applied successfully. Loan ID: {loan_id}")

        except Exception as e:
            print("Error in apply_loan:", e)
            self.conn.rollback()

    def calculate_interest(self, loan_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT principal_amount, interest_rate, loan_term FROM loan WHERE loan_id = %s", (loan_id,))
            result = cursor.fetchone()

            if result:
                principal, rate, term = result
                interest = (principal * rate * term) / 12
                print(f"Calculated Interest for Loan ID {loan_id}: ₹{interest:.2f}")
                return interest
            else:
                raise InvalidLoanException(f"Loan with ID {loan_id} not found.")

        except InvalidLoanException as e:
            print("Invalid", e)
        except Exception as e:
            print("Error calculating interest:", e)

    def calculate_interest_with_params(self, principal_amount, interest_rate, loan_term):
        try:
            interest = (principal_amount * interest_rate * loan_term) / 12
            print(f"Calculated Interest (manual): ₹{interest:.2f}")
            return interest
        except Exception as e:
            print("Error calculating interest with parameters:", e)

    def loan_status(self, loan_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT c.credit_score FROM loan l
                JOIN customer c ON l.customer_id = c.customer_id
                WHERE l.loan_id = %s
            """, (loan_id,))
            result = cursor.fetchone()

            if result:
                credit_score = result[0]
                new_status = 'Approved' if credit_score > 650 else 'Rejected'

                cursor.execute("UPDATE loan SET loan_status = %s WHERE loan_id = %s", (new_status, loan_id))
                self.conn.commit()

                print(f"Loan ID {loan_id} has been {new_status.lower()} based on credit score {credit_score}.")
            else:
                raise InvalidLoanException(f"Loan with ID {loan_id} not found.")

        except InvalidLoanException as e:
            print("Invalid", e)
        except Exception as e:
            print("Error updating loan status:", e)

    def calculate_emi(self, loan_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT principal_amount, interest_rate, loan_term FROM loan WHERE loan_id = %s", (loan_id,))
            result = cursor.fetchone()

            if result:
                P, annual_rate, N = result
                R = annual_rate / 12 / 100
                EMI = (P * R * (1 + R)**N) / ((1 + R)**N - 1)
                print(f"Calculated EMI for Loan ID {loan_id}: ₹{EMI:.2f}")
                return EMI
            else:
                raise InvalidLoanException(f"Loan with ID {loan_id} not found.")

        except InvalidLoanException as e:
            print("Invalid", e)
        except Exception as e:
            print("Error calculating EMI:", e)

    def calculate_emi_with_params(self, principal_amount, interest_rate, loan_term):
        try:
            R = interest_rate / 12 / 100
            N = loan_term
            EMI = (principal_amount * R * (1 + R)**N) / ((1 + R)**N - 1)
            print(f"Calculated EMI (manual): ₹{EMI:.2f}")
            return EMI
        except Exception as e:
            print("Error calculating EMI with parameters:", e)

    def loan_repayment(self, loan_id, amount):
        try:
            emi = self.calculate_emi(loan_id)
            if emi is None:
                return

            emi = float(emi)

            if amount < emi:
                print("Payment amount is less than a single EMI. Payment rejected.")
                return

            num_emis_paid = int(amount // emi)
            remaining_amount = amount % emi
            print(f" You can pay {num_emis_paid} EMI(s) with ₹{amount}. Remaining: ₹{remaining_amount:.2f}")

        except Exception as e:
            print("Error processing loan repayment:", e)

    def get_all_loan(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM loan")
            results = cursor.fetchall()

            if results:
                for row in results:
                    print(row)
            else:
                print("No loans found.")

        except Exception as e:
            print("Error fetching all loans:", e)

    def get_loan_by_id(self, loan_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM loan WHERE loan_id = %s", (loan_id,))
            result = cursor.fetchone()

            if result:
                print("Loan Details:", result)
                return result
            else:
                raise InvalidLoanException(f"Loan with ID {loan_id} not found.")

        except InvalidLoanException as e:
            print("Invalid", e)
        except Exception as e:
            print("Error fetching loan by ID:", e)
