from cryptography.fernet import Fernet

with open("key.txt", "rb") as file:
    key = file.read()
f = Fernet(key)
with open("../../readme.md.encrypted", "rb") as file:
    encrypted_data = file.read()
decrypted_data = f.decrypt(encrypted_data)
with open("../../readme.md", "wb") as file:
    file.write(decrypted_data)