import secrets
import time


class OTPService:

    def __init__(self):
        self.otp = None
        self.expires_at = None
        self.attempts = 0
        self.max_attempts = 3

    def generate_otp(self):
        self.otp = str(secrets.randbelow(9000) + 1000)
        self.expires_at = time.time() + 120
        self.attempts = 0 

        return self.otp

    def verify_otp(self, entered_otp):

        if self.otp is None:
            return False, "No OTP has been generated."

        if time.time() > self.expires_at:
            return False, "OTP has expired."

        if self.attempts >= self.max_attempts:
            return False, "Maximum OTP attempts exceeded."

        self.attempts += 1

        if entered_otp == self.otp:
            self.otp = None
            return True, "Phone verified successfully."

        remaining = self.max_attempts - self.attempts

        return False, f"Invalid OTP. Attempts remaining: {remaining}"