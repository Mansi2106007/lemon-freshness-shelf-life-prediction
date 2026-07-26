# Lemon Freshness & Shelf-Life Prediction Backend

## Overview
Backend API for predicting lemon freshness and estimated shelf life.

## Tech Stack
- FastAPI
- Python
- SQLAlchemy
- SQLite/MySQL (jo bhi use kar rahe ho)
- Uvicorn

## Features
- Image Upload
- Prediction API
- Prediction History
- Health Check
- Swagger Documentation

## API Endpoints
GET /health
POST /predict
GET /history

## Installation

1. Clone the repository
2. Create virtual environment
3. Install requirements
4. Run:
uvicorn app.main:app --reload

## Swagger
http://127.0.0.1:8000/docs

## Current Status
Backend is functional with mock predictions.
Real AI model integration is pending until the dataset is available.