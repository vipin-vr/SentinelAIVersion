# SentinelAI

SentinelAI is an AI-powered road damage detection system that identifies potholes and cracks from road images using a custom-trained YOLO11 model.

## Features

- Detects potholes and cracks
- FastAPI backend for AI inference
- HTML/CSS/JavaScript frontend
- Returns:
  - Total detections
  - Object classes
  - Confidence scores
  - Image with bounding boxes

## Project Structure

```
SentinelAI/
│
├── ai/
│   ├── predict.py
│   ├── prepare_dataset.py
│   └── train.py
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── runs/
│   └── detect/
│       └── runs/
│           └── sentinel_ai/
│               └── weights/
│                   └── best.pt
│
├── README.md
└── .gitignore
```

## Installation

```bash
pip install -r backend/requirements.txt
```

## Run Backend

```bash
uvicorn backend.main:app --reload
```

Backend URL:

```
http://127.0.0.1:8000
```

Swagger API:

```
http://127.0.0.1:8000/docs
```

## Run Frontend

Open `frontend/index.html` using Live Server.

## Technologies

- Python
- YOLO11 (Ultralytics)
- FastAPI
- HTML
- CSS
- JavaScript

## Author

Vipin VR
