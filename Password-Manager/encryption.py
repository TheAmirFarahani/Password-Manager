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
    def encrypt(key: bytes, plaintext: str) -> dict:
        """Encrypts the plaintext using AES-GCM."""
        iv = os.urandom(12)  # AES-GCM standard IV size is 12 bytes
        encryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=EncryptionManager.backend
        ).encryptor()

        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()

        return {
            'ciphertext': base64.b64encode(ciphertext).decode(),
            'iv': base64.b64encode(iv).decode(),
            'tag': base64.b64encode(encryptor.tag).decode()
        }
    @staticmethod
    def decrypt(key: bytes, cipher: dict) -> str:
        """Decrypts the ciphertext using AES-GCM by extracting parameters from the cipher dictionary."""
        iv = base64.b64decode(cipher['iv'])
        tag = base64.b64decode(cipher['tag'])
        ciphertext = base64.b64decode(cipher['ciphertext'])
        
        decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, tag),
            backend=EncryptionManager.backend
        ).decryptor()

        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode()