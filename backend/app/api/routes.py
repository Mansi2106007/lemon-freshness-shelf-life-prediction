from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from pathlib import Path

# Relative imports use kar rahe hain taaki ModuleNotFoundError na aaye
from ..core.database import get_db
from ..services.prediction_service import PredictionService
from ..models.prediction_model import PredictionRecord

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "Backend API is running"}

@router.post("/predict")
async def predict_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    allowed_extensions = [".jpg", ".jpeg", ".png"]
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed types: {allowed_extensions}"
        )
    
    try:
        result = PredictionService.process_and_save_prediction(file, db)
        return {
            "message": "Image processed and saved successfully!",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
def get_prediction_history(db: Session = Depends(get_db)):
    records = db.query(PredictionRecord).all()
    return {"total": len(records), "history": records}