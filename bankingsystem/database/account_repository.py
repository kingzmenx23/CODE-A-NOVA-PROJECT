from database.connection import get_connection


class AccountRepository:

    @staticmethod
    def generate_account_number():
        connection = get_connection()

        row = connection.execute("""
            SELECT MAX(CAST(account_number AS INTEGER)) AS last_account
            FROM accounts
        """).fetchone()

        connection.close()

        if row["last_account"] is None:
            return "100001"

        return str(row["last_account"] + 1)

    @staticmethod
    def save_account(account):
        connection = get_connection()

        connection.execute("""
            INSERT INTO accounts (
                account_number,
                name,
                phone,
                phone_verified,
                pin_salt,
                pin_hash,
                balance,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            account.account_number,
            account.name,
            account.phone,
            int(account.phone_verified),
            account.pin_salt,
            account.pin_hash,
            account.balance,
            account.status
        ))

        connection.commit()
        connection.close()