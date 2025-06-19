from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from . import auth, inventory, chatbot
import os
from fastapi.responses import RedirectResponse

app = FastAPI()

# Secret key for session
app.add_middleware(SessionMiddleware, secret_key='supersecretkey')

# Mount static files
app.mount('/static', StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'static')), name='static')

# Routers
app.include_router(auth.router)
app.include_router(inventory.router)
app.include_router(chatbot.router)

@app.get("/")
def root():
    return RedirectResponse(url="/login") 