from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import Base, engine
from .routes import router


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator",
    description="AI-powered 7-day fitness plan generator",
    version="1.0.0"
)


# Connect the static folder
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# Connect the templates folder
templates = Jinja2Templates(
    directory="templates"
)


# Include all application routes
app.include_router(router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "FitBuddy",
        "version": "1.0.0"
    }