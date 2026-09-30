import secrets
from database.connection import get_connection


class TransactionService:

    @staticmethod
    def deposit(account_number, amount):

        if amount <= 0:
            return False, "Deposit amount must be greater than zero.", None

        connection = get_connection()

        account = connection.execute("""
            SELECT balance, status
            FROM accounts
            WHERE account_number = ?
        """, (account_number,)).fetchone()

        if account is None:
            connection.close()
            return False, "Account not found.", None

        if account["status"] != "ACTIVE":
            connection.close()
            return False, "Account is not active.", None

        new_balance = account["balance"] + amount

        transaction_id = secrets.token_hex(8).upper()

        connection.execute("""
            UPDATE accounts
            SET balance = ?
            WHERE account_number = ?
        """, (new_balance, account_number))

        connection.execute("""
            INSERT INTO transactions (
                transaction_id,
                account_number,
                transaction_type,
                amount
            )
            VALUES (?, ?, ?, ?)
        """, (
            transaction_id,
            account_number,
            "DEPOSIT",
            amount
        ))

        connection.commit()
        connection.close()

        return True, "Deposit successful.", new_balance