import os
import shutil
from fastapi import FastAPI, Form, Request, Response, Cookie, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from src.backend.database import authenticateUser, createUser, getUserFiles, addFile, deleteUserDB
from src.backend.fileManager import vaultPath, deleteFolder

app = FastAPI()

frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
templates = Jinja2Templates(directory=frontend_dir)

@app.get("/", response_class = HTMLResponse)
def readRoot():
    index_path = os.path.join(frontend_dir, "index.html")
    with open(index_path, "r") as file:
        return file.read()

@app.get("/dashboard", response_class = HTMLResponse)
def dashboard(request: Request, user_id: str | None = Cookie(None)):
    if not user_id:
        return RedirectResponse(url="/", status_code = 303)
    files = getUserFiles(user_id)
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"files": files}
    )


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), action: str = Form("login")):
    if action == "register":
        user = createUser(username, password)
        if not user:
            return Response(content="Username already exists", status_code=400)
    else:
        user = authenticateUser(username, password)
        if not user:
            return Response(content="Invalid username or password", status_code=400)

    user_id = user[0]
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="user_id", value=str(user_id))
    return response

@app.post("/upload")
def uploadFile(userId: str | None = Cookie(None, alias="user_id"), file: UploadFile = File(...)):
    if not userId: return RedirectResponse(url="/")
    encFileName=f"{file.filename}.encrypted"
    addFile(userId, file.filename)
    from src.backend.fileManager import getFolder
    userVault = getFolder(userId)
    finalPath = os.path.join(userVault, encFileName)
    with open(finalPath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/download/{filename}")
def downloadFile(filename: str, userId: str | None = Cookie(None, alias="user_id")):
    if not userId:
        return RedirectResponse(url="/")
    userFiles = getUserFiles(userId)
    if filename not in userFiles:
        return Response(content="file not found", status_code=404)
    encryptedFilename = f"{filename}.encrypted"
    encryptedFilepath = os.path.join(vaultPath, str(userId), encryptedFilename)
    if not os.path.exists(encryptedFilepath):
        return Response(content="file not found", status_code=404)
    return FileResponse(path = encryptedFilepath, filename = encryptedFilename, media_type = "application/octet-stream")

@app.delete("/deleteUser/{userId}")
def deleteUser(userId: str):
    deleteFolder(userId)
    deleteUserDB(userId)
    return RedirectResponse(url="/", status_code=303)