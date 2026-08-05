from fastapi import FastAPI

from routers.user_router import router as user_router

app = FastAPI(title = "Finance Portfolio Tracker", version = "1.0.0")

app.include_router(user_router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}