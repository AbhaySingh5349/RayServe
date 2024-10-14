# uvicorn server:app --host 0.0.0.0 --port 8001 --reload

from fastapi import FastAPI

from route import router as StatusRouter

# creating server
app = FastAPI(
    title="MLVerse Status_Check API",
    description="API for Status_Check Module"
)

# include routes
app.include_router(
    StatusRouter,
    tags=["Status-Check-Service"],
)

@app.get("/", status_code=200)
def check_test_route():
    return {"message": "status check server is running"}