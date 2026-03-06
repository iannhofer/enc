from pathlib import Path
import shutil

vaultPath = "/home/inh/IdeaProjects/quantumSafeStorage/testVault"

def createFolder(id):
    newFolder = Path(vaultPath + "/" + id)
    try:
        newFolder.mkdir(parents = True, exist_ok = False)
        print("Folder created")
    except Exception as e:
        print("following error occured: " + e)

def getFolder(id):
    userFolder = vaultPath+"/" + id
    if not userFolder.is_dir():
        createFolder(id)
    return userFolder

def storeFile(userId, file):
    destination = getFolder(userId)
    shutil.move(file, destination)