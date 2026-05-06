from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv


load_dotenv()


def loadKey():
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise NotImplementedError("no encryption key")
    return key.encode()


def encrypt(file_path):
    key = loadKey()
    f = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    result = file_path + ".encrypted"
    with open(result, "wb") as file:
        file.write(encrypted_data)
    return result
