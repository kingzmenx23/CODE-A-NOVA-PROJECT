import hashlib
import secrets


class PINManager:

    @staticmethod
    def hash_pin(pin):
        salt = secrets.token_bytes(16)

        pin_hash = hashlib.pbkdf2_hmac(
            "sha256",
            pin.encode(),
            salt,
            100_000
        )

        return salt.hex(), pin_hash.hex()

    @staticmethod
    def verify_pin(pin, salt_hex, stored_hash):
        salt = bytes.fromhex(salt_hex)

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            pin.encode(),
            salt,
            100_000
        )

        return secrets.compare_digest(
            new_hash.hex(),
            stored_hash
        )   