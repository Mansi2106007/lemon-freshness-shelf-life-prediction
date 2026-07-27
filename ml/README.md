# Machine Learning Module - Lemon Freshness & Shelf-Life Prediction

## Overview

This module is responsible for training, testing, and saving the machine learning model used in the Lemon Freshness & Shelf-Life Prediction project.

## Features

- Data preprocessing
- Train/Test dataset generation
- Machine Learning model training
- Model testing and prediction
- Save trained model using Joblib

## Folder Structure

```
ml/
│── train_model.py          # Trains the machine learning model
│── test_model.py           # Tests the saved model
│── model_training.py       # Model development and experimentation
│── requirements.txt        # Python dependencies
│── README.md               # Documentation
│── models/
│   └── lemon_model.pkl     # Trained model
```

## Dataset

The dataset is located in the `dataset/` folder and contains:

- lemon_dataset.csv
- preprocessing.csv
- X_train.csv
- X_test.csv
- y_train.csv
- y_test.csv
- Lemon image dataset

## Machine Learning Workflow

1. Load dataset
2. Preprocess data
3. Split into training and testing sets
4. Train the model
5. Save the trained model
6. Load the saved model
7. Predict lemon freshness

## How to Train

```bash
python ml/train_model.py
```

## How to Test

```bash
python ml/test_model.py
```

## Output

Example:

```
✅ Model loaded successfully!
🍋 Lemon Condition Prediction: Fresh
```

*(The prediction label depends on the trained model.)*

## Developed By

Role 3 – Machine Learning Model Development