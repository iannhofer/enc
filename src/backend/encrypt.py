from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv


load_dotenv()


def loadKey():
    keyPath = os.getenv("ENCRYPTION_KEY_PATH", "src/backend/key.txt")
    with open(keyPath, "rb") as file:
        key = file.read()
    if not key:
        key = Fernet.generate_key()
        with open(keyPath, "wb") as file:
            file.write(key)
    return key


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
