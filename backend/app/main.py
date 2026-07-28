from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.database import Base, engine
from app.models.prediction_model import PredictionRecord

import os
import shutil

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Lemon Freshness & Shelf-Life Backend",
    version="1.0.0"
)

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Include API routes
app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Lemon Freshness API. Go to /docs for Swagger UI."
    }


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return JSONResponse(
            {
                "success": True,
                "message": "Image uploaded successfully",
                "filename": file.filename,
                "path": file_path
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )