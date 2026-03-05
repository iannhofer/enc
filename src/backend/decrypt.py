from cryptography.fernet import Fernet

with open("key.txt", "rb") as file:
    key = file.read()
f = Fernet(key)
filename = input("Enter file path")
with open(filename, "rb") as file:
    encrypted_data = file.read()
decrypted_data = f.decrypt(encrypted_data)
with open(filename, "wb") as file:
    file.write(decrypted_data)