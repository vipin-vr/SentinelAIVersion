import os
from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import shutil

app = FastAPI()

# Load the trained model only once
model = YOLO("runs/detect/runs/sentinel_ai/weights/best.pt")


@app.get("/")
def home():
    return {"message": "Sentinel AI Backend Running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    image_path = file.filename

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = model.predict(
        source=image_path,
        conf=0.05,
        save=True
    )

    detections = []
    output_image = ""

    for result in results:

        # Save output image path
        output_image = os.path.join(
            result.save_dir,
            os.path.basename(image_path)
        )

        for box in result.boxes:

            detections.append({
                "class": model.names[int(box.cls[0])],
                "confidence": round(float(box.conf[0]), 2)
            })

    return {
        "total_detections": len(detections),
        "detections": detections,
        "output_image": output_image
    }