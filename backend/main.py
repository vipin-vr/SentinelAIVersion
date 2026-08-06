import shutil
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO

# -----------------------------------
# FastAPI
# -----------------------------------
app = FastAPI()

# -----------------------------------
# Enable CORS
# -----------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# Project Paths
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "runs"
    / "detect"
    / "runs"
    / "sentinel_ai"
    / "weights"
    / "best.pt"
)

UPLOAD_DIR = BASE_DIR / "uploads"
RESULTS_DIR = BASE_DIR / "results"

UPLOAD_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# -----------------------------------
# Load Model
# -----------------------------------
model = YOLO(str(MODEL_PATH))

# -----------------------------------
# Serve Result Images
# -----------------------------------
app.mount("/results", StaticFiles(directory=str(RESULTS_DIR)), name="results")


@app.get("/")
def home():
    return {
        "message": "Sentinel AI Backend Running"
    }


@app.post("/predict")
async def predict(request: Request, file: UploadFile = File(...)):

    filename = file.filename

    upload_path = UPLOAD_DIR / filename

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = model.predict(
        source=str(upload_path),
        conf=0.02,
        imgsz=640,
        iou=0.45,
        augment=True,
        save=True,
        verbose=False
    )

    detections = []
    output_image_url = ""

    for result in results:

        output_image = Path(result.save_dir) / filename

        destination = RESULTS_DIR / filename

        shutil.copy(output_image, destination)

        # Dynamic URL (works locally and on Railway)
        output_image_url = f"{request.base_url}results/{filename}"

        for box in result.boxes:

            detections.append({
                "class": model.names[int(box.cls[0])],
                "confidence": round(float(box.conf[0]), 2)
            })

    return {
        "success": True,
        "total_detections": len(detections),
        "detections": detections,
        "output_image": output_image_url
    }