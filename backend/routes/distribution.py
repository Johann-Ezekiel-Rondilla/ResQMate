from fastapi import APIRouter
from sqlalchemy import text
from database import engine

router = APIRouter()


# GET ALL DISTRIBUTIONS
@router.get("/")
def get_distributions():

    query = text("""
        SELECT *
        FROM distributions
        ORDER BY distribution_id DESC
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        distributions = []

        for row in result:

            distributions.append({
                "distribution_id": row.distribution_id,
                "request_id": row.request_id,
                "resource_id": row.resource_id,
                "staff_id": row.staff_id,
                "quantity_given": row.quantity_given,
                "distribution_date": str(row.distribution_date)
            })

        return distributions


# CREATE DISTRIBUTION
@router.post("/create")
def create_distribution(
    request_id: int,
    resource_id: int,
    staff_id: int,
    quantity_given: int
):

    insert_query = text("""
        INSERT INTO distributions
        (
            request_id,
            resource_id,
            staff_id,
            quantity_given
        )
        VALUES
        (
            :request_id,
            :resource_id,
            :staff_id,
            :quantity_given
        )
    """)

    update_resource_query = text("""
        UPDATE resources
        SET quantity_available =
            quantity_available - :quantity_given
        WHERE resource_id = :resource_id
    """)

    with engine.begin() as conn:

        conn.execute(
            insert_query,
            {
                "request_id": request_id,
                "resource_id": resource_id,
                "staff_id": staff_id,
                "quantity_given": quantity_given
            }
        )

        conn.execute(
            update_resource_query,
            {
                "quantity_given": quantity_given,
                "resource_id": resource_id
            }
        )

    return {
        "message": "Distribution Recorded Successfully"
    }


# DELETE DISTRIBUTION
@router.delete("/{distribution_id}")
def delete_distribution(distribution_id: int):

    query = text("""
        DELETE FROM distributions
        WHERE distribution_id = :distribution_id
    """)

    with engine.begin() as conn:

        conn.execute(
            query,
            {
                "distribution_id": distribution_id
            }
        )

    return {
        "message": "Distribution Deleted Successfully"
    }