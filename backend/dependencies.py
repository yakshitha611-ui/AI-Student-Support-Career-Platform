from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from auth import SECRET_KEY, ALGORITHM
from database import SessionLocal
from models import User

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials.",
        )

    subject = payload.get("sub")
    user: User | None = None

    if subject is not None:
        subject_value = str(subject).strip()
        if "@" in subject_value:
            user = db.query(User).filter(User.email == subject_value.lower()).first()
        else:
            try:
                user = db.query(User).filter(User.id == int(subject_value)).first()
            except ValueError:
                user = None

    if user is None:
        email = payload.get("email")
        if email is not None:
            user = db.query(User).filter(User.email == str(email).strip().lower()).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )
    return user
