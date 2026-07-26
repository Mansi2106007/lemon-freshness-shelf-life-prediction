from fastapi import FastAPI
from app.api.routes import router
from app.core.database import engine, Base
from app.models.prediction_model import PredictionRecord

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Lemon Freshness & Shelf-Life Backend",
    version="1.0.0"
)

# Include API routes
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to the Lemon Freshness API. Go to /docs for Swagger UI."}