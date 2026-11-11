
from fastapi import FastAPI

from backend.app.api.tasks import router as tasks_router
from backend.app.core.database import Base, engine
from backend.app.models.task import Task

app = FastAPI(
    title="Famora API",
    description="Your family's little AI organizer",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register API routes
app.include_router(tasks_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Famora!",
        "status": "Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
