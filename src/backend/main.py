from src.backend import encrypt, decrypt
from src.backend.fileManager import getFolder
from src.backend.login import logIn


def main():
    user = logIn()
    if not user:
        print("auth failed")
        return
    userFolder = getFolder(user[0])
    print("your current file: " + userFolder)
    print("upload new (u) or decrypt existing (d) file?: ")
    choice = input()
    if choice == "u":
        fileToEncrypt = input("enter filepath: ")
        encryptedFile = encrypt(fileToEncrypt)
    elif choice =="d":
        fileToDecrypt = input("enter filepath: ")
        decryptedFile = decrypt(fileToDecrypt)