"""
api/app.py
-----------
Production Flask backend for the lemon-quality checker.

Routes
------
GET  /                Serves the farmer-facing web page.
POST /api/diagnose     Accepts an uploaded photo, runs it through the trained
                        CNN (model/predict.py), and returns the diagnosis.
GET  /api/health        Reports whether a trained model is currently loaded.

There is deliberately no mock prediction path: if the model isn't trained
yet, /api/diagnose returns HTTP 503 with a clear message rather than a
fabricated result.

Run with:
    cd lemon-cv
    pip install -r requirements.txt
    python api/app.py
Then open http://localhost:5000
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

import config
from diagnosis_data import get_diagnosis
from model import predict as predictor

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_UPLOAD_MB = 8

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024
# Frontend may end up served from a different origin/port during development
# (e.g. a separate React dev server) — CORS keeps that option open without
# extra config from whoever builds that piece.
CORS(app, resources={r"/api/*": {"origins": "*"}})


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "model_ready": predictor.is_ready(),
            "classes": config.CLASSES,
        }
    )


@app.route("/api/diagnose", methods=["POST"])
def diagnose():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded. Expected a multipart field named 'image'."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not _allowed_file(file.filename):
        return jsonify({"error": f"Unsupported file type. Allowed: {sorted(ALLOWED_EXTENSIONS)}"}), 400

    image_bytes = file.read()

    try:
        result = predictor.predict_image(image_bytes, top_k=3)
    except predictor.ModelNotReadyError as exc:
        return jsonify({"error": str(exc)}), 503
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:  # noqa: BLE001 — surface unexpected errors, don't crash silently
        app.logger.exception("Unexpected error during prediction")
        return jsonify({"error": "Prediction failed unexpectedly.", "detail": str(exc)}), 500

    diagnosis = get_diagnosis(result["predicted_class"])

    return jsonify(
        {
            "predicted_class": result["predicted_class"],
            "confidence": round(result["confidence"], 4),
            "top_k": [
                {"class": r["class"], "confidence": round(r["confidence"], 4)}
                for r in result["top_k"]
            ],
            "diagnosis": diagnosis,
        }
    )


if __name__ == "__main__":
    # debug=True is fine for local dev; turn off (or use gunicorn) in production.
    app.run(host="0.0.0.0", port=5000, debug=True)
