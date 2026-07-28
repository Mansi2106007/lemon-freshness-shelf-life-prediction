import os
import json
import pandas as pd
import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint

# ==========================
# Paths
# ==========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(BASE_DIR, "dataset", "lemon_dataset.csv")
IMAGE_DIR = os.path.join(BASE_DIR, "dataset", "Images")

MODEL_DIR = os.path.join(BASE_DIR, "Backend", "ml_models")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "lemon_quality_best.keras")
CLASS_PATH = os.path.join(MODEL_DIR, "class_indices.json")

IMG_SIZE = (224, 224)

# ==========================
# Load Dataset
# ==========================

df = pd.read_csv(CSV_PATH)

print(f"Dataset Size: {len(df)}")

images = []
labels = []

for _, row in df.iterrows():

    img_path = os.path.join(IMAGE_DIR, row["Image_Name"])

    if not os.path.exists(img_path):
        continue

    img = load_img(img_path, target_size=IMG_SIZE)
    img = img_to_array(img) / 255.0

    images.append(img)
    labels.append(int(row["Condition_Code"]))

X = np.array(images)
y = np.array(labels)

print("Images Loaded:", len(X))

# ==========================
# Labels
# ==========================

num_classes = len(np.unique(y))

y_cat = to_categorical(y, num_classes=num_classes)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_cat,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# ==========================
# CNN
# ==========================

model = Sequential([

    Conv2D(32, (3,3), activation="relu", input_shape=(224,224,3)),
    MaxPooling2D(),

    Conv2D(64, (3,3), activation="relu"),
    MaxPooling2D(),

    Conv2D(128, (3,3), activation="relu"),
    MaxPooling2D(),

    Flatten(),

    Dense(128, activation="relu"),
    Dropout(0.5),

    Dense(num_classes, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

checkpoint = ModelCheckpoint(
    MODEL_PATH,
    monitor="val_accuracy",
    save_best_only=True,
    verbose=1
)

model.fit(
    X_train,
    y_train,
    validation_data=(X_test, y_test),
    epochs=20,
    batch_size=8,
    callbacks=[checkpoint]
)

loss, acc = model.evaluate(X_test, y_test)

print(f"\nFinal Accuracy: {acc:.4f}")

class_map = {}

for idx in sorted(df["Condition_Code"].unique()):
    label = df[df["Condition_Code"] == idx]["Condition"].iloc[0]
    class_map[str(idx)] = label

with open(CLASS_PATH, "w") as f:
    json.dump(class_map, f, indent=4)

print("\nModel Saved:")
print(MODEL_PATH)

print("\nClass Mapping Saved:")
print(CLASS_PATH)