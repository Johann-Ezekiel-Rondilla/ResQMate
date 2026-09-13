from fastapi import APIRouter
from sqlalchemy import text
from database import engine

router = APIRouter()


# GET ALL REQUESTS
@router.get("/")
def get_requests():

    query = text("""
        SELECT *
        FROM assistance_requests
        ORDER BY request_id DESC
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        requests = []

        for row in result:

            requests.append({
                "request_id": row.request_id,
                "user_id": row.user_id,
                "category_id": row.category_id,
                "location_id": row.location_id,
                "request_details": row.request_details,
                "priority_level": row.priority_level,
                "status": row.status,
                "date_requested": str(row.date_requested)
            })

        return requests


# GET REQUEST BY ID
@router.get("/{request_id}")
def get_request(request_id: int):

    query = text("""
        SELECT *
        FROM assistance_requests
        WHERE request_id = :request_id
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {
                "request_id": request_id
            }
        )

        row = result.fetchone()

        if not row:
            return {
                "message": "Request Not Found"
            }

        return {
            "request_id": row.request_id,
            "user_id": row.user_id,
            "category_id": row.category_id,
            "location_id": row.location_id,
            "request_details": row.request_details,
            "priority_level": row.priority_level,
            "status": row.status,
            "date_requested": str(row.date_requested)
        }


# CREATE REQUEST
@router.post("/create")
def create_request(
    user_id: int,
    category_id: int,
    location_id: int,
    request_details: str
):

    query = text("""
        INSERT INTO assistance_requests
        (
            user_id,
            category_id,
            location_id,
            request_details,
            status
        )
        VALUES
        (
            :user_id,
            :category_id,
            :location_id,
            :request_details,
            'Pending'
        )
    """)

    with engine.begin() as conn:

        conn.execute(
            query,
            {
                "user_id": user_id,
                "category_id": category_id,
                "location_id": location_id,
                "request_details": request_details
            }
        )

    return {
        "message": "Request Created Successfully"
    }


# UPDATE REQUEST STATUS
@router.put("/{request_id}/status")
def update_request_status(
    request_id: int,
    status: str,
    updated_by: int
):

    with engine.begin() as conn:

        # Get Request Owner
        user_query = text("""
            SELECT user_id
            FROM assistance_requests
            WHERE request_id = :request_id
        """)

        user_result = conn.execute(
            user_query,
            {
                "request_id": request_id
            }
        ).fetchone()

        if not user_result:
            return {
                "message": "Request Not Found"
            }

        user_id = user_result.user_id

        # Update Request Status
        update_query = text("""
            UPDATE assistance_requests
            SET status = :status
            WHERE request_id = :request_id
        """)

        conn.execute(
            update_query,
            {
                "status": status,
                "request_id": request_id
            }
        )

        # Insert History
        history_query = text("""
            INSERT INTO request_status_history
            (
                request_id,
                updated_by,
                status,
                remarks
            )
            VALUES
            (
                :request_id,
                :updated_by,
                :status,
                :remarks
            )
        """)

        conn.execute(
            history_query,
            {
                "request_id": request_id,
                "updated_by": updated_by,
                "status": status,
                "remarks": f"Status changed to {status}"
            }
        )

        # Create Notification
        notification_query = text("""
            INSERT INTO notifications
            (
                user_id,
                title,
                message
            )
            VALUES
            (
                :user_id,
                :title,
                :message
            )
        """)

        conn.execute(
            notification_query,
            {
                "user_id": user_id,
                "title": "Request Update",
                "message": f"Your request status is now {status}"
            }
        )

    return {
        "message": "Request Updated Successfully"
    }