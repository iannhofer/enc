from cryptography.fernet import Fernet

from src.backend.encrypt import load_key


def decrypt(file_path, destination_path):
    key = load_key()
    f = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(destination_path, "wb") as file:
        file.write(decrypted_data)
    return destination_path

