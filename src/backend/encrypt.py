from cryptography.fernet import Fernet


key = Fernet.generate_key()
f = Fernet(key)
with open("key.txt", "wb") as file:
    file.write(key)
filename = input("Enter file path")
with open(filename, "rb") as file:
    file_data = file.read()
encrypted_data = f.encrypt(file_data)
with open(filename + ".encrypted", "wb") as file:
    file.write(encrypted_data)
