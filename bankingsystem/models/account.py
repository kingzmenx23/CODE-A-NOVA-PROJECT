from datetime import datetime


class BankAccount:

    def __init__(
        self,
        account_number,
        name,
        phone,
        pin_salt,
        pin_hash,
        balance=0.0
    ):
        self.account_number = account_number
        self.name = name
        self.phone = phone
        self.pin_hash = pin_hash
        self.pin_salt = pin_salt
        self._balance = balance
        self._phone_verified = False
        self._status = "ACTIVE"
        self.created_at = datetime.now()

    @property
    def balance(self):
        return self._balance

    @property
    def phone_verified(self):
        return self._phone_verified

    @property
    def status(self):
        return self._status

    def verify_phone(self):
        self._phone_verified = True

    def deposit(self, amount):
        if self._status != "ACTIVE":
            raise ValueError("Account is not active.")

        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")

        self._balance += amount

    def withdraw(self, amount):
        if self._status != "ACTIVE":
            raise ValueError("Account is not active.")

        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")

        if amount > self._balance:
            raise ValueError("Insufficient balance.")

        self._balance -= amount

    def deactivate(self):
        self._status = "INACTIVE"