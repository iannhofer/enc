from cryptography.fernet import Fernet

def load_key():
    with open("key.txt", "rb") as file:
        key = file.read()
    if not key:
        key = Fernet.generate_key()
        with open("key.txt", "wb") as file:
            file.write(key)
    return key


def encrypt(file_path, destination_path):
    key = load_key()
    f = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(destination_path+".ecnrypted", "wb") as file:
        file.write(encrypted_data)
    return destination_path
