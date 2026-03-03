"""Auth endpoints."""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, decode_token, hash_password, verify_password
from app.database import get_db
from app.models.token import RefreshToken
from app.models.user import User
from app.schemas.common import LoginRequest, TokenPair, UserRead, UserRegister
from app.utils.rate_limiter import check_login_rate_limit

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=201)
def register(payload: UserRegister, db: Session = Depends(get_db)) -> User:
    exists = db.query(User).filter((User.username == payload.username) | (User.email == payload.email)).first()
    if exists:
        raise HTTPException(status_code=422, detail="User already exists")
    user = User(username=payload.username, email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)) -> TokenPair:
    check_login_rate_limit(request.client.host if request.client else "unknown")
    user = db.query(User).filter((User.username == payload.login) | (User.email == payload.login)).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    db.add(RefreshToken(user_id=user.id, token=refresh, expires_at=datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=settings.refresh_token_days)))
    db.commit()
    return TokenPair(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenPair)
def refresh_tokens(payload: dict, db: Session = Depends(get_db)) -> TokenPair:
    token = payload.get("refresh_token")
    if not token:
        raise HTTPException(status_code=422, detail="refresh_token is required")
    decode = decode_token(token, "refresh")
    stored = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if not stored:
        raise HTTPException(status_code=401, detail="Refresh token revoked")

    db.delete(stored)
    user_id = int(decode["sub"])
    access = create_access_token(user_id)
    refresh = create_refresh_token(user_id)
    db.add(RefreshToken(user_id=user_id, token=refresh, expires_at=datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=settings.refresh_token_days)))
    db.commit()
    return TokenPair(access_token=access, refresh_token=refresh)
