from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from pathlib import Path

from app.database import get_db
from app.services.prediction_service import PredictionService
from app.models.prediction_model import PredictionRecord

router = APIRouter()

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "model": (
            "loaded"
            if PredictionService.MODEL_LOADED
            else "not_loaded"
        ),
        "version": "1.0.0",
        "service": "Lemon Freshness Backend API"
    }


@router.post("/predict")
async def predict_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    ext = Path(file.filename).suffix.lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG and PNG images are allowed."
        )

    # 👇 ADD THIS HERE
    contents = await file.read()

    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file.")

    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 5 MB.")

    # Reset file pointer so it can be saved later
    file.file.seek(0)

    try:
        result = PredictionService.process_and_save_prediction(file, db)

        return {
            "success": True,
            "message": "Image uploaded successfully.",
            "result": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

@router.get("/history")
def get_prediction_history(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    offset = (page - 1) * limit

    records = (
        db.query(PredictionRecord)
        .order_by(PredictionRecord.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    history = []

    for record in records:
        history.append({
            "id": record.id,
            "filename": record.filename,
            "prediction": record.prediction,
            "confidence": record.confidence,
            "estimated_shelf_life": record.estimated_shelf_life,
            "timestamp": record.timestamp
        })

    return {
        "page": page,
        "limit": limit,
        "count": len(history),
        "history": history
    }