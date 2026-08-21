import os
from datetime import datetime, timedelta
from typing import Any

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from models import User

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY must be set before starting the backend.")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password[:72])


def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(db, email: str, password: str):
    normalized_email = email.strip().lower()
    print(f"LOGIN DEBUG EMAIL: {normalized_email}")
    user = db.query(User).filter(User.email == normalized_email).first()
    print(f"LOGIN DEBUG USER FOUND: {user is not None}")
    if not user:
        return None
    password_verified = verify_password(password, user.hashed_password)
    print(f"LOGIN DEBUG PASSWORD VERIFIED: {password_verified}")
    if not password_verified:
        return None
    return user
