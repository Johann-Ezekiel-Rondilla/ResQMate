from fastapi import APIRouter
from sqlalchemy import text
from database import engine

router = APIRouter()

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