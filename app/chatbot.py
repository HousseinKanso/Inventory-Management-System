import os
from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import Response
from dotenv import load_dotenv
import openai

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

HELP_GUIDE_PATH = os.path.join(os.path.dirname(__file__), "help_guide.txt")

# Dependency to enforce viewer role
def require_viewer(request: Request):
    return request.session.get("user") and request.session.get("role") == "viewer"

@router.get("/chat")
def chat_get(request: Request):
    if not require_viewer(request):
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("chat.html", {"request": request})

@router.post("/chat")
def chat_post(request: Request, question: str = Form(...)):
    if not require_viewer(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=403)
    # Load help guide context
    with open(HELP_GUIDE_PATH, "r", encoding="utf-8") as f:
        help_guide = f.read()
    prompt = f"Help Guide:\n{help_guide}\n\nUser Question: {question}\nAI Assistant:"  # RAG-style prompt
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": help_guide}, {"role": "user", "content": question}],
            max_tokens=256,
            temperature=0.2,
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"[Error: {str(e)}]"
    return JSONResponse({"answer": answer}) 