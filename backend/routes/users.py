from fastapi import APIRouter
from sqlalchemy import text
from database import engine
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str

@router.get("/")
def get_users():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    user_id,
                    full_name,
                    email,
                    role
                FROM users
            """)
        )

        users = []

        for row in result:
            users.append({
                "user_id": row.user_id,
                "full_name": row.full_name,
                "email": row.email,
                "role": row.role
            })

    return users

@router.post("/login")
def login_user(data: LoginRequest):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    user_id,
                    full_name,
                    email,
                    password,
                    role
                FROM users
                WHERE email = :email
            """),
            {"email": data.email}
        )

        user = result.fetchone()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid Email"
            )

        if user.password != data.password:
            raise HTTPException(
                status_code=401,
                detail="Invalid Password"
            )

        return {
            "user_id": user.user_id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "message": "Login Successful"
        }


@router.post("/register")
def register_user(data: RegisterRequest):

    with engine.connect() as conn:

        existing_user = conn.execute(
            text("""
                SELECT email
                FROM users
                WHERE email = :email
            """),
            {"email": data.email}
        ).fetchone()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        conn.execute(
            text("""
                INSERT INTO users
                (
                    full_name,
                    email,
                    password,
                    role
                )
                VALUES
                (
                    :full_name,
                    :email,
                    :password,
                    'community_user'
                )
            """),
            {
                "full_name": data.full_name,
                "email": data.email,
                "password": data.password
            }
        )

        conn.commit()

        return {
            "message": "Registration Successful"
        }