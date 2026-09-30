from database.connection import get_connection
from security.password import PINManager


class AuthService:

    MAX_LOGIN_ATTEMPTS = 3

    @staticmethod
    def login(account_number, pin):

        connection = get_connection()

        account = connection.execute("""
            SELECT *
            FROM accounts
            WHERE account_number = ?
        """, (account_number,)).fetchone()

        if account is None:
            connection.close()
            return False, "Account not found.", None

        if account["status"] != "ACTIVE":
            connection.close()
            return False, "Account is not active.", None

        if account["failed_login_attempts"] >= AuthService.MAX_LOGIN_ATTEMPTS:
            connection.close()
            return False, "Account is locked.", None

        valid_pin = PINManager.verify_pin(
            pin,
            account["pin_salt"],
            account["pin_hash"]
        )

        if valid_pin:

            connection.execute("""
                UPDATE accounts
                SET failed_login_attempts = 0
                WHERE account_number = ?
            """, (account_number,))

            connection.commit()
            connection.close()

            return True, "Login successful.", account

        # Wrong PIN
        new_attempts = account["failed_login_attempts"] + 1

        if new_attempts >= AuthService.MAX_LOGIN_ATTEMPTS:

            connection.execute("""
                UPDATE accounts
                SET failed_login_attempts = ?,
                    status = 'LOCKED'
                WHERE account_number = ?
            """, (new_attempts, account_number))

            connection.commit()
            connection.close()

            return False, "Too many failed attempts. Account locked.", None

        connection.execute("""
            UPDATE accounts
            SET failed_login_attempts = ?
            WHERE account_number = ?
        """, (new_attempts, account_number))

        connection.commit()
        connection.close()

        remaining = AuthService.MAX_LOGIN_ATTEMPTS - new_attempts

        return False, f"Invalid PIN. Attempts remaining: {remaining}", None