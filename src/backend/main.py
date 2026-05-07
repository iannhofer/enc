import os
import shutil
from fastapi import FastAPI, Form, Request, Response, Cookie, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from src.backend.database import authenticateUser, createUser, getUserFiles, addFile
from src.backend.fileManager import storeFile
from src.backend.encrypt import encrypt

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
        "dashboard.html",
        {"request": request, "files": files}
    )


@app.post("/login")
def login(username:str=Form(...), password: str = Form(...)):
    user = authenticateUser(username, password)


    if not user:
        user = createUser(username, password)

    if user:
        user_id = user[0]
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="user_id", value=str(user_id))
        return response
    
    return Response(content="Fehler beim Login/Registrieren", status_code=400)

@app.post("/upload")
def uploadFile(userId: str | None= Cookie(None),file: UploadFile = File(...)):
    if not userId: return RedirectResponse(url="/")
    tmpPath=f"temp_{file.filename}"
    with open(tmpPath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    encTmpPath = encrypt(tmpPath)
    storeFile(userId, encTmpPath)
    addFile(userId, file.filename)
    os.remove(tmpPath)
    return RedirectResponse(url="/dashboard", status_code=303)
