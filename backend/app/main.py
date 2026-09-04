from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import requests

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Decision Queue API",
    description="API for managing product requests and decisions",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(requests.router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "healthy"}
