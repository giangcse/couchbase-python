from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from starlette.responses import RedirectResponse
from app.core import security
from app.core.config import settings
from app.schemas.user import UserCreate, UserInDB
from app.services.user_service import authenticate_user, create_user

router = APIRouter()


@router.post("/register", response_model=UserInDB)
async def register_user(user: UserCreate):
    db_user = await create_user(user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return db_user


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        "Authorization",
        value=f"{access_token}",
        httponly=False,
        max_age=3600 * 3,
        expires=3600 * 3,
        samesite=None,
        secure=False,
    )
    return response
