from pathlib import Path
import shutil
import os
from dotenv import load_dotenv

load_dotenv()

vaultPath = os.getenv("VAULT_PATH", "vault")
vaultPath = Path(vaultPath).resolve()

def createFolder(id):
    newFolder = vaultPath / str(id)
    try:
        newFolder.mkdir(parents = True, exist_ok = False)
        print("Folder created")
    except Exception as e:
        print("following error occured: " + str(e))

def getFolder(id):
    userFolder = vaultPath / str(id)
    if not userFolder.is_dir():
        createFolder(id)
    return userFolder

def deleteFolder(id):
    folder = getFolder(id)
    shutil.rmtree(folder)

def storeFile(userId, file):
    destination = getFolder(userId)
    shutil.move(file, destination)