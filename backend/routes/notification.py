from fastapi import APIRouter
from sqlalchemy import text
from database import engine

router = APIRouter()

@router.get("/")
def get_notifications():

    query = text("""
        SELECT *
        FROM notifications
        ORDER BY created_at DESC
    """)

    with engine.connect() as conn:
        result = conn.execute(query)

        notifications = []

        for row in result:
            notifications.append({
                "notification_id": row.notification_id,
                "user_id": row.user_id,
                "title": row.title,
                "message": row.message,
                "is_read": row.is_read,
                "created_at": str(row.created_at)
            })

        return notifications


@router.post("/create")
def create_notification(
    user_id: int,
    title: str,
    message: str
):

    query = text("""
        INSERT INTO notifications
        (user_id, title, message)
        VALUES
        (:user_id, :title, :message)
    """)

    with engine.begin() as conn:
        conn.execute(
            query,
            {
                "user_id": user_id,
                "title": title,
                "message": message
            }
        )

    return {
        "message": "Notification Created"
    }