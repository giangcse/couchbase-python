from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.services.book_service import get_books
from app.services.user_service import authenticate_user
from app.core import security
from app.core.security import verify_token
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.utils import get_current_user

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
templates = Jinja2Templates(directory="templates")

async def get_current_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        user = verify_token(token)
        return user
    except HTTPException:
        return None

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    user = await get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    books = await get_books()
    return templates.TemplateResponse("index.html", {"request": request, "books": books})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    user = await get_current_user_from_cookie(request)
    if user:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request})