import os
from fastapi import FastAPI, Form, Request, Response, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from src.backend.database import authenticateUser, createUser, getUserFiles

app = FastAPI()

frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
templates = Jinja2Templates(directory=frontend_dir)

@app.get("/", response_class = HTMLResponse)
def read_root():
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