import shutil
from pathlib import Path
import uuid
from sqlalchemy.orm import Session

from app.core.config import UPLOAD_DIR
from app.models.prediction_model import PredictionRecord


class PredictionService:

    @staticmethod
    def save_upload_file(file) -> Path:
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path

    @staticmethod
    def process_and_save_prediction(file, db: Session):

        # 1. Save file locally
        saved_path = PredictionService.save_upload_file(file)

        # 2. Mock prediction (Until AI model is ready)
        prediction_data = {
            "prediction": "Fresh",
            "confidence": 98.5,
            "estimated_shelf_life": "12 days",
            "status": "Mock Prediction"
        }

        # 3. Save to SQLite database
        db_record = PredictionRecord(
            filename=saved_path.name,
            prediction=prediction_data["prediction"],
            confidence=prediction_data["confidence"],
            estimated_shelf_life=prediction_data["estimated_shelf_life"]
        )

        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        # 4. Return response
        return {
            "id": db_record.id,
            "filename": db_record.filename,
            "prediction": db_record.prediction,
            "confidence": db_record.confidence,
            "estimated_shelf_life": db_record.estimated_shelf_life,
            "timestamp": db_record.timestamp,
            "status": prediction_data["status"]
        }