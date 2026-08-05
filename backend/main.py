import shutil
import traceback
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO

# ----------------------------------------
# FastAPI
# ----------------------------------------
app = FastAPI()

# ----------------------------------------
# CORS
# ----------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------
# Paths
# ----------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "runs" / "detect" / "runs" / "sentinel_ai" / "weights" / "best.pt"

UPLOAD_DIR = BASE_DIR / "uploads"
RESULTS_DIR = BASE_DIR / "results"

UPLOAD_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# ----------------------------------------
# Load YOLO Model
# ----------------------------------------
print("Loading model...")
print("Model Path:", MODEL_PATH)

model = YOLO(str(MODEL_PATH))

print("Model Loaded Successfully!")

# ----------------------------------------
# Static Files
# ----------------------------------------
app.mount("/results", StaticFiles(directory=str(RESULTS_DIR)), name="results")


@app.get("/")
def home():
    return {"message": "Sentinel AI Backend Running"}


@app.post("/predict")
async def predict(request: Request, file: UploadFile = File(...)):
    try:

        filename = file.filename

        upload_path = UPLOAD_DIR / filename

        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("\n===============================")
        print("Uploaded File :", upload_path)

        # ----------------------------------------
        # Prediction
        # ----------------------------------------
        results = model.predict(
            source=str(upload_path),
            conf=0.25,
            imgsz=640,
            iou=0.45,
            augment=False,
            save=True,
            verbose=False
        )

        detections = []

        output_image_url = ""

        for result in results:

            output_image = Path(result.save_dir) / filename

            destination = RESULTS_DIR / filename

            print("YOLO Save Directory :", result.save_dir)
            print("YOLO Output Image   :", output_image)
            print("Destination         :", destination)

            print("Output Exists       :", output_image.exists())

            if output_image.exists():

                shutil.copy(output_image, destination)

                print("Image Copied Successfully!")

            else:

                print("ERROR: Output image not found!")

            print("Destination Exists  :", destination.exists())

            output_image_url = str(request.base_url) + f"results/{filename}"

            for box in result.boxes:

                detections.append({
                    "class": model.names[int(box.cls[0])],
                    "confidence": round(float(box.conf[0]), 2)
                })

        if upload_path.exists():
            upload_path.unlink()

        print("Output URL:", output_image_url)
        print("===============================\n")

        return {
            "success": True,
            "total_detections": len(detections),
            "detections": detections,
            "output_image": output_image_url
        }

    except Exception:

        print(traceback.format_exc())

        return {
            "success": False,
            "error": traceback.format_exc()
        }