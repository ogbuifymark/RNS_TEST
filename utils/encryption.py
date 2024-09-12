from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from os import urandom
import base64

# Function to generate a new AES key for encryption
def generate_key():
    return urandom(32)  # Generates a 256-bit key

# Function to encrypt the file data
def encrypt_file(key, file_data):
    iv = urandom(16)  # Generates a 128-bit IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(file_data) + encryptor.finalize()
    return iv + encrypted_data  # Prepend IV to encrypted data for decryption purposes

