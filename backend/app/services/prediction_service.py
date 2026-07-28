import shutil
import uuid
import json
import numpy as np
import tensorflow as tf

from pathlib import Path
from tensorflow.keras.preprocessing import image
from sqlalchemy.orm import Session

from app.core.config import (
    UPLOAD_DIR,
    BEST_MODEL_PATH,
    CLASS_INDEX_PATH,
    IMG_SIZE,
)

from app.models.prediction_model import PredictionRecord


class PredictionService:

    # ===========================
    # Load CNN Model
    # ===========================
    try:
        model = tf.keras.models.load_model(BEST_MODEL_PATH)

        with open(CLASS_INDEX_PATH, "r") as f:
            class_map = json.load(f)

        MODEL_LOADED = True
        print("✅ CNN Model Loaded Successfully")

    except Exception as e:
        model = None
        class_map = {}
        MODEL_LOADED = False
        print(f"❌ CNN Model Load Failed: {e}")

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

        # Save uploaded image
        saved_path = PredictionService.save_upload_file(file)

        # ===========================
        # AI Prediction
        # ===========================
        img = image.load_img(saved_path, target_size=IMG_SIZE)
        img = image.img_to_array(img)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)

        pred = PredictionService.model.predict(img, verbose=0)

        pred_index = int(np.argmax(pred))
        confidence = float(np.max(pred) * 100)

        prediction = PredictionService.class_map.get(str(pred_index), "Unknown")

        shelf_life_map = {
            "Room Temperature": "7-10 days",
            "Refrigerator": "20-30 days",
            "Oil Coated": "25-35 days",
            "Wet Cotton": "12-18 days",
        }

        estimated_shelf_life = shelf_life_map.get(prediction, "Unknown")

        prediction_data = {
            "prediction": prediction,
            "confidence": round(confidence, 2),
            "estimated_shelf_life": estimated_shelf_life,
            "status": "CNN Prediction",
        }

        # Save to database
        db_record = PredictionRecord(
            filename=saved_path.name,
            prediction=prediction_data["prediction"],
            confidence=prediction_data["confidence"],
            estimated_shelf_life=prediction_data["estimated_shelf_life"],
        )

        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        return {
            "id": db_record.id,
            "filename": db_record.filename,
            "prediction": db_record.prediction,
            "confidence": db_record.confidence,
            "estimated_shelf_life": db_record.estimated_shelf_life,
            "timestamp": db_record.timestamp,
            "status": prediction_data["status"],
        }