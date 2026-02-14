"""JWT authentication utilities using stdlib only (HS256)."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time
from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..models import SessionLocal
from ..models.users import User

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-production")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Password hashing (salted SHA-256, no native deps) ---

def hash_password(password: str) -> str:
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}${hashed}"


def verify_password(plain: str, hashed: str) -> bool:
    parts = hashed.split("$", 1)
    if len(parts) != 2:
        return False
    salt, stored_hash = parts
    computed = hashlib.sha256(f"{salt}{plain}".encode()).hexdigest()
    return hmac.compare_digest(computed, stored_hash)


# --- Minimal HS256 JWT (no external library) ---

def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64url_decode(s: str) -> bytes:
    s += "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    header = _b64url_encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    payload = data.copy()
    exp = time.time() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).total_seconds()
    payload["exp"] = int(exp)
    body = _b64url_encode(json.dumps(payload).encode())
    sig_input = f"{header}.{body}".encode()
    signature = _b64url_encode(hmac.new(SECRET_KEY.encode(), sig_input, hashlib.sha256).digest())
    return f"{header}.{body}.{signature}"


def _decode_token(token: str) -> dict:
    """Decode and verify an HS256 JWT. Raises ValueError on failure."""
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Bad token")
    header_b, body_b, sig_b = parts
    sig_input = f"{header_b}.{body_b}".encode()
    expected = hmac.new(SECRET_KEY.encode(), sig_input, hashlib.sha256).digest()
    actual = _b64url_decode(sig_b)
    if not hmac.compare_digest(expected, actual):
        raise ValueError("Invalid signature")
    payload = json.loads(_b64url_decode(body_b))
    if payload.get("exp", 0) < time.time():
        raise ValueError("Token expired")
    return payload


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Decode JWT and return the authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = _decode_token(token)
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except ValueError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
