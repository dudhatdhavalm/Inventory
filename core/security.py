from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from typing import Optional
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer
from jose import jwt
from core.config import settings
from fastapi.requests import Request
from sqlalchemy.orm import Session
from models.user import User
from schemas.auth import RegisterSchema

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

reusable_oauth2 = HTTPBearer(scheme_name="Authorization")
PREFIX = "Bearer"


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_context.hash(password)


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).all()


def create_user(db: Session, register_schema: RegisterSchema):
    password_hash = get_password_hash(register_schema.password)
    expiry_date = datetime.now() + timedelta(90)
    user = User(
        first_name=(register_schema.first_name),
        last_name=(register_schema.last_name),
        password=password_hash,
        email=(register_schema.email),
        phone=(register_schema.phone),
        gender=(register_schema.gender),
        expiry_date=expiry_date,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_access_token(claim: dict, expires_delta: Optional[timedelta] = None):
    to_encode = claim.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return jwt_token


def get_user_by_email_active(db: Session, email: str):
    return db.query(User).filter(User.email == email).all()


def decode_access_token(token):
    payload = None
    try:
        auth_token = get_token(token)
        payload = jwt.decode(auth_token, settings.SECRET_KEY, settings.ALGORITHM)
    except Exception as e:
        print("Problem with token decode => ", str(e))
    return payload


def is_unauthorized_url(request: Request):
    allow_urls = [
        "/docs",
        "/openapi.json",
        "/auth/login",
        "/auth/register",
        "/auth/forgot-password",
        "/auth/verify-forgot-password-token",
        "/auth/refresh-token",
    ]
    current_url = request.url.path
    if current_url.startswith("/static"):
        return True

    if current_url in allow_urls:
        return True
    return False


def get_token(header):
    bearer, _, token = header.partition(" ")
    if bearer != PREFIX:
        raise ValueError("Invalid token")

    return token
