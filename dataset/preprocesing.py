import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# -------------------------------
# Load Dataset
# -------------------------------
df = pd.read_csv("lemon_dataset.csv")

print("Dataset Shape:", df.shape)
print(df.head())

# -------------------------------
# Handle Missing Values
# -------------------------------
df.fillna("Unknown", inplace=True)

# -------------------------------
# Remove Unnecessary Columns
# -------------------------------
drop_cols = ["Sample_ID", "Image_Name", "Image_Path", "Remarks"]

for col in drop_cols:
    if col in df.columns:
        df.drop(col, axis=1, inplace=True)

# -------------------------------
# Encode Categorical Features
# -------------------------------
label_encoder = LabelEncoder()

categorical_columns = df.select_dtypes(include="object").columns

for col in categorical_columns:
    df[col] = label_encoder.fit_transform(df[col])

print("\nEncoded Dataset")
print(df.head())

# -------------------------------
# Separate Features & Target
# -------------------------------

X = df.drop("Freshness", axis=1)
y = df["Freshness"]

# -------------------------------
# Feature Scaling
# -------------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# -------------------------------
# Train Test Split
# -------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTrain Shape :", X_train.shape)
print("Test Shape :", X_test.shape)

# -------------------------------
# Save Processed Data
# -------------------------------

pd.DataFrame(X_train).to_csv("X_train.csv", index=False)
pd.DataFrame(X_test).to_csv("X_test.csv", index=False)

pd.DataFrame(y_train).to_csv("y_train.csv", index=False)
pd.DataFrame(y_test).to_csv("y_test.csv", index=False)

print("\nPreprocessing Completed Successfully!")


from sklearn.feature_selection import SelectKBest, f_classif

selector = SelectKBest(score_func=f_classif, k=10)

X_selected = selector.fit_transform(X_scaled, y)

selected_features = X.columns[selector.get_support()]

print("Selected Features:")
print(selected_features)