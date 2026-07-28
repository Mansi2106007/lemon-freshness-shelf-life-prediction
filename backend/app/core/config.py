from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

UPLOAD_DIR = BASE_DIR / "app" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MODEL_DIR = BASE_DIR / "ml_models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

IMG_SIZE = (224, 224)

BEST_MODEL_PATH = MODEL_DIR / "lemon_quality_best.keras"
FINAL_MODEL_PATH = MODEL_DIR / "lemon_quality_final.keras"
CLASS_INDEX_PATH = MODEL_DIR / "class_indices.json"