from dao.loan_repository_impl import LoanRepositoryImpl
from entity.customer import Customer
from entity.home_loan import HomeLoan
from entity.car_loan import CarLoan

def main():
    service = LoanRepositoryImpl()

    while True:
        print("\n====== Loan Management System ======")
        print("1. Apply Loan")
        print("2. Calculate Interest")
        print("3. Loan Status")
        print("4. Calculate EMI")
        print("5. Loan Repayment")
        print("6. Get All Loans")
        print("7. Get Loan by ID")
        print("8. Exit")
        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            customer = Customer(customer_id=int(input("Enter Customer ID: ")))
            loan_type = input("Enter Loan Type (HomeLoan/CarLoan): ").strip()

            principal = float(input("Enter Principal Amount: "))
            rate = float(input("Enter Interest Rate: "))
            term = int(input("Enter Loan Term (in months): "))

            if loan_type.lower() == 'homeloan':
                prop_addr = input("Enter Property Address: ")
                prop_val = int(input("Enter Property Value: "))
                loan = HomeLoan(customer=customer, principal_amount=principal,
                                interest_rate=rate, loan_term=term, loan_status='Pending',
                                property_address=prop_addr, property_value=prop_val)
            elif loan_type.lower() == 'carloan':
                car_model = input("Enter Car Model: ")
                car_val = int(input("Enter Car Value: "))
                loan = CarLoan(customer=customer, principal_amount=principal,
                               interest_rate=rate, loan_term=term, loan_status='Pending',
                               car_model=car_model, car_value=car_val)
            else:
                print(" Invalid Loan Type!")
                continue

            service.apply_loan(loan)

        elif choice == '2':
            sub_choice = input("1. By Loan ID\n2. By Manual Entry\nChoose: ")
            if sub_choice == '1':
                loan_id = int(input("Enter Loan ID: "))
                service.calculate_interest(loan_id)
            elif sub_choice == '2':
                principal = float(input("Enter Principal Amount: "))
                rate = float(input("Enter Interest Rate: "))
                term = int(input("Enter Loan Term (in months): "))
                service.calculate_interest_with_params(principal, rate, term)

        elif choice == '3':
            loan_id = int(input("Enter Loan ID to check and update status: "))
            service.loan_status(loan_id)

        elif choice == '4':
            sub_choice = input("1. By Loan ID\n2. By Manual Entry\nChoose: ")
            if sub_choice == '1':
                loan_id = int(input("Enter Loan ID: "))
                service.calculate_emi(loan_id)
            elif sub_choice == '2':
                principal = float(input("Enter Principal Amount: "))
                rate = float(input("Enter Interest Rate: "))
                term = int(input("Enter Loan Term (in months): "))
                service.calculate_emi_with_params(principal, rate, term)

        elif choice == '5':
            loan_id = int(input("Enter Loan ID: "))
            amount = float(input("Enter repayment amount: "))
            service.loan_repayment(loan_id, amount)

        elif choice == '6':
            service.get_all_loan()

        elif choice == '7':
            loan_id = int(input("Enter Loan ID: "))
            service.get_loan_by_id(loan_id)

        elif choice == '8':
            print("Exiting Loan Management System. Goodbye!")
            break
        else:
            print(" Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
