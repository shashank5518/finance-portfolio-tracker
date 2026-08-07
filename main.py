from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions.user_service_exceptions import UserNotFoundError
from routers.user_router import router as user_router

app = FastAPI(title = "Finance Portfolio Tracker", version = "1.0.0")

app.include_router(user_router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundError
): 
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )