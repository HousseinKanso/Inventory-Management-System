from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import InventoryItem, StatusEnum
from starlette.responses import Response

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def require_login(request: Request):
    if not request.session.get("user"):
        return False
    return True

def require_admin(request: Request):
    return request.session.get("role") == "admin"

@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    if not require_login(request):
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    items = db.query(InventoryItem).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "items": items, "role": request.session.get("role")})

@router.get("/add")
def add_get(request: Request):
    if not require_login(request) or not require_admin(request):
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("add.html", {"request": request, "statuses": [e.value for e in StatusEnum]})

@router.post("/add")
def add_post(request: Request, name: str = Form(...), quantity: int = Form(...), category: str = Form(...), status: str = Form(...), db: Session = Depends(get_db)):
    if not require_login(request) or not require_admin(request):
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    item = InventoryItem(name=name, quantity=quantity, category=category, status=StatusEnum(status))
    db.add(item)
    db.commit()
    # Render add.html with a success message and empty form
    return templates.TemplateResponse(
        "add.html",
        {
            "request": request,
            "statuses": [e.value for e in StatusEnum],
            "success": "Item successfully added!"
        }
    )

@router.get("/edit/{item_id}")
def edit_get(request: Request, item_id: int, db: Session = Depends(get_db)):
    if not require_login(request) or not require_admin(request):
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    item = db.query(InventoryItem).filter_by(id=item_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "item": item, "statuses": [e.value for e in StatusEnum]})

@router.post("/edit/{item_id}")
def edit_post(request: Request, item_id: int, name: str = Form(...), quantity: int = Form(...), category: str = Form(...), status: str = Form(...), db: Session = Depends(get_db)):
    if not require_login(request) or not require_admin(request):
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    item = db.query(InventoryItem).filter_by(id=item_id).first()
    item.name = name
    item.quantity = quantity
    item.category = category
    item.status = StatusEnum(status)
    db.commit()
    # Render edit.html with a success message
    return templates.TemplateResponse(
        "edit.html",
        {
            "request": request,
            "item": item,
            "statuses": [e.value for e in StatusEnum],
            "success": "Changes applied."
        }
    )

@router.get("/delete/{item_id}")
def delete_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    if not require_login(request) or not require_admin(request):
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    item = db.query(InventoryItem).filter_by(id=item_id).first()
    db.delete(item)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@router.get("/search")
def search(request: Request, name: str = "", category: str = "", status: str = "", db: Session = Depends(get_db)):
    if not require_login(request):
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    query = db.query(InventoryItem)
    if name:
        query = query.filter(InventoryItem.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(InventoryItem.category == category)
    if status:
        query = query.filter(InventoryItem.status == StatusEnum(status))
    items = query.all()
    return templates.TemplateResponse("search.html", {"request": request, "items": items, "role": request.session.get("role")}) 