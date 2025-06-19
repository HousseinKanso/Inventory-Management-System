from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from .database import SessionLocal, init_db
from .models import User

from starlette.responses import Response

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.on_event("startup")
def on_startup():
    init_db()

@router.get("/signup")
def signup_get(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "error": None})

@router.post("/signup")
def signup_post(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=username).first():
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Username already exists."})
    hashed_password = bcrypt.hash(password)
    user = User(username=username, hashed_password=hashed_password, role='viewer')
    db.add(user)
    db.commit()
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return response

@router.get("/login")
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@router.post("/login")
def login_post(request: Request, response: Response, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user or not bcrypt.verify(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials."})
    request.session["user"] = user.username
    request.session["role"] = user.role
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND) 