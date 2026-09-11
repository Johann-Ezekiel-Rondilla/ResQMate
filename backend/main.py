from fastapi import FastAPI
from routes.users import router as user_router

app = FastAPI(
    title="ResQMate API",
    version="1.0"
)

app.include_router(
    user_router,
    prefix="/users",
    tags=["Users"]
)

@app.get("/")
def home():
    return {
        "message": "ResQMate API Running"
    }