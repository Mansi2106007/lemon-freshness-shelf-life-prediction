# train_model.py

import pandas as pd
import os
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ==============================
# 1. Load Dataset
# ==============================

df = pd.read_csv("dataset/lemon_dataset.csv")

print("\nDataset Loaded Successfully!")
print("Original Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ==============================
# 2. Remove Empty Columns
# ==============================

df = df.dropna(axis=1, how="all")

print("\nAfter removing empty columns:")
print(df.shape)

print(df.columns.tolist())


# ==============================
# 3. Select Target
# ==============================

# Predicting lemon condition stage
target_column = "Condition_Code"

print("\nTarget Column:", target_column)


# Remove rows where target is missing
df = df.dropna(subset=[target_column])


# ==============================
# 4. Remove unnecessary columns
# ==============================

remove_columns = [
    "Sample_ID",
    "Image_Name",
    "Image_Path"
]

for col in remove_columns:
    if col in df.columns:
        df = df.drop(col, axis=1)


# ==============================
# 5. Encode Categorical Data
# ==============================

encoder = LabelEncoder()

for col in df.columns:
    if df[col].dtype == "object":
        df[col] = encoder.fit_transform(df[col])


# ==============================
# 6. Features and Target
# ==============================

X = df.drop(target_column, axis=1)

y = df[target_column]


print("\nFeature Shape:", X.shape)
print("Target Shape:", y.shape)


# ==============================
# 7. Train Test Split
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ==============================
# 8. Train Model
# ==============================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

print("\nModel Training Completed!")


# ==============================
# 9. Evaluate Model
# ==============================

prediction = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    prediction
)

print("\nAccuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, prediction))


# ==============================
# 10. Save Model
# ==============================

os.makedirs("models", exist_ok=True)

with open("ml/models/lemon_model.pkl", "wb") as f:
    pickle.dump(model, f)


print("\nModel saved successfully!")
print("Location: models/lemon_model.pkl")