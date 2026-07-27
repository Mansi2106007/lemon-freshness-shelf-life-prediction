# Rind Report — lemon crop diagnosis

A web app for farmers: upload a photo of a Tahiti lime, get back what's
wrong with the peel and what to do about it. The damage categories and the
field recommendations are grounded in Botina A., García M., and Romero B.
(2019), *"Pre- and post-harvest factors that affect the quality and
commercialization of the Tahiti lime,"* Scientia Horticulturae 257.

## What's in this folder

```
lemon-cv/
├── config.py              # class list, paths, image size, training hyperparameters
├── diagnosis_data.py       # farmer-facing cause + field actions for each class
├── model/
│   ├── __init__.py
│   └── predict.py          # loads the trained CNN and runs real inference
├── api/
│   ├── app.py               # Flask backend: serves the site + /api/diagnose
│   ├── templates/index.html # the farmer-facing page
│   └── static/
│       ├── style.css
│       └── app.js
├── saved_models/           # trained .keras file goes here (not included yet)
├── artifacts/              # class_indices.json goes here (written by training)
└── requirements.txt
```

## Status: backend is production-ready, model is not trained yet

This part of the pipeline — the site, the upload flow, and the API contract
— is done and works end-to-end. What's still missing is the trained model
itself: `model/predict.py` looks for a file at
`saved_models/lemon_quality_best.keras` (or `lemon_quality_final.keras`)
plus `artifacts/class_indices.json`, and neither exists yet.

There is **no mock/fallback prediction** anywhere in this code on purpose.
Until a real model is dropped in, `POST /api/diagnose` returns HTTP 503
with a clear message instead of making something up. You can see this for
yourself — run the app now and try uploading a photo.

### To make it real, the CV/dataset side still needs:
1. A labelled image set sorted into the 9 folders named in `config.CLASSES`
   (healthy, sunburn, scars, pest_damage, yellowing, dehydration,
   brown_spot, mechanical_damage, microbial_damage).
2. A `model/train.py` that builds a `tf.data` pipeline from that folder
   structure, trains a CNN (transfer learning, e.g. MobileNetV2, is the
   sensible default for a dataset this size), and on completion:
   - saves the model to `config.BEST_MODEL_PATH`
   - writes `config.CLASS_INDEX_PATH` (a JSON `{"0": "healthy", "1": "scars", ...}`
     mapping the model's output order to class names — `predict.py` already
     expects this exact file and format)
3. Drop the resulting `.keras` file and `class_indices.json` into
   `saved_models/` and `artifacts/` respectively — no code changes needed,
   `/api/health` and `/api/diagnose` will pick them up automatically.

## Running it

```bash
cd lemon-cv
pip install -r requirements.txt
python api/app.py
```

Then open `http://localhost:5000`.

## API contract

**GET `/api/health`**
```json
{"status": "ok", "model_ready": false, "classes": ["healthy", "sunburn", ...]}
```

**POST `/api/diagnose`** — multipart form, field name `image` (jpg/png/webp, ≤8MB)

Success (200):
```json
{
  "predicted_class": "scars",
  "confidence": 0.87,
  "top_k": [{"class": "scars", "confidence": 0.87}, {"class": "sunburn", "confidence": 0.09}, ...],
  "diagnosis": {
    "label": "Scarring",
    "stage": "pre-harvest",
    "cause": "...",
    "actions": ["...", "..."]
  }
}
```

Model not trained yet (503) / bad upload (400) / unexpected error (500) all
return `{"error": "..."}`.
