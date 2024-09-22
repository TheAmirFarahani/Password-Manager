import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from argon2.low_level import hash_secret_raw, Type  # Import Argon2 low-level functions

class EncryptionManager:
    backend = default_backend()
    key_length = 32  # AES-256 requires 32 bytes

    @staticmethod
    def generate_salt() -> bytes:
        """Generate a random 16-byte salt."""
        return os.urandom(16)

    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        """Derive a key from the master password and salt using Argon2."""
        return hash_secret_raw(
            secret=password.encode(),
            salt=salt,
            time_cost=2,         # Number of iterations
            memory_cost=65536,    # Memory in KB
            parallelism=2,        # Number of threads
            hash_len=EncryptionManager.key_length,
            type=Type.I           # Argon2i variant for password hashing
        )

    @staticmethod
    def encrypt(key: bytes, plaintext: str) -> str:
        """Encrypts the plaintext using AES-GCM and combines all components into a single string."""
        iv = os.urandom(12)  # AES-GCM standard IV size is 12 bytes
        encryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=EncryptionManager.backend
        ).encryptor()

        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()

        # Combine IV, tag, and ciphertext into a single string
        encrypted_data = base64.b64encode(iv + encryptor.tag + ciphertext).decode()
        return encrypted_data

    @staticmethod
    def decrypt(key: bytes, encrypted_data: str) -> str:
        """Decrypts the ciphertext using AES-GCM by extracting parameters from the combined string."""
        # Decode the base64 encoded string
        encrypted_data = base64.b64decode(encrypted_data)

        # Extract IV, tag, and ciphertext
        iv = encrypted_data[:12]
        tag = encrypted_data[12:28]
        ciphertext = encrypted_data[28:]

        decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, tag),
            backend=EncryptionManager.backend
        ).decryptor()

        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode()