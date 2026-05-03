from pathlib import Path
import shutil

vaultPath = "/home/inh/IdeaProjects/quantumSafeStorage/testVault"

def createFolder(id):
    newFolder = Path(vaultPath + "/" + str(id))
    try:
        newFolder.mkdir(parents = True, exist_ok = False)
        print("Folder created")
    except Exception as e:
        print("following error occured: " + str(e))

def getFolder(id):
    userFolder = Path(vaultPath+"/" + str(id))
    if not userFolder.is_dir():
        createFolder(id)
    return userFolder

def storeFile(userId, file):
    destination = getFolder(userId)
    shutil.move(file, destination)