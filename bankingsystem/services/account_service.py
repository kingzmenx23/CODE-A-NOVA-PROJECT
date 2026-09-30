from database.connection import get_connection


class AccountService:

    @staticmethod
    def get_balance(account_number):
        connection = get_connection()

        account = connection.execute("""
            SELECT balance
            FROM accounts
            WHERE account_number = ?
        """, (account_number,)).fetchone()

        connection.close()

        if account is None:
            return None

        return account["balance"]