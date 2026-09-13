from fastapi import APIRouter
from sqlalchemy import text
from database import engine

router = APIRouter()


# GET ALL RESOURCES
@router.get("/")
def get_resources():

    query = text("""
        SELECT *
        FROM resources
        ORDER BY resource_id DESC
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        resources = []

        for row in result:

            resources.append({
                "resource_id": row.resource_id,
                "resource_name": row.resource_name,
                "quantity_available": row.quantity_available,
                "unit": row.unit,
                "last_updated": str(row.last_updated)
            })

        return resources


# CREATE RESOURCE
@router.post("/create")
def create_resource(
    resource_name: str,
    quantity_available: int,
    unit: str
):

    query = text("""
        INSERT INTO resources
        (
            resource_name,
            quantity_available,
            unit
        )
        VALUES
        (
            :resource_name,
            :quantity_available,
            :unit
        )
    """)

    with engine.begin() as conn:

        conn.execute(
            query,
            {
                "resource_name": resource_name,
                "quantity_available": quantity_available,
                "unit": unit
            }
        )

    return {
        "message": "Resource Added Successfully"
    }


# UPDATE RESOURCE
@router.put("/{resource_id}")
def update_resource(
    resource_id: int,
    quantity_available: int
):

    query = text("""
        UPDATE resources
        SET quantity_available = :quantity_available
        WHERE resource_id = :resource_id
    """)

    with engine.begin() as conn:

        conn.execute(
            query,
            {
                "quantity_available": quantity_available,
                "resource_id": resource_id
            }
        )

    return {
        "message": "Resource Updated Successfully"
    }


# DELETE RESOURCE
@router.delete("/{resource_id}")
def delete_resource(resource_id: int):

    query = text("""
        DELETE FROM resources
        WHERE resource_id = :resource_id
    """)

    with engine.begin() as conn:

        conn.execute(
            query,
            {
                "resource_id": resource_id
            }
        )

    return {
        "message": "Resource Deleted Successfully"
    }