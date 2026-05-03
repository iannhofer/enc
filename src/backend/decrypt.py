from pathlib import Path

from cryptography.fernet import Fernet

from src.backend.encrypt import loadKey


def decrypt(file_path, destination_path):
    key = loadKey()
    f = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    destination_path = Path(destination_path)
    with open(destination_path.rename(destination_path.stem), "wb") as file:
        file.write(decrypted_data)
    return destination_path

