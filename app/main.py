from fastapi import FastAPI, Request
from app.database import engine, Base
from app import models, auth, todos, admin
from fastapi.templating import Jinja2Templates
import os
from datetime import datetime

app = FastAPI(
    title="Todo API",
    description="A simple Todo API with authentication",
    version="1.0.0"
)

# Setup Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(todos.router)  # Router has prefix="/todos"
app.include_router(admin.router)  # Router has prefix="/admin"

@app.get("/")
async def home(request: Request):
    """Render the home page"""
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )

@app.get("/login")
async def login_page(request: Request, error: str = None, success: str = None):
    """Render the login page"""
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": error,
            "success": success
        }
    )

# ✅ ADD THIS NEW ROUTE for Register page
@app.get("/register")
async def register_page(request: Request, error: str = None):
    """Render the registration page"""
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "error": error
        }
    )

@app.get("/dashboard")
async def dashboard_page(request: Request):
    """Render the dashboard page"""
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )

@app.get("/todos")
async def todos_page(request: Request):
    """Render the todo management page"""
    return templates.TemplateResponse(
        "todos.html",
        {"request": request}
    )

@app.get("/ping")
async def ping():
    return {"ping": "pong!"}

@app.get("/api")
async def api_root():
    return {
        "message": "Welcome to Todo API",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0"
    }