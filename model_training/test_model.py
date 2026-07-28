import pickle
import pandas as pd


# Load model
with open("ml/models/lemon_model.pkl", "rb") as file:
    model = pickle.load(file)

print("✅ Model loaded successfully!")


# Create sample input with SAME columns used during training
sample = pd.DataFrame({
    "Day": [5],
    "Condition": ["Fresh"],
    "Temperature": ["Room"],
    "Oil_Coated": [0],
    "Wet_Cotton": [0]
})


# Encode Condition and Temperature same way as training
from sklearn.preprocessing import LabelEncoder

encoder_condition = LabelEncoder()
sample["Condition"] = encoder_condition.fit_transform(sample["Condition"])

encoder_temperature = LabelEncoder()
sample["Temperature"] = encoder_temperature.fit_transform(sample["Temperature"])


# Prediction
prediction = model.predict(sample)

print("🍋 Lemon Condition Prediction:", prediction[0])