from fastapi import APIRouter
from sqlalchemy import text
from database import engine

router = APIRouter()

@router.get("/")
def dashboard_stats():

    with engine.connect() as conn:

        total_requests = conn.execute(
            text("SELECT COUNT(*) FROM assistance_requests")
        ).scalar()

        pending_requests = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM assistance_requests
                WHERE status='Pending'
            """)
        ).scalar()

        approved_requests = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM assistance_requests
                WHERE status='Approved'
            """)
        ).scalar()

        total_users = conn.execute(
            text("SELECT COUNT(*) FROM users")
        ).scalar()

        total_resources = conn.execute(
            text("SELECT COUNT(*) FROM resources")
        ).scalar()

    return {
        "total_requests": total_requests,
        "pending_requests": pending_requests,
        "approved_requests": approved_requests,
        "total_users": total_users,
        "total_resources": total_resources
    }