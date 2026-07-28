import os
import shutil

# ========= PATHS =========
SOURCE_DIR = r"../dataset/Images"
DEST_DIR = r"../dataset/train"

# ========= CLASS FOLDERS =========
classes = {
    "Room_Day": "Room Temperature",
    "Fridge_Day": "Refrigerator",
    "Oil_Day": "Oil Coated",
    "Cotton_Day": "Wet Cotton",
}

# Create destination folders
for folder in classes.values():
    os.makedirs(os.path.join(DEST_DIR, folder), exist_ok=True)

count = {
    "Room Temperature": 0,
    "Refrigerator": 0,
    "Oil Coated": 0,
    "Wet Cotton": 0,
}

# Copy images
for file in os.listdir(SOURCE_DIR):

    if not file.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    # Ignore Oil+Cotton images
    if file.startswith("Oil+Cotton"):
        continue

    src = os.path.join(SOURCE_DIR, file)

    copied = False

    for prefix, folder in classes.items():

        if file.startswith(prefix):

            dst = os.path.join(DEST_DIR, folder, file)

            shutil.copy2(src, dst)

            count[folder] += 1

            copied = True
            break

    if not copied:
        print("Skipped:", file)

print("\n========== DONE ==========")

for k, v in count.items():
    print(f"{k}: {v} images")

print("\nDataset prepared successfully!")