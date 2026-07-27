"""
model/predict.py
-----------------
Loads the trained CNN once and exposes a single function, `predict_image`,
that the API calls. There is no mock or placeholder path here on purpose:
if a trained model isn't present, this raises a clear error instead of
guessing, so the API layer can report that honestly rather than fake a
diagnosis.

Expects a model saved with model.save(...) in Keras format (.keras or
.h5) at config.BEST_MODEL_PATH (falls back to config.FINAL_MODEL_PATH),
trained with config.CLASSES in the same order as config.CLASS_INDEX_PATH
(written by model/train.py — see class_indices.json).
"""

import io
import json
import os

import numpy as np
from PIL import Image, UnidentifiedImageError

import config


class ModelNotReadyError(RuntimeError):
    """Raised when no trained model file / class index file can be found."""


_model = None          # lazily loaded tf.keras.Model
_class_names = None    # list[str], index-aligned with the model's output layer


def _resolve_model_path() -> str:
    if os.path.exists(config.BEST_MODEL_PATH):
        return config.BEST_MODEL_PATH
    if os.path.exists(config.FINAL_MODEL_PATH):
        return config.FINAL_MODEL_PATH
    raise ModelNotReadyError(
        "No trained model found. Expected a file at "
        f"'{config.BEST_MODEL_PATH}' or '{config.FINAL_MODEL_PATH}'. "
        "Run model/train.py first, or copy a trained .keras file into "
        "config.MODEL_DIR."
    )


def _load_class_names() -> list:
    """Load the index->class-name mapping written by model/train.py.

    We read this from disk instead of trusting config.CLASSES directly
    because Keras' image_dataset_from_directory sorts class folders
    alphabetically, which may not match the order in config.py. train.py
    writes the *actual* training order to class_indices.json — that file
    is the source of truth for what index 0, 1, 2... mean for this
    specific model file.
    """
    if not os.path.exists(config.CLASS_INDEX_PATH):
        raise ModelNotReadyError(
            f"No class index file found at '{config.CLASS_INDEX_PATH}'. "
            "This is written automatically by model/train.py during training."
        )
    with open(config.CLASS_INDEX_PATH, "r") as f:
        index_to_class = json.load(f)
    # JSON keys are strings; sort numerically to rebuild the ordered list.
    ordered = [index_to_class[str(i)] for i in range(len(index_to_class))]
    return ordered


def _get_model():
    """Lazily load (and cache) the Keras model and class name list."""
    global _model, _class_names
    if _model is None:
        # Check these first, and cheaply, before paying for a TensorFlow
        # import: a not-yet-trained model should fail fast with
        # ModelNotReadyError, not a slow import followed by a crash.
        model_path = _resolve_model_path()
        _class_names = _load_class_names()

        import tensorflow as tf  # noqa: PLC0415 — deliberately deferred, see above

        _model = tf.keras.models.load_model(model_path)

        expected = _model.output_shape[-1]
        if expected != len(_class_names):
            raise ModelNotReadyError(
                f"Model output has {expected} classes but class_indices.json "
                f"lists {len(_class_names)}. Re-train or re-export so these match."
            )
    return _model, _class_names


def is_ready() -> bool:
    """Cheap check the API can use for a health endpoint, without raising."""
    try:
        _get_model()
        return True
    except ModelNotReadyError:
        return False


def preprocess_image_bytes(image_bytes: bytes) -> np.ndarray:
    """Decode raw upload bytes into a normalized (1, H, W, 3) float32 array."""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img = img.convert("RGB")
    except UnidentifiedImageError as exc:
        raise ValueError("File is not a readable image (jpg/png/webp, etc.).") from exc

    img = img.resize(config.IMG_SIZE)
    arr = np.asarray(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def predict_image(image_bytes: bytes, top_k: int = 3) -> dict:
    """Run the trained model on one uploaded image.

    Returns:
        {
          "predicted_class": str,
          "confidence": float,             # 0-1, for the top class
          "top_k": [{"class": str, "confidence": float}, ...],
        }

    Raises:
        ModelNotReadyError: no trained model / class index file yet.
        ValueError: the uploaded bytes aren't a decodable image.
    """
    model, class_names = _get_model()
    batch = preprocess_image_bytes(image_bytes)

    probs = model.predict(batch, verbose=0)[0]  # shape: (num_classes,)

    order = np.argsort(probs)[::-1]
    top_k = min(top_k, len(class_names))
    ranked = [
        {"class": class_names[i], "confidence": float(probs[i])}
        for i in order[:top_k]
    ]

    return {
        "predicted_class": ranked[0]["class"],
        "confidence": ranked[0]["confidence"],
        "top_k": ranked,
    }
