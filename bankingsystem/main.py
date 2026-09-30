from models.account import BankAccount
from security.otp import OTPService
from security.password import PINManager
from database.schema import create_tables
from database.account_repository import AccountRepository
from security.auth_service import AuthService
from services.account_service import AccountService
from services.transaction_service import TransactionService

def create_account():
    print("\n===== CREATE ACCOUNT =====")

    name = input("Enter your name: ").strip()
    phone = input("Enter your phone number: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    if not phone.isdigit() or len(phone) != 10:
        print("Please enter a valid 10-digit phone number.")
        return

    otp_service = OTPService()

    otp = otp_service.generate_otp()

    print(f"\n[DEMO] OTP sent to ******{phone[-4:]}")
    print(f"[DEMO] Your OTP is: {otp}")

    entered_otp = input("Enter OTP: ").strip()

    verified, message = otp_service.verify_otp(entered_otp)

    print(message)

    if not verified:
        return

    pin = input("Create a 4-digit PIN: ").strip()

    if not pin.isdigit() or len(pin) != 4:
        print("PIN must contain exactly 4 digits.")
        return

    initial_deposit = input("Enter initial deposit: ").strip()

    try:
        initial_deposit = float(initial_deposit)

        if initial_deposit < 0:
            print("Initial deposit cannot be negative.")
            return

    except ValueError:
        print("Please enter a valid amount.")
        return

    account_number = AccountRepository.generate_account_number()

    salt, pin_hash = PINManager.hash_pin(pin)

    account = BankAccount(
        account_number=account_number,
        name=name,
        phone=phone,
        pin_salt=salt,
        pin_hash=pin_hash,
        balance=initial_deposit
    )

    AccountRepository.save_account(account)

    print("\nAccount created successfully!")
    print(f"Account Number: {account.account_number}")
    print(f"Name: {account.name}")
    print(f"Balance: ₹{account.balance:.2f}")

def account_menu(account):
    while True:
        print("\n================================")
        print("          ACCOUNT MENU")
        print("================================")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            balance = AccountService.get_balance(
                account["account_number"]
            )

            print(f"\nCurrent Balance: ₹{balance:.2f}")
        
        elif choice == "2":
            print("\n===== DEPOSIT =====")

            amount = input("Enter deposit amount: ").strip()

            try:
                amount = float(amount)
            except ValueError:
                print("Please enter a valid amount.")
            continue

            success, message, new_balance = TransactionService.deposit(
                account["account_number"],
                amount
                )

    print(message)

    if success:
        print(f"New Balance: ₹{new_balance:.2f}")

    elif choice == "7":
            print("\nLogged out successfully.")
            break

    else:
            print("\nThis feature is coming next.")

def login():
    print("\n===== LOGIN =====")

    account_number = input("Enter account number: ").strip()
    pin = input("Enter PIN: ").strip()

    success, message, account = AuthService.login(
        account_number,
        pin
    )

    print(message)

    if not success:
        return

    print(f"\nWelcome, {account['name']}!")

    account_menu(account)


def main():
    while True:
        print("\n================================")
        print("       SECURE BANKING SYSTEM")
        print("================================")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_account()

        elif choice == "2":
            login()

        elif choice == "3":
            print("Thank you for using our banking system.")
            break

        else:
            print("Invalid choice. Please try again with 1, 2, or 3.")


if __name__ == "__main__":
    create_tables()
    main()