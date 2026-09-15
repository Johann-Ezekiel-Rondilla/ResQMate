from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from database import engine

router = APIRouter()


class LoginRequest(BaseModel):
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


@router.post("/register")
def register_user():

    return {
        "message": "User Registered Successfully"
    }


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
            {
                "email": data.email
            }
        ).fetchone()

    if not result:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if result.password != data.password:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "user_id": result.user_id,
        "full_name": result.full_name,
        "email": result.email,
        "role": result.role
    }