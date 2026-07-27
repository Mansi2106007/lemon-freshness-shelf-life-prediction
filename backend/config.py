"""
config.py
----------
Single source of truth for the Lemon Quality CV pipeline: class names,
image size, folder locations, and training hyperparameters.

Every other script imports from here so the whole team (and the web/API
side) stays in sync with one class list.
"""

import os

# ---------------------------------------------------------------------------
# Class taxonomy
# ---------------------------------------------------------------------------
# Built directly from the damage categories described in the Tahiti lime
# paper (Botina et al., 2019): pre-harvest damage (sunburn, scars, pest
# damage) and post-harvest damage (yellowing, dehydration, brown spot,
# mechanical damage, microbial/fungal damage), plus a healthy class.
#
# NOTE: if you change this list, the folder names under DATA_ROOT/raw and
# DATA_ROOT/processed must match exactly (case-sensitive), and any already
# trained model becomes invalid (num_classes changes).
CLASSES = [
    "healthy",
    "sunburn",              # pre-harvest: sunspot / solar scald
    "scars",                # pre-harvest: wind/hail/thorn scratches
    "pest_damage",          # pre-harvest: mites, thrips, scale insects
    "yellowing",            # post-harvest: chlorophyll degradation
    "dehydration",          # post-harvest: shriveling, moisture loss
    "brown_spot",           # post-harvest: chilling injury / senescence
    "mechanical_damage",    # post-harvest: bruises, cuts, oleocellosis
    "microbial_damage",     # post-harvest: fungal rot (anthracnose, etc.)
]
NUM_CLASSES = len(CLASSES)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DATA_ROOT = os.path.join(PROJECT_ROOT, "data")
RAW_DIR = os.path.join(DATA_ROOT, "raw")              # unsorted / incoming photos
PROCESSED_DIR = os.path.join(DATA_ROOT, "processed")   # cleaned + resized, one folder per class
SPLIT_DIR = os.path.join(DATA_ROOT, "split")           # train/val/test, one folder per class

TRAIN_DIR = os.path.join(SPLIT_DIR, "train")
VAL_DIR = os.path.join(SPLIT_DIR, "val")
TEST_DIR = os.path.join(SPLIT_DIR, "test")

MODEL_DIR = os.path.join(PROJECT_ROOT, "saved_models")
ARTIFACT_DIR = os.path.join(PROJECT_ROOT, "artifacts")  # metrics, plots, class_indices.json

BEST_MODEL_PATH = os.path.join(MODEL_DIR, "lemon_quality_best.keras")
FINAL_MODEL_PATH = os.path.join(MODEL_DIR, "lemon_quality_final.keras")
CLASS_INDEX_PATH = os.path.join(ARTIFACT_DIR, "class_indices.json")

# ---------------------------------------------------------------------------
# Image / training hyperparameters
# ---------------------------------------------------------------------------
IMG_SIZE = (224, 224)      # matches MobileNetV2 / EfficientNet expected input
IMG_CHANNELS = 3
BATCH_SIZE = 32
SEED = 42

# Split ratios (must sum to 1.0)
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

# Transfer-learning training schedule
HEAD_EPOCHS = 15           # train the new classification head, base frozen
FINE_TUNE_EPOCHS = 15      # unfreeze top of the base model and fine-tune
FINE_TUNE_AT_LAYER = 100   # unfreeze layers from this index onward (MobileNetV2)
LEARNING_RATE_HEAD = 1e-3
LEARNING_RATE_FINE_TUNE = 1e-5

for _d in (DATA_ROOT, RAW_DIR, PROCESSED_DIR, SPLIT_DIR, MODEL_DIR, ARTIFACT_DIR):
    os.makedirs(_d, exist_ok=True)
