# SentinelAI

SentinelAI is an AI-powered road damage detection system that identifies potholes and cracks from road images using a custom-trained YOLO11 model.

---

## 🚀 Live Demo

**Frontend:**  
https://vipin-vr.github.io/SentinelAIVersion/

**Backend API:**  
https://sentinelaiversion-production.up.railway.app

**Swagger API Documentation:**  
https://sentinelaiversion-production.up.railway.app/docs

---

## ✨ Features

- Detects potholes and road cracks using YOLO11
- FastAPI backend for AI inference
- Responsive HTML/CSS/JavaScript frontend
- Upload road images for instant prediction
- Returns:
  - Total detections
  - Detected object classes
  - Confidence scores
  - Processed image with bounding boxes

---

## 📂 Project Structure

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
├── Dockerfile
├── railway.json
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🛠 Technologies Used

- Python
- YOLO11 (Ultralytics)
- FastAPI
- HTML
- CSS
- JavaScript
- Railway
- GitHub Pages

---

## ⚙ Installation

Clone the repository:

```bash
git clone https://github.com/vipin-vr/SentinelAIVersion.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶ Run Backend

```bash
uvicorn backend.main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

## ▶ Run Frontend

Open:

```
frontend/index.html
```

using **VS Code Live Server**.

---

## 📸 How It Works

1. Upload a road image.
2. Click **Predict**.
3. The image is sent to the FastAPI backend.
4. YOLO11 detects potholes and cracks.
5. The processed image and detection details are displayed.

---

## 👨‍💻 Author

**Vipin VR**

GitHub: https://github.com/vipin-vr

---

## 📄 License

This project is developed for educational and hackathon purposes.